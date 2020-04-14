import os
import flask
import chess
import random
import traceback
import json
import time

from flask import Flask, Response, request
from chess import Move
from state import Board
from player import Computer


app = Flask(__name__)


@app.route('/')
def hello():
    response = open('index.html').read()
    return response.replace('start', board.fen())


@app.route('/check_move')
def check_move():
    def parse_request(agrs):
        print(request.args)
        piece = request.args.get('piece')
        piece_color = piece[0]
        piece_type = piece[1]
        src = request.args.get('from', default='')
        dst = request.args.get('to', default='')
        promotion = request.args.get('promotion', default='')
        promotion = promotion if (dst[1]=='8' and piece_type=='P') else ''
        return piece_color, piece_type, src, dst, promotion

    piece_color, piece_type, src, dst, promotion = parse_request(request.args)
    move = Move.from_uci(src + dst + promotion)
    if piece_color != 'w' or move not in board.legal_moves:
        print('*'*20)
        print(list(board.legal_moves))
        print(move)
        print('*'*20, 'ilegal move')
        value = 'ilegal'
    else:
        value = 'legal'
        board.push(move)

    return json.dumps({'value':value, 'board':board.fen()})


@app.route('/move')
def move():
    move = computer.get_move(board)
    time.sleep(1)
    board.push(move)

    return json.dumps({'value':'done', 'board': board.fen()})
    for char in 'abcdefgh':
        try:
            board.push(Move.from_uci(f'{char}7{char}6'))
            print('moving')
            time.sleep(3)
            return json.dumps({'value':'done', 'board': board.fen()})
            return json.dumps({'value':'game over', 'board': 0})
        except:
            continue


@app.route('/newgame')
def new_game():
    board.reset()
    return board.fen()


if __name__ == '__main__':
    board = Board()
    computer = Computer()
    app.run(debug=True)
