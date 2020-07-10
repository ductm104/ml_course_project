import chess
import numpy as np
import random
import time

from collections import defaultdict
from chess import Move
from valuator import Valuator
from deep_valuator import DeepValuator


class Player:
    def __init__(self):
        pass


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(f'Enlapsed time {method.__name__}: {te-ts}')
        return result
    return timed


class Computer(Player):
    DEPTH = 3
    MAX_VAL = 1e12

    def __init__(self):
        super(Computer, self).__init__()
        self.valuator = DeepValuator(
            "/data.local/giangh/ml_course_project/reinforcement_learning/ckpt/0.5040.pth", 
            "cpu"
        )

    def __random_move(self, board):
        self.valuator(board)
        legal_moves = list(board.legal_moves)
        print(legal_moves)
        move = legal_moves[np.random.randint(len(legal_moves))]
        return move

    def __minimax(self, board, is_min=True, depth=0):
        if depth == 0:
            return self.valuator(board)

        if is_min:
            value = self.MAX_VAL
            for move in board.legal_moves:
                board.push(move)
                value = min(value, self.__minimax(board, False, depth-1))
                board.pop()
        else:
            value = -self.MAX_VAL
            for move in board.legal_moves:
                board.push(move)
                value = max(value, self.__minimax(board, True, depth-1))
                board.pop()

        return value

        #not enough space for bigger depth value
        #values = []
        #for move in board.legal_moves:
        #    board.push(move)
        #    values.append(self.__minimax(board, not is_min, depth-1))
        #    board.pop()

        #return np.min(values) if is_min else np.max(values)

    def __alpha_beta(self, board, alpha, beta, is_min=True, depth=0):
        if depth == 0:
            return self.valuator(board)

        if is_min:
            value = self.MAX_VAL
            for move in board.legal_moves:
                board.push(move)
                value = min(value, self.__alpha_beta(board, alpha, beta, False, depth-1))
                board.pop()
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            value = -self.MAX_VAL
            for move in board.legal_moves:
                board.push(move)
                value = max(value, self.__alpha_beta(board, alpha, beta, True, depth-1))
                board.pop()
                beta = min(beta, value)
                if alpha >= beta:
                    break

        return value

    @timeit
    def __explore_leaves(self, board):
        values = defaultdict(list)
        for move in board.legal_moves:
            board.push(move)
            #score = self.__minimax(board, False, self.DEPTH)
            score = self.__alpha_beta(board, -self.MAX_VAL, self.MAX_VAL, False, self.DEPTH)
            values[score].append(move.uci())
            board.pop()
        values = sorted(values.items())
        print(values)
        return Move.from_uci(random.choice(values[0][1]))

    def get_move(self, board):
        #move = self.__random_move(board)
        move = self.__explore_leaves(board)
        print('Selected move:', move)
        return move


class Human(Player):
    def __init__(self):
        super(Human, self).__init()


if __name__ == '__main__':
    pass
