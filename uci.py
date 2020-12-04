"""
Contains functions used to communicating with GUIs through UCI protocol

Documentation for the UCI protocol can be found at:
http://wbec-ridderkerk.nl/html/UCIProtocol.html
"""

import chess
import random
import engine
from itertools import takewhile, dropwhile


class UniversalChessInterface:
    def __init__(self, eng = None):
        if not eng:
            eng = engine.Engine()
        self._engine = eng 

    """
    [uci()] responds to the input "uci" from the GUI to establish 
    communication. The engine prints the engine name and engine author to the 
    GUI followed by uciok, as required by the UCI protocol. The engine name 
    corresponds is stored in the global variable [ENGINE] and the engine author 
    is stored in the global variable [AUTHOR].
    """
    def uci(self, options=None):
        print('id name {} {}'.format(self._engine.name(), self._engine.version()))
        print('id name {}'.format(self._engine._author()))
        #TODO deal with options here
        print('uciok')
    
    """
    [setoption(opt_str)] responds to the input "setoptiion" from the GUI, 
    indicating that the user would like to modify the internal parameters of the 
    engine.

    Parameter opt_str: the name and optionally a value for the option the user 
    would like to change
    Precondition: opt_str is a string, including the name of an option and 
    perhaps a value
    """
    def setoption(self, opt_str):
        #TODO set options here
        pass

    """
    [isready()] resonds to the input "isready" from the GUI. The engine prints 
    "readyok" to the GUI to communicate that it is ready to proceed.
    """
    def isready(self):
        print("readyok")

    """
    [ucinewgame()] responds to the input "ucinewgame" from the GUI, indicating 
    that the next search will be from a different game. The engine resets any of 
    its internal mechanisms that may need to be reset in order to consider a 
    different game.
    """
    def ucinewgame(self):
        self._engine.reset()

    
    """
    [position(pos_str)] responds to the input "position" from the GUI, 
    indicating that the engine should set up the position represented by [pos_str] 
    on its internal board. The position can either be set to the starting board or 
    a position represented by FEN notation, or kept the same as the current board 
    state. [pos_str] may also contain a series of moves in UCI notation which 
    is to be added on to the position.

    Parameter pos_str: the position that the engine's internal board should be set 
    to
    Precondition: pos_str is a string, starting with "starpos", "fen", or "moves". 
    """
    def position(self, pos_str):
        tokens = pos_str.split()
        moves = list(dropwhile(lambda token: token != 'moves', tokens))[1:]
        if tokens[0] == 'startpos':
            self._engine.setposition(moves=moves)
        elif tokens[0] == 'fen':
            fen = ' '.join(takewhile(lambda token: token != 'moves', tokens))
            self._engine.setposition(fen=fen, moves=moves)
    
        
        


    """
    [go()] responds to the input "go" from the GUI, indicating that the engine 
    should calculate the best move to make based on the current board state. The 
    engine responds with "bestmove" followed by the move in UCI notation, as 
    required by the UCI protocol.
    """
    def go(self, searchmoves = None, movetime = 10000, infinite = False):
        #TODO change "make_random move" to a smarter move generation function
        if searchmoves:
            print("searchmoves is unimplemented")
        if infinite:
            print("infinite is unimplemented")

        move = self._engine.best_move() 
        print("bestmove "+move)
        pass


    # """
    # [do_print()] prints the board state to the GUI. White pieces are represented 
    # by upper-case letters, and black pieces are represented by lower-case letters. 
    # This function is only used for debugging
    # """
    # def print(self):
    #     if (.turn):
    #         print("White to move:")
    #     else:
    #         print("Black to move:")
    #     print(BOARD)
        
    def run(self):
        while True:
            input_str = input()
            if (input_str == "uci"):
                self.uci()
            elif (input_str.startswith("setoption")):
                self.setoption(input_str[10:])
            elif (input_str == "isready"):
                self.isready()
            elif (input_str == "ucinewgame"):
                self.ucinewgame()
            elif (input_str.startswith("position")):
                self.position(input_str[9:])
            elif (input_str.startswith("go")):
                self.go()
            elif (input_str == "stop"):
                self._engine.stop()
            elif (input_str == "quit"):
                break
            else:
                print('invalid command')
            







