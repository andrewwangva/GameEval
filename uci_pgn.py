import chess
import chess.pgn
import io

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
        move_string += f"{move_number}."

    move_string += f" {pgn_move} "

    pgn_game += move_string

    return pgn_game

def create_puzzles(pgn_moves, UCI_moves):
    board = create_board_from_pgn_moves(pgn_moves)
    board_positions = []

    for i in range(len(UCI_moves)):
        parsed_move = chess.Move.from_uci(UCI_moves[i])
        pgn_move = board.san(parsed_move)

        pgn_moves = add_move(pgn_moves, pgn_move)
        
        if(i % 2 == 0):
            board_positions.append(pgn_moves)

    return board_positions

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

# Example PGN moves
pgn_moves = "1. d4 d5 2. Nc3 Bf5 3. f3 Nf6 4. Bf4 c6 5. g4 Bg6 6. h4 h6 7. h5 Bh7 8. Nh3 Nbd7 9. Bg2 Qb6 10. Rb1 e6 11. a3 c5 12. e3 cxd4 13. exd4 Rc8 14. O-O Bd6 15. Qd2 O-O 16. Na4 Qc7 17. Bxd6 Qxd6 18. Nc3 Nb6 19. Qf2 Nc4 20. g5 hxg5 21. Nxg5 Bf5 22. Qh4 Nd2 23. h6 Nxb1 24. Rxb1 Nh7 25. Bh3 Qe7 26. f4 Nxg5 27. fxg5 Bxh3 28. hxg7 Kxg7 29. Qh6+ Kg8 30. Qxh3"
UCI_moves = ["e7g5", "g1h1", "g5g6", "b1g1", "g8g7", "g1g6"]
print(UCI_moves)

print(splice_pgn_moves(pgn_moves, 2))



# Create a chess.Board object from PGN moves


#parsed_move = chess.Move.from_uci(UCI_moves[0])


#print(create_puzzles(pgn_moves, UCI_moves))

#pgn_move = board.san(parsed_move)
#print(pgn_move)
# Print the resulting board
