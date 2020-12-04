import chess
from chess import Board
from eng_config import engine_config
import net_config
from game import Game, GameState
from agent import Agent
from model import Residual_CNN


class Engine:
    def __init__(self):
        self._config = engine_config
        self._game = Game()
        NN = Residual_CNN(net_config.REG_CONST, net_config.LEARNING_RATE, self._game.input_shape, self._game.action_size, net_config.HIDDEN_CNN_LAYERS)
        network = NN.read(self._game.name, run_version, player1version) #not sure what to put for [run_version] or [player1version]
        NN.model.set_weights(network.get_weights())   
        self._agent = Agent(self._config['NAME'], self._game.state_size, self._game.action_size, net_config.MCTS_SIMS, net_config.CPUCT, NN)
    
    def name(self):
        return self._config['NAME']

    def version(self):
        return self._config['VERSION']

    def author(self):
        return self._config['AUTHOR']

    def setposition(self, fen=None, moves=None):
        if fen:
            new_board = Board(fen)
        else:
            new_board = Board()
        if moves:
            for move in moves:
                new_board.push_uci(move)
        self._game.gameState = GameState(board=new_board)

    def best_move(self): 
        
        if self._game.gameState.board.fullmove_number < net_config.turns_until_tau0:
                action, _, _, _ = self._agent.act(self._game.gameState, 1)
        else:
            action, _, _, _ = self._agent.act(self._game.gameState, 0)
        
        from_square, to_square = divmod(action, 64)
        
        best = chess.Move(from_square=from_square, to_square=to_square).uci()

        self._game.step(action)

        return best

    def stop(self):
        pass

    def reset(self):
        self._agent.mcts = None
        self._game.reset()
    
    """
    minimax search of the game tree up to a depth of [depth], using evaluation 
    function [eval_func]. Includes alpha-beta pruning optimization
    """
    def minimax_search(self, depth, eval_func, player, board=_board, alpha=-1001, beta=1001, next=None):
        if (depth == 0 or board.is_game_over()):
            return eval_func(board), next
        if player:
            best_score = -1001
            for move in board.legal_moves:
                if next == None:
                    score, next_move = minimax_search(depth-1, eval_func, (not player), Board(board.fen()).push(move), alpha, beta, move)
                else:
                    score, next_move = minimax_search(depth-1, eval_func, (not player), Board(board.fen()).push(move), alpha, beta, next)
                if score > best_score:
                    best_score = score
                    best_move = next_move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            return best_score, best_move
        else:
            best_score = 1001
            for move in board.legal_moves:
                if next == None:
                    score, next_move = minimax_search(depth-1, eval_func, (not player), Board(board.fen()).push(move), alpha, beta, move)
                else:
                    score, next_move = minimax_search(depth-1, eval_func, (not player), Board(board.fen()).push(move), alpha, beta, next)
                if score < best_score:
                    best_score = score
                    best_move = next_move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score, best_move

    """
    Based on Claude Shannon's evaluation function created in 1949:
    f(board)=200(K-K')+9(Q-Q')+5(R-R')+3(B-B'+N-N')+(P-P')-.5(D-D'+S-S'+I-I')
    +.1(M-M')+...
    KQRBNP = pieces
    D = D,S,I = doubled, blocked and isolated pawns
    M = legal moves
    """
    def cs_eval(self, board):
        res = board.result()
        if res == "1-0":
            return 1000
        elif res == "0-1":
            return -1000
        elif res == "1/2-1/2":
            return 0

        else:
            score = 0
            for square in chess.SQUARES:
                piece = board.piece_at(square)
                if piece:
                    piece = piece.symbol()
                    if piece == "P":
                        score += 1
                        square_f = chess.square_file(square)
                        file = chess.FILE_NAMES[square_f]
                        doubled = False
                        for sq in chess.SquareSet.ray(chess.parse_square(file+"1"), chess.parse_square(file+"8")):
                            sq_piece = board.piece_at(sq)
                            if (chess.square_rank(sq) == chess.square_rank(square)+1) and sq_piece:
                                #is blocked pawn
                                score -= 0.5
                            if not doubled and sq_piece and sq_piece.symbol() == "P":
                                #is doubled pawn
                                score -= (0.25)
                                doubled = True
                        isolated = True
                        if file != "a":
                            left_file = chess.FILE_NAMES[square_f-1]
                            for sq in chess.SquareSet.ray(chess.parse_square(left_file+"1"), chess.parse_square(left_file+"8")):
                                sq_piece = board.piece_at(sq)
                                if sq_piece and sq_piece.symbol() == "P":
                                    isolated = False
                                    break
                        if file != "h" and isolated:
                            right_file = chess.FILE_NAMES[square_f+1]
                            for sq in chess.SquareSet.ray(chess.parse_square(right_file+"1"), chess.parse_square(right_file+"8")):
                                sq_piece = board.piece_at(sq)
                                if sq_piece and sq_piece.symbol() == "P":
                                    isolated = False
                                    break
                        if isolated:
                            score -= 0.5
                    elif piece == "p":
                        score -= 1
                        square_f = chess.square_file(square)
                        file = chess.FILE_NAMES[square_f]
                        doubled = False
                        for sq in chess.SquareSet.ray(chess.parse_square(file+"1"), chess.parse_square(file+"8")):
                            sq_piece = board.piece_at(sq)
                            if (chess.square_rank(sq) == chess.square_rank(square)-1) and sq_piece:
                                #is blocked pawn
                                score += 0.5
                            if not doubled and sq_piece and sq_piece.symbol() == "p":
                                #is doubled pawn
                                score += (0.25)
                                doubled = True
                        isolated = True
                        if file != "a":
                            left_file = chess.FILE_NAMES[square_f-1]
                            for sq in chess.SquareSet.ray(chess.parse_square(left_file+"1"), chess.parse_square(left_file+"8")):
                                sq_piece = board.piece_at(sq)
                                if sq_piece and sq_piece.symbol() == "p":
                                    isolated = False
                                    break
                        if file != "h" and isolated:
                            right_file = chess.FILE_NAMES[square_f+1]
                            for sq in chess.SquareSet.ray(chess.parse_square(right_file+"1"), chess.parse_square(right_file+"8")):
                                sq_piece = board.piece_at(sq)
                                if sq_piece and sq_piece.symbol() == "p":
                                    isolated = False
                                    break
                        if isolated:
                            score += 0.5
                    elif piece == "Q":
                        score += 9
                    elif piece == "q":
                        score -= 9
                    elif piece == "R":
                        score += 5
                    elif piece == "r":
                        score -= 5
                    elif piece == "N" or piece == "B":
                        score += 3
                    elif piece == "n" or piece == "b":
                        score -= 3
            
                if board.turn:
                    score += (0.1*len(board.legal_moves))
                    board.turn = (not board.turn)
                    score -= (0.1*len(board.legal_moves))
                else:
                    score -= (0.1*len(board.legal_moves))
                    board.turn = (not board.turn)
                    score += (0.1*len(board.legal_moves))
                board.turn = (not board.turn)

            return score 