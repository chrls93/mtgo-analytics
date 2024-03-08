from flask import Flask, render_template, request
import os
import dotenv
from openai import OpenAI
import psycopg2


dotenv.load_dotenv()
client = OpenAI()
app = Flask(__name__)

def connect_to_database():
    conn = psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USERNAME"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_IP"),
        port=os.getenv("DATABASE_PORT")
    )
    return conn

def fetch_random_row_data(table_name):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute(f"""SELECT 
oracle_id
,name
,mana_cost
,type_line
,oracle_text
,power
,toughness
,image_uris_png
FROM {table_name} 
WHERE type_line NOT LIKE '%TOKEN%'
ORDER BY RANDOM()
LIMIT 1""")
    data = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    conn.close()
    return data, column_names

def unique_values(column, data):
    unique_values_set = set()
    for row in data:
        unique_values_set.add(row[column])
    return sorted(unique_values_set)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decklists')
def decklists():
    return render_template('decklists.html')

@app.route('/random_card')
def random_card():
    # Fetch random card data
    data, column_names = fetch_random_row_data('MTG_LIBRARY.ORACLE_CARDS')
    
    card_data = dict(zip(column_names, data[0]))
    
    return render_template('random_card.html', card_name=card_data['name'],
                           mana_cost=card_data['mana_cost'], type_line=card_data['type_line'],
                           oracle_text=card_data['oracle_text'], power=card_data['power'],
                           toughness=card_data['toughness'], card_image=card_data['image_uris_png'])

@app.route('/send_request_to_openai', methods=['POST'])
def send_request_to_openai():
    data = request.json
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": """Design an API endpoint response that, given a Magic: The Gathering card's data, provides a detailed analysis of the card's attributes and mechanics. The response should include the following sections:
    Cost-Efficiency: Evaluate the mana cost and any additional costs in relation to the card's stats or effects.
    Synergy: Assess the synergy between the card's abilities and how they complement each other or interact with other cards.
    Resource Management: Analyze any resource generation or consumption mechanisms the card offers and discuss their implications for gameplay.
    Creature Type: Discuss the significance of the card's creature type, if applicable, in terms of tribal synergies or thematic connections.
    Versatility: Consider the card's flexibility in fitting into various deck archetypes or strategies, highlighting potential use cases.
    Overall Assessment: Provide a concise summary of the card's strengths, weaknesses, and overall utility within the Magic: The Gathering ecosystem.
    Ensure that the API response is structured and easily readable, providing clear insights into the card's gameplay implications."""},
    {data}]
    )
    insights = f"Sample insights for {data['card_name']}..."
    return jsonify({"insights": insights})

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


if __name__ == '__main__':
    app.run(debug=True)
