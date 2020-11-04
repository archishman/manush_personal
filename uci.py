"""
Contains functions used to communicating with GUIs through UCI protocol

Documentation for the UCI protocol can be found at:
http://wbec-ridderkerk.nl/html/UCIProtocol.html
"""

import chess
import random
import move_gen


"""
[ENGINE_NAME] is the name of the engine

Precondition: [ENGINE_NAME] is a string
"""
ENGINE_NAME = "Manush v0"


"""
[AUTHOR] is the name of the author of the engine

Precondition: [AUTHOR] is a string
"""
AUTHOR = "Thomas Koconis and Archie Sravankumar"


"""
[BOARD] is a representation of the current state of the board

Precondition: [BOARD] is of type chess.Board if a position has been set; 
otherwise [BOARD] is None
"""
BOARD = None


"""
[uci_communication()] takes input from the GUI and calls the appropriate 
function in response.
"""
def uci_communication():
    while True:
        input_str = input()
        if (input_str == "uci"):
            do_uci()
        elif (input_str.startswith("setoption")):
            do_setoption(input_str[10:])
        elif (input_str == "isready"):
            do_isready()
        elif (input_str == "ucinewgame"):
            do_ucinewgame()
        elif (input_str.startswith("position")):
            do_position(input_str[9:])
        elif (input_str.startswith("go")):
            do_go()
        elif (input_str == "print"):
            do_print()


"""
[do_uci()] responds to the input "uci" from the GUI to establish 
communication. The engine prints the engine name and engine author to the 
GUI followed by uciok, as required by the UCI protocol. The engine name 
corresponds is stored in the global variable [ENGINE] and the engine author 
is stored in the global variable [AUTHOR].
"""
def do_uci():
    print("id name "+ENGINE_NAME)
    print("id author "+AUTHOR)
    #TODO deal with options here
    print("uciok")


"""
[do_setoption(opt_str)] responds to the input "setoptiion" from the GUI, 
indicating that the user would like to modify the internal parameters of the 
engine.

Parameter opt_str: the name and optionally a value for the option the user 
would like to change
Precondition: opt_str is a string, including the name of an option and 
perhaps a value
"""
def do_setoption(opt_str):
    #TODO set options here
    pass


"""
[do_isready()] resonds to the input "isready" from the GUI. The engine prints 
"readyok" to the GUI to communicate that it is ready to proceed.
"""
def do_isready():
    print("readyok")


"""
[do_ucinewgame()] responds to the input "ucinewgame" from the GUI, indicating 
that the next search will be from a different game. The engine resets any of 
its internal mechanisms that may need to be reset in order to consider a 
different game.
"""
def do_ucinewgame():
    #TODO
    pass


"""
[do_position(pos_str)] responds to the input "position" from the GUI, 
indicating that the engine should set up the position represented by [pos_str] 
on its internal board. The position can either be set to the starting board or 
a position represented by FEN notation, or kept the same as the current board 
state. [pos_str] may also contain a series of moves in UCI notation which 
is to be added on to the position.

Parameter pos_str: the position that the engine's internal board should be set 
to
Precondition: pos_str is a string, starting with "starpos", "fen", or "moves". 
"""
def do_position(pos_str):
    moves_str = pos_str
    global BOARD
    if (pos_str.startswith("startpos")):
        BOARD = chess.Board()
    elif (pos_str.startswith("fen")):
        if (moves_str.count("moves") == 1):
            BOARD = chess.Board(moves_str[4:moves_str.index("moves")-1])
        else:
            manush.BOARD = chess.Board(moves_str)
    if (moves_str.count("moves") == 1):
        moves_str = moves_str[moves_str.index("moves")+6:]
        moves_lst = moves_str.split()
        for m in moves_lst:
            BOARD.push_uci(m)


"""
[do_go()] responds to the input "go" from the GUI, indicating that the engine 
should calculate the best move to make based on the current board state. The 
engine responds with "bestmove" followed by the move in UCI notation, as 
required by the UCI protocol.
"""
def do_go():
    #TODO change "make_random move" to a smarter move generation function
    move = move_gen.make_random_move(BOARD) 
    print("bestmove "+move)
    pass


"""
[do_print()] prints the board state to the GUI. White pieces are represented 
by upper-case letters, and black pieces are represented by lower-case letters. 
This function is only used for debugging
"""
def do_print():
    if (BOARD.turn):
        print("White to move:")
    else:
        print("Black to move:")
    print(BOARD)