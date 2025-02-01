from openai import OpenAI
from dotenv import load_dotenv


class CodeGenerator:
    def __init__(self):
        # Initialize LLM here
        self.client = OpenAI()

    def generate_response(self):
        # Prompt ChatGPT and return response
        chat_completion = self.client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[
				{
					"role": "user",
	                "content": "Please create a multi-sentence paragraph about a random topic for a typing game. Please try to make them fun facts about history, biology, science, or literature. Make it 3-5 sentences please."
				}		
			]
		)
        return chat_completion.choices[0].message.content