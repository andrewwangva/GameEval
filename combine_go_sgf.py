import os
import json

# Define the directory containing the SGF files and the output JSON file
sgf_directory = './go_sgf'
output_json_file = './go_sgf/combined_sgf.json'

# Initialize an empty list to store the SGF data
sgf_data = []

# Iterate through all files in the sgf_directory
for filename in os.listdir(sgf_directory):
    if filename.endswith('.sgf'):
        file_path = os.path.join(sgf_directory, filename)
        with open(file_path, 'r', encoding='utf-8') as sgf_file:
            sgf_contents = sgf_file.read()
            if("Correct." in sgf_contents):
                sgf_data.append({
                    'filename': filename,
                    'content': sgf_contents
                })


for puzzle in sgf_data:
    content = puzzle["content"]
    content_lines = content.split("\n")
    base_puzzle = content_lines[0] + "\n" + content_lines[1] + "\n" + content_lines[2] +  "\n" + content_lines[3] + "C[What is the best next move?]"
    #print(base_puzzle)

    puzzle_moves = content_lines[4].split("C[Correct.]")[0].split(";")[1:]
    puzzle["moves"] = []
    puzzle["moves"].append((base_puzzle[:], ";" + puzzle_moves[0]))
    base_puzzle += "\n" + ";" + puzzle_moves[0]
    for i in range(1, len(puzzle_moves), 2):
        base_puzzle += "\n" + ";" + puzzle_moves[i]
        print(i, len(puzzle_moves), puzzle["filename"])  
        puzzle["moves"].append((base_puzzle[:], ";" + puzzle_moves[i+1]))   
                       
        base_puzzle += "\n" + ";" + puzzle_moves[i+1]
# Write the combined SGF data to a JSON file
with open(output_json_file, 'w', encoding='utf-8') as json_file:
    json.dump(sgf_data, json_file, ensure_ascii=False, indent=4)

print(f"Combined {len(sgf_data)} SGF files into {output_json_file}.")
