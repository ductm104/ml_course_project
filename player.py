import chess
import numpy as np

from chess import Move


class Player:
    def __init__(self):
        pass


class Computer(Player):
    def __init__(self):
        super(Computer, self).__init__()

    def __random_move(self, board):
        legal_moves = list(board.legal_moves)
        print(legal_moves)
        move = legal_moves[np.random.randint(len(legal_moves))]
        return move

    def get_move(self, board):
        move = self.__random_move(board)
        print('selected move:', move)
        return move


class Human(Player):
    def __init__(self):
        super(Human, self).__init()


if __name__ == '__main__':
    pass
