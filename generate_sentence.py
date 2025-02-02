from openai import OpenAI
from dotenv import load_dotenv
from random import randrange 

fun_fact_topics = [
    "Space and Astronomy",
    "Deep Sea Creatures",
    "Ancient Civilizations",
    "Weird Laws Around the World",
    "Unusual Phobias",
    "Rare Animal Species",
    "Forgotten Inventions",
    "Famous Unsolved Mysteries",
    "Strange Food from Different Cultures",
    "Mind-Blowing Optical Illusions",
    "Physics Phenomena That Seem Like Magic",
    "Cool Mathematical Paradoxes",
    "Historical Figures with Unexpected Hobbies",
    "The Origins of Everyday Phrases",
    "Surprising Facts About the Human Body",
    "Bizarre Coincidences in History",
    "Hidden Messages in Popular Movies",
    "Unexplained Scientific Phenomena",
    "Unusual Jobs That Actually Exist",
    "Animals with Superpowers"
]

class CodeGenerator:
    def __init__(self):
        # Initialize LLM here
        self.client = OpenAI()
    
    def generate_paragraph(self):
        # Select a random topic from the list
        topic = fun_fact_topics[randrange(len(fun_fact_topics))]
        
        # Prompt ChatGPT and return response
        chat_completion = self.client.chat.completions.create(
            model="gpt-4",  # Ensure you are using the correct model name
            messages=[
                {
                    "role": "user",
                    "content": f"Please create a single sentence about space/constellations for a typing game. No longer, no shorter. Preferably under 50 words. Only generate one fun fact. Do not use a quote, and do not surround the sentence with quotes."
                }		
            ]
        )
        return chat_completion.choices[0].message.content