import chess
import numpy as np


class Board(chess.Board):
    WIN = {'1-0': 'You win!', '0-1': 'You lose!', '1/2-1/2': 'Draw'}
    def __init__(self):
        super().__init__()

    def who_win(self):
        if not self.is_game_over():
            return None

        res = self.result()
        return self.WIN[res]


if __name__ == '__main__':
    pass
