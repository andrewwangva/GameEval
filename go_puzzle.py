import json
import requests

class Puzzle:
    base_url = 'https://online-go.com/api/v1/puzzles/'

    def __init__(self):
        self.initial_state_white = []
        self.initial_state_black = []
        self.game_size = None
        self.tree = None
        self.initial_player = None
        self.source = None
        self.valid = False
        self.date = "0"
    @classmethod
    def from_json(cls, data):
        if not data:
            raise ValueError('No valid object as JSON result given')

        puzzle_data = data.get('puzzle', None)
        if(puzzle_data == None):
            return None
        
        
        puzzle = cls()

        puzzle.id = int(data['id'])
        puzzle.game_size = int(puzzle_data['width'])
        height = int(puzzle_data['height'])
        if puzzle.game_size != height:
            puzzle.game_size = f"{puzzle.game_size}:{height}"
        
        puzzle.date = data.get("created", None).split("-")[0]
        rating =  data.get("rating", None)
        rating_cnt = data.get("rating_count", None)
        if(rating == None or rating_cnt == None):
            return None
        rating, rating_cnt = int(rating), int(rating_cnt)
        if(not(puzzle.game_size == 19 and puzzle.date == "2023")):
            print(puzzle.game_size, puzzle.date)
            return None

        puzzle.initial_state_white = [puzzle_data['initial_state']['white'][i:i+2] for i in range(0, len(puzzle_data['initial_state']['white']), 2)]
        puzzle.initial_state_black = [puzzle_data['initial_state']['black'][i:i+2] for i in range(0, len(puzzle_data['initial_state']['black']), 2)]
        puzzle.initial_player = puzzle_data['initial_player'][0].upper()
        puzzle.tree = puzzle_data['move_tree']

        return puzzle

    @classmethod
    def from_url(cls, id):
        response = requests.get(f"{cls.base_url}{id}")
        data = json.loads(response.text)
        return cls.from_json(data)

    @classmethod
    def collection_summary(cls, id):
        response = requests.get(f"{cls.base_url}{id}/collection_summary")
        return response

    def save(self, filename='test.sgf'):
        with open(filename, 'w') as file:
            file.write('(;')
            file.write('FF[4]')
            file.write('GM[1]')
            file.write(f"SZ[{self.game_size}]")
            file.write("\n")
            file.write(self.initial_state_to_sgf('W', self.initial_state_white))
            file.write(self.initial_state_to_sgf('B', self.initial_state_black))
            file.write(f"PL[{self.initial_player}]")
            file.write("\n")
            self.save_moves(file, self.tree, self.initial_player)
            file.write(")")

    def save_moves(self, file, tree, player):
        if tree['x'] != -1 and tree['y'] != -1:
            file.write(f";{player}[{self.sgf_board_position(tree)}]")
            player = self.invert_color(player)
            comment = tree.get('text', None)

            if 'correct_answer' in tree:
                comment = "Correct."
            elif 'wrong_answer' in tree:
                comment = "Wrong."

            if comment:
                file.write(f"C[{escape_for_sgf(comment)}]")

        if "marks" in tree:
            for mark in tree['marks']:
                position = self.sgf_board_position(mark)
                type = mark['marks']

                if type.get('circle'):
                    file.write(f"CR[{position}]")
                if type.get('triangle'):
                    file.write(f"TR[{position}]")
                if type.get('cross'):
                    file.write(f"MA[{position}]")
                if type.get('square'):
                    file.write(f"SQ[{position}]")
                if type.get('letter'):
                    file.write(f"LB[{position}:{type['letter']}]")

        if "branches" in tree:
            if len(tree['branches']) > 1:
                for branch in tree['branches']:
                    file.write('(')
                    self.save_moves(file, branch, player)
                    file.write(")\n")
            elif len(tree['branches']) == 1:
                self.save_moves(file, tree['branches'][0], player)

    @staticmethod
    def invert_color(color):
        return 'B' if color == 'W' else 'W'

    @staticmethod
    def sgf_board_position(tree):
        x = chr(ord('a') + tree['x'])
        y = chr(ord('a') + tree['y'])
        return f"{x}{y}"

    @staticmethod
    def initial_state_to_sgf(color, state):
        if not state:
            return ''
        return f'A{color}' + ''.join([f"[{s}]" for s in state]) + "\n"

def escape_for_sgf(s):
    return s.replace(']', '\\]').strip()
"""
for i in range(50000):
    puzzle = Puzzle.from_url(i)
    if(puzzle == None):
        continue
    print(puzzle)
    puzzle.save(f"sgf_go/output_{i}.sgf")
    break
"""

for i in range(1, 5001):
    if(i % 100 == 0):
        print(i)
    response = requests.get(f"https://online-go.com/api/v1/puzzles?page={i}")
    data = json.loads(response.text)
    if "results" not in data:
        continue
    for entry in data["results"]:
        date = entry["created"].split("-")[0]
        if(date == "2023"):
            id = entry["id"]
            print(entry["id"])
            puzzle = Puzzle.from_url(entry["id"])
            if(puzzle == None):
                continue
            print(puzzle)
            puzzle.save(f"sgf_go/output_{id}.sgf")