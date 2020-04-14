import numpy as np


class Valuator:
    def __init__(self):
        self.scores = {'p':-10, 'n':-20, 'r':-30, 'b':-50, 'q':-90, 'k':-100, \
                       'P':10, 'N':20, 'R':30, 'B':50, 'Q':90, 'K':100}

    def __call__(self, board):
        pieces = [self.scores[val.symbol()] for key, val in board.piece_map().items()]
        return sum(pieces)


if __name__ == '__main__':
    val = Valuator()
