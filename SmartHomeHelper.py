from openai import OpenAI

import json

CONFIG_FILE = 'secrets.json'

# Set your API key
with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)
    client = OpenAI(api_key=config["openAI_API_key"])

# Define the engine ID for Smart Home Helper
engine_id = 'Smart Home Helper'

# Create a request to the OpenAI API
response = client.chat.completions.create(model=engine_id,
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Please help me schedule a meeting with the team tomorrow at 10 AM."}
],
max_tokens=100)

# Print the response
print(response.choices[0].message.content.strip())
