from openai import OpenAI
import os

print(os.environ["KEY"])

client = OpenAI(
    api_key=os.environ.get("KEY"),
)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a supercomputer Chess Engine that plays live chess games. Given the algebraic notation for a given match, play the best next move. Do not return anything except for the algebraic notation for your move."},
    {"role": "user", "content": "1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6 4. d4 exd4 5. O-O Bc5 6. e5 Ne4 7. Re1 d5 8. Bxd5 Nxf2"},
  ]
)
print(response)