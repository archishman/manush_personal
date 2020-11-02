import sys
import chess
import random

"""
Contains methods for Manush to play random moves, either against itself or 
against a human opponent through the terminal/command prompt

Can be run as a script with the following command in terminal/command prompt:
python manush_random.py [number of human players]
"""

def play_random_game(num_players):
    """
    Manush plays a game, always choosing random moves. If num_players == 0,
    Manush plays against itself. If num_players == 1, Manush plays against the 
    user.


    Parameter num_players: number of human players in the game
    Precondition: num_players is an int, either 0 or 1
    """
    board = chess.Board()
    if num_players == 0:
        play_cpu_random_vs_cpu_random(board)
    elif num_players == 1:
        play_human_vs_cpu_random(board)
    else:
        print("you can't play a game with "+str(num_players)+" human players")
    

def play_cpu_random_vs_cpu_random(board):
    """
    Manush plays a game against itself, always choosing random moves.
    
    Parameter board: the starting state of the board
    Precondition: board is of type chess.Board
    """
    while not board.is_game_over():
        legal_moves = list(board.generate_legal_moves())
        move = random.choice(legal_moves)
        print(board.san(move))
        board.push(move)
    print_game_result(board)


def play_human_vs_cpu_random(board):
    """
    Manush plays a game against the user, always choosing random moves

    Parameter board: the starting state of the board
    Precondition: board is of type chess.Board
    """
    player_color = int(input("What color would you like to play as? (White = 1; Black = 0): "))
    if (player_color == 1):
        print("You are playing as White")
    else:
        player_color = 0
        print("You are playing as Black")
    while not board.is_game_over():
        legal_moves = list(board.generate_legal_moves())
        if (board.turn == player_color):
            while True:
                try:
                    move = chess.Move.from_uci(input("Enter your move in uci format: "))
                    break
                except ValueError:
                    print("that is not uci format")
            while move not in legal_moves:
                while True:
                    try:
                        move = chess.Move.from_uci(input("That is not a legal move. Enter your move in uci format: "))
                        break
                    except ValueError:
                        print("that is not uci format")
            print("You played "+board.san(move))
        else:
            move = random.choice(legal_moves)
            print("Manush played "+board.san(move))
        board.push(move)
    print_game_result(board)


def print_game_result(board):
    """
    Prints the game result to the console

    Parameter board: The current board state
    Precondition: board is of type chess.Board and represents a completed 
    game
    """
    print(board.result())
    if board.is_stalemate():
        print("stalemate")
    elif board.is_insufficient_material():
        print("insufficient material")
    elif board.is_seventyfive_moves():
        print("seventy-five moves")
    elif board.is_fivefold_repetition():
        print("five-fold repetition")

if __name__ == "__main__":
    play_random_game(int(sys.argv[1]))
