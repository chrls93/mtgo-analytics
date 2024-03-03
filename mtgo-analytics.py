from flask import Flask, render_template
import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()
client = OpenAI()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decklists')
def decklists():
    return render_template('decklists.html')

@app.route('/database')
def database():
    return render_template('database.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

if __name__ == '__main__':
    app.run(debug=True)
