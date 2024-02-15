from openai import OpenAI
import os
import json
from tqdm import tqdm


SYSTEM_PROMPT = "You are a supercomputer Go Engine that plays live Go games. Given the SGF notation for a given puzzle, play the best next move. Do not return anything except for the next move."


def evaluate(file_path, inference_func):
  """

    Args:
        file_path (str): The json path containing the puzzles to be evaluated
        inference_func (function): The function to be used for inference. Should take a string as input and return a string as output.

    Returns:
        total_correct (str): The total number of correct predictions
        total (str): The total number of predictions
  """
  with open(file_path, 'r') as file:
    cleaned_puzzles = json.load(file)
  
  result_dict = {} 

  total_correct = 0
  total_puzzles = len(cleaned_puzzles)

  # Initialize tqdm progress bar
  progress_bar = tqdm(total=total_puzzles, desc="Processing Puzzles", unit="puzzle")

  for puzzle in cleaned_puzzles:
      puzzle_id = puzzle["filename"].split(".")[0]
      bool_eval = [go_move[1] in inference_func(go_move[0]) for go_move in puzzle["moves"]]
      correct = all(bool_eval)
      total_correct += correct

      result_dict[puzzle_id] = 1 if correct else 0
      # Update progress bar
      progress_bar.update(1)
      accuracy = total_correct / progress_bar.n * 100
      progress_bar.set_postfix(accuracy=f"{accuracy:.2f}%")

  # Close progress bar
  progress_bar.close()
  
  with open("evaluation.json", 'w') as outfile:
    json.dump(result_dict, outfile)

  return total_correct, total_puzzles


def infer_RLHF(message):
  client = OpenAI(
    api_key=os.environ.get("KEY"),
  )
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature= 0,
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": message},
    ]
  )
  return response.choices[0].message.content.strip()

def infer_gpt4(message):
  client = OpenAI(
    api_key=os.environ.get("KEY"),
  )
  response = client.chat.completions.create(
    model="gpt-4",
    temperature= 0,
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": message},
    ]
  )
  return response.choices[0].message.content.strip()

def infer_instruct(message):
  client = OpenAI(
    api_key=os.environ.get("KEY"),
  )
  response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    temperature= 0,
    max_tokens=300,
    prompt = SYSTEM_PROMPT + "\n" + message
  )
  return response.choices[0].text.strip()

acc_cnt, total = evaluate("go_sgf/combined_sgf2.json", infer_instruct)
print("infer_instruct", acc_cnt)

#GPT4 6/98
#instruct 1/98