import os
import glob
import sys

import numpy as np
import chess.pgn


unit2index = {".": 0, "r": 1, "n": 2, "b": 3, "q": 4, "k": 5, "p": 6}
result2winner = {
    "1-0": "white",
    "1/2-1/2": "draw",
    "0-1": "black"
}
n_saved_files = 0 

def load_pgn_files(paths, savedir):
    for path in paths[::-1]:
        load_pgn_file(path, savedir)

def load_pgn_file(path, savedir):
    f = open(path)
    while True:
        game = chess.pgn.read_game(f)
        board = game.board()
        moves, result = parse_game(game, board)
        save_moves(moves, result, savedir)
        if game is None:
            break
    f.close()

def parse_game(game, board):
    moves = [board.__str__()]
    for move in game.mainline_moves():
        board.push(move)
        moves.append(board.__str__())
    moves = [parse_move(move) for move in moves]
    result = result2winner[game.headers["Result"]]
    return moves, result

def parse_move(move):
    move = [row.strip().replace(" ", "") for row in move.splitlines()]
    is_white = np.array([
        [int(unit.isupper()) for unit in row]
        for row in move
    ])
    is_black = np.array([
        [int(unit.islower()) for unit in row]
        for row in move
    ])
    units = np.array([
        [unit2index[unit.lower()] for unit in row]
        for row in move
    ])
    onehot_units = np.zeros((8, 8, 6))
    for idx in range(1, 7):
        onehot_units[units == idx, idx-1] = 1
    move = np.concatenate([
        onehot_units, is_white[..., None], is_black[..., None]
    ], axis=-1)
    return move

def save_moves(moves, result, savedir):
    global n_saved_files
    savedir = os.path.join(savedir, result)
    os.makedirs(savedir, exist_ok=True)
    for move in moves:
        np.save(os.path.join(savedir, str(n_saved_files)), move)
        n_saved_files += 1
    print(f"Number of saved files: {n_saved_files}")
    if n_saved_files >= 2e4:
        exit(0)
    return


if __name__ == "__main__":
    r"""Generate a dataset of 100,000 examples. Each of the form (move, result) where
        .move is a 8x8x8 array, i.e. 8x8x6 onehot chess-board encoding and 8x8x2 onehot player encoding
        .result is either "white", "draw", or "black", i.e. the winner of the game corresponding to the move
    """
    pgn_paths = glob.glob("/data.local/giangh/ml_course_project/reinforcement_learning/data/games/*.pgn")
    savedir = "/data.local/giangh/ml_course_project/reinforcement_learning/data/moves"
    load_pgn_files(pgn_paths, savedir)