from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

def bot_answer(query_result):

    detailed_prompt = """
    You are magic the gathering pro player, with multimple top tournament finishes and trophies.Based on charateristics in provided data describe card using these guidelines:.
    Design an API endpoint response that, given a Magic: The Gathering card's data, provides a detailed analysis of the card's attributes and mechanics. The response should include the following sections:
    Cost-Efficiency: Evaluate the mana cost and any additional costs in relation to the card's stats or effects.
    Synergy: Assess the synergy between the card's abilities and how they complement each other or interact with other cards.
    Resource Management: Analyze any resource generation or consumption mechanisms the card offers and discuss their implications for gameplay.
    Creature Type: Discuss the significance of the card's creature type, if applicable, in terms of tribal synergies or thematic connections.
    Versatility: Consider the card's flexibility in fitting into various deck archetypes or strategies, highlighting potential use cases.
    Overall Assessment: Provide a concise summary of the card's strengths, weaknesses, and overall utility within the Magic: The Gathering ecosystem.
    Ensure that the API response is structured and easily readable, providing clear insights into the card's gameplay implications. """
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": detailed_prompt},
        {"role": "user", "content": query_result}
    ]
    )
    return completion