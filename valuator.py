import numpy as np
import chess

from collections import defaultdict
from state import Board


class Valuator:
    '''
    Squares tables: For white piece
    In the begining: white pieces at square 63->48
    '''
    pawn_values = [ 0,  0,  0,  0,  0,  0,  0,  0,
                   50, 50, 50, 50, 50, 50, 50, 50,
                   10, 10, 20, 30, 30, 20, 10, 10,
                    5,  5, 10, 25, 25, 10,  5,  5,
                    0,  0,  0, 20, 20,  0,  0,  0,
                    5, -5,-10,  0,  0,-10, -5,  5,
                    5, 10, 10,-20,-20, 10, 10,  5,
                    0,  0,  0,  0,  0,  0,  0,  0]

    knight_values =[-50,-40,-30,-30,-30,-30,-40,-50,
                    -40,-20,  0,  0,  0,  0,-20,-40,
                    -30,  0, 10, 15, 15, 10,  0,-30,
                    -30,  5, 15, 20, 20, 15,  5,-30,
                    -30,  0, 15, 20, 20, 15,  0,-30,
                    -30,  5, 10, 15, 15, 10,  5,-30,
                    -40,-20,  0,  5,  5,  0,-20,-40,
                    -50,-40,-30,-30,-30,-30,-40,-50]

    bishop_values =[-20,-10,-10,-10,-10,-10,-10,-20,
                    -10,  0,  0,  0,  0,  0,  0,-10,
                    -10,  0,  5, 10, 10,  5,  0,-10,
                    -10,  5,  5, 10, 10,  5,  5,-10,
                    -10,  0, 10, 10, 10, 10,  0,-10,
                    -10, 10, 10, 10, 10, 10, 10,-10,
                    -10,  5,  0,  0,  0,  0,  5,-10,
                    -20,-10,-10,-10,-10,-10,-10,-20]

    rook_values = [ 0,  0,  0,  0,  0,  0,  0,  0,
                    5, 10, 10, 10, 10, 10, 10,  5,
                   -5,  0,  0,  0,  0,  0,  0, -5,
                   -5,  0,  0,  0,  0,  0,  0, -5,
                   -5,  0,  0,  0,  0,  0,  0, -5,
                   -5,  0,  0,  0,  0,  0,  0, -5,
                   -5,  0,  0,  0,  0,  0,  0, -5,
                    0,  0,  0,  5,  5,  0,  0,  0]

    queen_values = [-20,-10,-10, -5, -5,-10,-10,-20,
                    -10,  0,  0,  0,  0,  0,  0,-10,
                    -10,  0,  5,  5,  5,  5,  0,-10,
                     -5,  0,  5,  5,  5,  5,  0, -5,
                      0,  0,  5,  5,  5,  5,  0, -5,
                    -10,  5,  5,  5,  5,  5,  0,-10,
                    -10,  0,  5,  0,  0,  0,  0,-10,
                    -20,-10,-10, -5, -5,-10,-10,-20]

    king_middle = [-30,-40,-40,-50,-50,-40,-40,-30,
                   -30,-40,-40,-50,-50,-40,-40,-30,
                   -30,-40,-40,-50,-50,-40,-40,-30,
                   -30,-40,-40,-50,-50,-40,-40,-30,
                   -20,-30,-30,-40,-40,-30,-30,-20,
                   -10,-20,-20,-20,-20,-20,-20,-10,
                    20, 20,  0,  0,  0,  0, 20, 20,
                    20, 30, 10,  0,  0, 10, 30, 20]

    king_endgame = [-50,-40,-30,-20,-20,-30,-40,-50,
                    -30,-20,-10,  0,  0,-10,-20,-30,
                    -30,-10, 20, 30, 30, 20,-10,-30,
                    -30,-10, 30, 40, 40, 30,-10,-30,
                    -30,-10, 30, 40, 40, 30,-10,-30,
                    -30,-10, 20, 30, 30, 20,-10,-30,
                    -30,-30,  0,  0,  0,  0,-30,-30,
                    -50,-30,-30,-30,-30,-30,-30,-50]

    king_values = king_middle.copy()

    def __init__(self):
        self.scores = {'p':-10, 'n':-20, 'r':-30, 'b':-50, 'q':-90, 'k':-100, \
                       'P':10, 'N':20, 'R':30, 'B':50, 'Q':90, 'K':100}

        self.scores = {'P':100, 'N':320, 'B':330, 'R':500, 'Q':900, 'K':20000, \
                       'p':-100, 'n':-320, 'b':-330, 'r':-500, 'q':-900, 'k':-20000}

        self.squares_table = defaultdict(list)
        self.squares_table['P'] = self.pawn_values
        self.squares_table['N'] = self.knight_values
        self.squares_table['R'] = self.rook_values
        self.squares_table['B'] = self.bishop_values
        self.squares_table['Q'] = self.queen_values
        self.squares_table['K'] = self.king_middle

    def __call__(self, board):
        #pieces = [self.scores[val.symbol()] for key, val in board.piece_map().items()]
        pieces = [(v.symbol(), k) for k, v in board.piece_map().items()]
        #print(pieces)

        valuesW = [self.scores[symb]*(1+self.squares_table[symb][63-pos]) \
                for symb, pos in pieces if symb in 'PNKQBR']
        valuesB = [self.scores[symb]*(1+self.squares_table[symb.upper()][pos]) \
                for symb, pos in pieces if symb in 'pnkqbr']

        return sum(valuesW) - sum(valuesB)


if __name__ == '__main__':
    val = Valuator()
    board = Board()
    print(val(board))
