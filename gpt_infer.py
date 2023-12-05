from openai import OpenAI
import os
import json

SYSTEM_PROMPT = "You are a supercomputer Chess Engine that plays live chess games. Given the algebraic notation for a given match, play the best next move. Do not return anything except for the algebraic notation for your move."

client = OpenAI(
    api_key=os.environ.get("KEY"),
)

with open("cleaned_chess_puzzles.json", 'r') as file:
    cleaned_puzzles = json.load(file)

print(len(cleaned_puzzles))

def infer_RLHF(message):

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature= 0,
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": message},
    ]
  )
  return response.choices[0].message.content.strip()

def infer_instruct(message):
  
  response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    temperature= 0,
    max_tokens=10,
    prompt = SYSTEM_PROMPT + "\n" + message
  )
  return response.choices[0].text.strip()


acc_cnt = 0

correcy_array = [0 for i in range(len(cleaned_puzzles))]
for i in range(len(cleaned_puzzles)):
  bool_flag = True
  for j in range(len(cleaned_puzzles[i]["puzzle_solution"])):
    response = infer_instruct(cleaned_puzzles[i]["puzzle_input"][j])
    if(cleaned_puzzles[i]["puzzle_solution"][j] not in response):
      bool_flag = False
      print(i)
      break
  
  if(bool_flag):
    acc_cnt += 1
    correcy_array[i] = 1

print(acc_cnt)

#print(correcy_array)

with open("accuracy_instruct.json", 'w') as json_file:
    json.dump(correcy_array, json_file, indent=4)
