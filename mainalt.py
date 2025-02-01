import openai

openai.api_key = "YOUR_API_KEY"  # Replace with your OpenAI API key

def generate_paragraph(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or another suitable engine
        prompt=prompt,
        max_tokens=150,  # Adjust as needed for desired length
        temperature=0.7,  # Adjust for creativity
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    prompt = "Write a paragraph about the benefits of exercise."
    paragraph = generate_paragraph(prompt)
    print(paragraph)