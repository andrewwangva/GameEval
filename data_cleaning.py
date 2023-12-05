import pandas as pd
import chess
import chess.pgn
import io
import json
import os

def create_board_from_pgn_moves(pgn_moves):
    board = chess.Board()
    pgn_game = chess.pgn.read_game(io.StringIO(pgn_moves))

    for move in pgn_game.mainline_moves():
        board.push(move)

    return board

def add_move(pgn_game, pgn_move):
    moves = pgn_game.split()

    move_number = len(moves) // 3 + 1
    move_string = ""
    if(len(moves) % 3 == 0):
        move_string += f" {move_number}."

    move_string += f" {pgn_move}"

    pgn_game += move_string

    return pgn_game

def create_puzzles(pgn_moves, UCI_moves):
    board = create_board_from_pgn_moves(pgn_moves)
    board_positions = []
    board_solutios = []

    for i in range(len(UCI_moves)):
        parsed_move = chess.Move.from_uci(UCI_moves[i])
        pgn_move = board.san(parsed_move)

        pgn_moves = add_move(pgn_moves, pgn_move)
        
        if(i % 2 == 0):
            board_positions.append(pgn_moves)
        if(i % 2 == 1):
            board_solutios.append(pgn_move)
        board.push(parsed_move)

    return board_positions, board_solutios

def splice_pgn_moves(pgn_moves, move_number):
    if(move_number == 0):
        return ""
    moves = pgn_moves.split()
    spliced_moves = []

    for i in range(0, len(moves), 3):
        move_number -= 2
        if move_number == -1:
            break
        spliced_moves.extend(moves[i:i+3])
        if move_number == 0:
            spliced_moves = spliced_moves[:-1]
            break

    return ' '.join(spliced_moves)

json_output = []

for num_json in range(33):
    filename = f"puzzles_annot_{num_json}.json"
    
    if os.path.exists(filename):
        df = pd.read_json(filename, lines=True)
    else:
        print(f"File {filename} does not exist. Skipping.")
        continue
    for index, row in df.iterrows():
        #print(row["pgn"])
        move = int(row["GameUrl"].rsplit('#', 1)[-1])
        pgn_puzzle = splice_pgn_moves(row["pgn"], move)

        puzzle_pos, puzzle_sol = create_puzzles(pgn_puzzle, row["Moves"].split())
        cleaned_dict = {"PuzzleId": row["PuzzleId"], "GameURL": row["GameUrl"], "Rating": row["Rating"], "Popularity": row["Popularity"], "Themes": row["Themes"], "puzzle_input": puzzle_pos, "puzzle_solution": puzzle_sol}

        json_output.append(cleaned_dict)

with open("cleaned_chess_puzzles.json", 'w') as json_file:
    json.dump(json_output, json_file, indent=4)