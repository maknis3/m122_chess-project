import pygame
import sys
import copy
from collections import Counter
from board import Board
from pieces import ChessPiece, Color
from chess import Chess

PIECE_WORTH = {
    ChessPiece.EMPTY: 0,
    ChessPiece.PAWN_BLACK: 1,
    ChessPiece.PAWN_WHITE: 1,
    ChessPiece.ROOK_BLACK: 5,
    ChessPiece.ROOK_WHITE: 5,
    ChessPiece.KNIGHT_BLACK: 3,
    ChessPiece.KNIGHT_WHITE: 3,
    ChessPiece.BISHOP_BLACK: 3,
    ChessPiece.BISHOP_WHITE: 3,
    ChessPiece.QUEEN_BLACK: 7,
    ChessPiece.QUEEN_WHITE: 7
}

class ChessEngine:
    def __init__(self, chess):
        self.chess = chess
    
    def calculate_move(self, initial_board_matrix, en_passant_square):
        temp_board = copy.deepcopy(initial_board_matrix)
        promotion_piece = None
        best_promotion_piece = None
        possible_moves = []
        best_move_eval = -100000
        from_best_move = None
        to_best_move = None
        
        
        for r in range(8):
            for c in range(8):
                if self.chess.is_valid_square((r, c), temp_board, Color.BLACK):
                    possible_moves = self.chess.calculate_possible_moves((r, c), temp_board, en_passant_square, Color.BLACK)
                    for move in possible_moves:
                        if (move[0] == 7 and self.chess.get_piece((r, c), temp_board) == ChessPiece.PAWN_BLACK):
                            for promotion_piece in (ChessPiece.ROOK_BLACK, ChessPiece.KNIGHT_BLACK, ChessPiece.BISHOP_BLACK, ChessPiece.QUEEN_BLACK):
                                new_eval =  self.minimax(temp_board, en_passant_square, promotion_piece, 4, -10000, 10000, True)
                                if new_eval > best_move_eval:
                                    from_best_move = (r, c)
                                    to_best_move = move
                                    best_promotion_piece = promotion_piece
                        new_eval =  self.minimax(temp_board, en_passant_square, promotion_piece, 4, -10000, 10000, True)
                        if new_eval > best_move_eval:
                            from_best_move = (r, c)
                            to_best_move = move
    
        return from_best_move, to_best_move, best_promotion_piece
    
    def evaluate(self, board_matrix, color):
        evaluation = 0
        for r in range(8):
            for c in range(8):
                piece = self.chess.get_piece((r, c), board_matrix)
                evaluation += PIECE_WORTH[piece] * 1 if piece.value[0] == color else -1
        return evaluation
                
    def minimax(self, board_matrix, en_passant_square, promotion_piece, depth, alpha, beta, maximazingPlayer):
        temp_board = copy.deepcopy(board_matrix)
        
        if depth == 0 or self.chess.is_checkmate(temp_board, en_passant_square, Color.BLACK if maximazingPlayer else Color.WHITE):
            return self.evaluate(temp_board, Color.BLACK if maximazingPlayer else Color.WHITE)
        
        if maximazingPlayer:
            maxEval = -10000
            for r in range(8):
                for c in range(8):
                    piece = self.chess.get_piece((r, c), temp_board)
                    if (piece == ChessPiece.EMPTY) or (piece.value[0] == Color.BLACK):
                        continue
                    for move in self.chess.calculate_possible_moves((r, c), temp_board, en_passant_square, Color.BLACK):
                        temp_board, en_passant_square = self.chess.move_piece((r, c), move, temp_board, en_passant_square, Color.BLACK, promotion_piece)
                        eval = self.minimax(temp_board, en_passant_square, promotion_piece, depth -1, alpha, beta, False)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
                    return maxEval
        else:
            minEval = 10000
            for r in range(8):
                for c in range(8):
                    piece = self.chess.get_piece((r, c), temp_board)
                    if (piece == ChessPiece.EMPTY) or (piece.value[0] == Color.WHITE):
                        continue
                    for move in self.chess.calculate_possible_moves((r, c), temp_board, en_passant_square, Color.WHITE):
                        temp_board, en_passant_square = self.chess.move_piece((r, c), move, temp_board, en_passant_square, Color.BLACK, promotion_piece)
                        eval = self.minimax(temp_board, en_passant_square, promotion_piece, depth -1, alpha, beta, False)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
                    return minEval

             
                