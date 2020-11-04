"""
Contains various functions Manush can use to generate moves
"""

import chess
import random


"""
[make_random_move(board)] returns the UCI notation of a random legal move 
based on [board].

Parameter board: A representation of the board state to use to pick a move
Precondition: board is of type chess.Board
"""
def make_random_move(board):
    legal_moves = list(board.generate_legal_moves())
    move = random.choice(legal_moves)
    board.push(move)
    return move.uci()