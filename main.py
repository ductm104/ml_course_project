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


app = Flask(__name__)


@app.route('/')
def hello():
    response = open('index.html').read()
    return response.replace('start', board.fen())


@app.route('/check_move')
def check_move():
    piece = request.args.get('piece')
    piece_color = piece[0]
    piece_type = piece[1]
    src = request.args.get('from', default='')
    dst = request.args.get('to', default='')
    print(request.args)

    move = Move.from_uci(src + dst)
    if piece_color != 'w' or move not in board.legal_moves:
        value = 'ilegal'
    else:
        value = 'legal'
        board.push(move)

    return json.dumps({'value':value, 'board':board.fen()})


@app.route('/move')
def move():
    board.push(Move.from_uci('a7a6'))
    print('moving')
    time.sleep(3)
    #return json.dumps({'value':'done', 'board': board.fen()})
    return json.dumps({'value':'game over', 'board': 0})


@app.route('/newgame')
def new_game():
    board.reset()
    return board.fen()


if __name__ == '__main__':
    board = Board()
    app.run(debug=True)
