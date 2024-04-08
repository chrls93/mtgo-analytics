from flask import Flask, render_template, request
import os
import dotenv
from openai import OpenAI
import psycopg2
from bot_insights import bot_answer
import json

dotenv.load_dotenv()
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
    card_data_for_ai = json.dumps(card_data)
    # Ai function call below + insights parameter in return
    card_insights = bot_answer(card_data_for_ai)
    #card_insights = """ChatCompletion(id='chatcmpl-93S3nnCvry6HimROSls2qJqp1IOY1', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='{\n "card_name": "Vedalken Heretic",\n "mana_cost": "{G}{U}",\n "type": "Creature",\n "subtype": "Vedalken Rogue",\n "power": 1.0,\n "toughness": 1.0,\n "image_url": "https://cards.scryfall.io/png/front/5/a/5ab2ba75-e52e-46f5-8a34-3fe1e07446fd.png?1562641484",\n "Cost-Efficiency": {\n "analysis": "The mana cost of {G}{U} is considered relatively low for a card that potentially allows card draw. The ability to draw a card upon dealing damage to an opponent provides good value for the cost."\n },\n "Synergy": {\n "analysis": "The ability of Vedalken Heretic to draw a card upon dealing damage synergizes well with strategies focusing on aggression and card advantage. It encourages players to attack with the creature to benefit from the card draw effect."\n },\n "Resource Management": {\n "analysis": "Vedalken Heretic offers a resource generation mechanism by potentially providing card advantage each time it deals damage. This can help replenish hand size and maintain card advantage over the opponent."\n },\n "Creature Type": {\n "analysis": "Being a Vedalken Rogue, the creature type may have synergy with other cards that care about Rogues or Vedalkens. Tribal synergies centered around Rogues or Vedalkens could enhance the card\'s effectiveness in certain deck archetypes."\n },\n "Versatility": {\n "analysis": "Vedalken Heretic\'s ability to draw cards upon dealing damage makes it versatile in decks that need card advantage or seek to apply pressure on the opponent. It can fit well in aggressive strategies or decks focused on card draw."\n },\n "Overall Assessment": {\n "strengths": "Good cost-efficiency with potential card draw, synergistic ability with aggression strategies, resource generation through card advantage, tribal synergy possibilities, versatile in various deck archetypes.",\n "weaknesses": "Vulnerable as a 1/1 creature, requires dealing damage to trigger ability.",\n "utility": "Overall, Vedalken Heretic offers valuable card advantage potential and fits well in decks that can support its aggression-based strategy or benefit from consistent card draw."\n }\n}', role='assistant', function_call=None, tool_calls=None))], created=1710609875, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint='fp_4f2ebda25a', usage=CompletionUsage(completion_tokens=502, prompt_tokens=404, total_tokens=906))"""
    return render_template('random_card.html', card_name=card_data['name'],
                           mana_cost=card_data['mana_cost'], type_line=card_data['type_line'],
                           oracle_text=card_data['oracle_text'], power=card_data['power'],
                           toughness=card_data['toughness'], card_image=card_data['image_uris_png'], insights=card_insights)

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


if __name__ == '__main__':
    app.run(debug=True)
