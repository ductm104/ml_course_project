import chess
import numpy as np
import random

from collections import defaultdict
from chess import Move
from valuator import Valuator


class Player:
    def __init__(self):
        pass


class Computer(Player):
    DEPTH = 2

    def __init__(self):
        super(Computer, self).__init__()
        self.valuator = Valuator()

    def __random_move(self, board):
        self.valuator(board)
        legal_moves = list(board.legal_moves)
        print(legal_moves)
        move = legal_moves[np.random.randint(len(legal_moves))]
        return move

    def __minimax(self, board, val='min', depth=0):
        if depth == 0:
            return self.valuator(board)

        values = []
        next_val = 'max' if val == 'min' else 'min'
        for move in board.legal_moves:
            board.push(move)
            values.append(self.__minimax(board, next_val, depth-1))
            board.pop()

        return np.min(values) if val=='min' else np.max(values)

    def __explore_leaves(self, board):
        values = defaultdict(list)
        for move in board.legal_moves:
            board.push(move)
            score = self.__minimax(board, val='min', depth=self.DEPTH)
            values[score].append(move.uci())
            board.pop()
        values = sorted(values.items())
        print(values)
        return Move.from_uci(random.choice(list(values)[0][1]))

    def __classic_move(self, board):
        return None

    def get_move(self, board):
        #move = self.__random_move(board)
        move = self.__explore_leaves(board)
        print('selected move:', move)
        return move


class Human(Player):
    def __init__(self):
        super(Human, self).__init()


if __name__ == '__main__':
    pass
