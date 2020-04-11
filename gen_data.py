import os
import chess.pgn
import numpy as np

#from state import State

valid_results = {'1/2-1/2':0, '0-1':-1, '1-0':1}


def get_data_from_pgn(num_samples=1):
    num_games = 0
    X, Y = [], []
    for path in os.listdir("dataset"):
        if path[-4:] == ".pgn":
            if "small" not in path:
                continue

            print("Parsing from file: ", path)
            file = open(os.path.join("dataset", path))

            num_games += 1
            while True:
                game = chess.pgn.read_game(file)
                if game is None: break

                result = game.headers['Result']
                if result not in valid_results:
                    continue

                result = valid_results[result]

                board = game.board()
                for move in game.mainline_moves():
                    board.push(move)

                print(f"Parsing game {num_games}, got {len(Y)} examples")
                break

    return 0, 1


if __name__ == '__main__':
    X, Y = get_data_from_pgn()
    print(X)
    print(Y)
