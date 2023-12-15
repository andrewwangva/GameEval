import json

def calculate_elo(player_elo, opponents_elo, results):
    """
    Calculate a player's Elo rating.

    Parameters:
    - player_elo: The current Elo rating of the player.
    - opponents_elo: List of opponents' Elo ratings.
    - results: List of results, where 1 represents a win and 0 represents a loss.

    Returns:
    - The updated Elo rating of the player.
    """
    k_factor = 512  # K-factor determines how much the ratings will change after each game

    for i in range(len(opponents_elo)):
        if(i < 100):
            k_factor = k_factor * 0.95
            k_factor = max(k_factor, 16)
        expected_score = 1 / (1 + 10 ** ((opponents_elo[i] - player_elo) / 400))
        actual_score = results[i]

        rating_change = k_factor * (actual_score - expected_score)
        player_elo += rating_change
        

    return int(player_elo)  # Round to the nearest integer (optional)



with open("accuracy_RLHF2500.json", 'r') as file:
    accuracy = json.load(file)

with open("cleaned_chess_puzzles.json", 'r') as file:
    cleaned_puzzles = json.load(file)

eval_num = 2500
accuracy = accuracy[:2500]
cleaned_puzzles = cleaned_puzzles[:2500]

puzzle_themes = {
    "endgame": {"puzzle_rating": [], "result": []},
    "middlegame": {"puzzle_rating": [], "result": []},
    "mate": {"puzzle_rating": [], "result": []},
    "pin": {"puzzle_rating": [], "result": []},
    "fork": {"puzzle_rating": [], "result": []},
    "defensive": {"puzzle_rating": [], "result": []},
    "sacrifice": {"puzzle_rating": [], "result": []},
    "Attack": {"puzzle_rating": [], "result": []},
}

ratings = []


for i, row in enumerate(cleaned_puzzles):
    ratings.append(row["Rating"])
    for key, value in puzzle_themes.items():
        if(key in row["Themes"]):
            value["puzzle_rating"].append(row["Rating"])
            value["result"].append(accuracy[i])

for key, value in puzzle_themes.items():
    print(key, calculate_elo(1200, value["puzzle_rating"], value["result"]))

ELO = calculate_elo(1200, ratings, accuracy)
print("ELO: ", ELO)
print("Accuracy:", sum(accuracy)/len(accuracy))



