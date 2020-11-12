from chess import Board
from config import engine_config


class Engine:
    def __init__(self):
        self._board = Board()
        self._config = engine_config
    
    def name(self):
        return self._config['NAME']
    def version(self):
        return self._config['VERSION']
    def author(self):
        return self._config['AUTHOR']

    def setposition(self, fen=None, moves=None):
        if fen:
            self._board = Board(fen=fen)
        else:
            self._board = Board()
        if moves:
            for move in moves:
                self._board.push_uci(move)
    def best_move(self):
        pass
    def go(self, searchmoves = None, movetime = 10000, infinite = False):
        pass

    def stop(self):
        pass
    
        