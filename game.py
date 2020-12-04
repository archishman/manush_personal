import numpy as np
import logging
from chess import Board
import chess
from itertools import product
class Game:

    def __init__(self):        
        self.currentPlayer = 1
        self.gameState = GameState()
        self.actionSpace = list(product(range(64), range(64)))
        self.pieces = {'1':'W', '0': '-', '-1':'B'}
        self.grid_shape = (8,8)
        self.input_shape = (20,8,8)
        self.name = 'chess'
        self.state_size = np.prod(self.gameState.binary.shape)
        self.action_size = 64 * 72

    
    def reset(self):
        self.gameState = GameState()
        self.currentPlayer = 1
        return self.gameState

    def step(self, action):
        next_state, value, done = self.gameState.takeAction(action)
        self.gameState = next_state
        self.currentPlayer = -self.currentPlayer
        info = None
        return ((next_state, value, done, info))

    def identities(self, state, actionValues):
        identities = [(state,actionValues)]
        return identities


class GameState():
    def __init__(self, board = None):
        if not board:
            self.board = Board()
        else:
            self.board = board
        self.pieces = {'1':'W', '0': '-', '-1':'B'}
        self.playerTurn = 1 if self.board.turn else -1
        self.binary = self._binary()
        self.id = self.board.fen()
        self.allowedActions = self._allowedActions()
        self.isEndGame = self._checkForEndGame()
        self.value = self._getValue()
        self.score = self._getScore()

    def _allowedActions(self):
        allowedActions = [self._moveToAction(move) 
            for move 
            in self.board.legal_moves]
        return allowedActions

    def _binary(self):
        pieces = list(product(
            [chess.WHITE, chess.BLACK], 
            range(chess.PAWN, chess.KING + 1)))
        layers = []
        board = self.board if self.board.turn else self.board.mirror()        
        for col, typ in pieces:
            piece_position_lst = board.pieces(typ, col).tolist()
            piece_position_array = np.reshape(np.array(piece_position_lst), (8,8)).astype(np.uint8)
            layers.append(piece_position_array)

        turn = np.ones((8,8)) * self.board.turn 
        move_count = np.ones((8,8)) * self.board.fullmove_number
        no_progress = np.ones((8,8)) * self.board.halfmove_clock
        p1_k_castle = np.ones((8,8)) * self.board.has_kingside_castling_rights(chess.WHITE)
        p1_q_castle = np.ones((8,8)) * self.board.has_queenside_castling_rights(chess.WHITE)
        p2_k_castle = np.ones((8,8)) * self.board.has_kingside_castling_rights(chess.BLACK)
        p2_q_castle = np.ones((8,8)) * self.board.has_queenside_castling_rights(chess.BLACK)
        repetition = np.ones((8,8)) * True #self.board.can_claim_threefold_repetition() #only way I could think of to track 3-fold repetition, quite slow
        layers.extend([turn, move_count, no_progress, p1_k_castle, 
            p1_q_castle, p2_k_castle, p2_q_castle, repetition])
        return np.stack(layers, axis=0)

    def _convertStateToId(self):
        return self.board.fen()

    def _checkForEndGame(self):
        return self.board.is_game_over(claim_draw=True)


    def _getValue(self):
        # This is the value of the state for the current player
        # i.e. if the previous player played a winning move, you lose
        result = self.board.mirror().result()
        if result == '1/2-1/2':
            return (0.5, 0.5, 0.5)
        elif result == '1-0':
            return (1,1,1)
        elif result == '0-1': 
            return (-1,-1,-1)
        else:
            return (0,0,0)
        


    def _getScore(self):
        tmp = self.value
        return (tmp[1], tmp[2])

    def _promotionToAction(self, move):
        start_file = chess.square_file(move.from_square)
        end_file = chess.square_file(move.to_square)
        piece = move.promotion - chess.KNIGHT
        if chess.square_rank(move.to_square) == 0:
            piece += 4
        return 64*64 + piece * 64 + start_file * 8 + end_file
    def _actionToPromotion(self, action):
        p, f = divmod(action - 64*64, 64)
        start_file, end_file = divmod(f, 8)
        if p < 4:
            piece = chess.KNIGHT + p
            from_square = chess.A7 + start_file
            to_square = chess.A8 + end_file
        else:
            piece = chess.KNIGHT + p - 4
            from_square = chess.A2 + start_file
            to_square = chess.A1 + end_file
        return chess.Move(from_square, to_square, piece)        
    def _actionToMove(self, action):
        num_regular_moves = 64*64
        num_white_promotions = 8*4
        num_black_promotions = 8*4
        if action < num_regular_moves:
            from_square, to_square = divmod(action, 64)
            return chess.Move(from_square=from_square, to_square=to_square)
        else:
            return self._actionToPromotion(action)

    def _moveToAction(self, move):
        if move.promotion:
            return self._promotionToAction(move)
        return move.from_square * 64 +  move.to_square


    def takeAction(self, action):
        move = self._actionToMove(action)
        newBoard = self.board.copy()
        newBoard.push(move)        
        newState = GameState(board=newBoard)
        value = 0
        done = 0

        if newState.isEndGame:
            value = newState.value[0]
            done = 1

        return (newState, value, done) 




    def render(self, logger):
        for r in range(6):
            logger.info(self.board.fen())
        logger.info('--------------')