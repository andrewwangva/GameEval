from openai import OpenAI
import os

print(os.environ["KEY"])

client = OpenAI(
    api_key=os.environ.get("KEY"),
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello?"},
  ]
)
print(response)