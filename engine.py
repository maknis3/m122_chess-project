import pygame
import sys
import copy
from collections import Counter
from board import Board
from pieces import ChessPiece, Color, Piece
from chess import Chess

PIECE_WORTH = {
    Piece.PAWN.value: 1,
    Piece.BISHOP.value: 3,
    Piece.KNIGHT.value: 3,
    Piece.ROOK.value: 5,
    Piece.QUEEN.value: 7,
    Piece.KING.value: 0
}

PAWN_POS_WEIGHT = 3
BISHOP_POS_WEIGHT = 1
KNIGHT_POS_WEIGHT = 2
ROOK_POS_WEIGHT = 1
QUEEN_POS_WEIGHT = 1
KING_POS_WEIGHT = 2
IN_CHECK_BONUS = 2

PAWN_POS_BONUS = {
    Color.WHITE.value: 
    [
        [0.8, 0.8, 0.9, 1.0, 1.0, 0.9, 0.8, 0.8],
        [0.7, 0.7, 0.8, 0.8, 0.8, 0.8, 0.7, 0.7],
        [0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 0.6, 0.6],
        [0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.5, 0.5],
        [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4],
        [0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3],
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1] 
    ],
    Color.BLACK.value:
    [
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        [0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3],
        [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4],
        [0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.5, 0.5],
        [0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 0.6, 0.6],
        [0.7, 0.7, 0.8, 0.8, 0.8, 0.8, 0.7, 0.7],
        [0.8, 0.8, 0.9, 1.0, 1.0, 0.9, 0.8, 0.8] 
    ]
}
KNIGHT_POS_BONUS = [
    [0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.3, 0.5, 0.6, 0.6, 0.6, 0.6, 0.5, 0.3],
    [0.3, 0.5, 0.6, 0.7, 0.7, 0.6, 0.5, 0.3],
    [0.3, 0.5, 0.6, 0.7, 0.7, 0.6, 0.5, 0.3],
    [0.3, 0.5, 0.6, 0.6, 0.6, 0.6, 0.5, 0.3],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2] 
]
BISHOP_POS_BONUS = [
    [0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4],
    [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.3, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.3],
    [0.3, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.3],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
    [0.4, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4]
]
QUEEN_POS_BONUS = [
    [0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2],
    [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.3, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.3],
    [0.3, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.3],
    [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
    [0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.3],
    [0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2]
]
ROOK_POS_BONUS = []
KING_POS_BONUS_OPENING = {
    Color.WHITE.value: 
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        [0.3, 0.4, 0.3, 0.2, 0.2, 0.3, 0.4, 0.3],
        [0.6, 0.7, 0.9, 0.6, 0.5, 0.6, 0.9, 0.7]
    ],
    Color.BLACK.value: 
    [
        [0.6, 0.7, 0.9, 0.6, 0.5, 0.6, 0.9, 0.7],
        [0.3, 0.4, 0.3, 0.2, 0.2, 0.3, 0.4, 0.3],
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    }
KING_POS_BONUS_ENDGAME = {
    Color.WHITE.value: 
    [
        [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1],
        [0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3],
        [0.4, 0.5, 0.6, 0.7, 0.7, 0.6, 0.4, 0.5],
        [0.4, 0.6, 0.7, 0.8, 0.8, 0.7, 0.4, 0.6],
        [0.3, 0.5, 0.7, 0.8, 0.8, 0.7, 0.3, 0.5],
        [0.2, 0.4, 0.6, 0.7, 0.7, 0.6, 0.2, 0.4],
        [0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2],
        [0, 0, 0, 0.1, 0.1, 0, 0, 0]
    ],
    Color.BLACK.value: 
    [
        [0, 0, 0, 0.1, 0.1, 0, 0, 0],
        [0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2],
        [0.2, 0.4, 0.6, 0.7, 0.7, 0.6, 0.2, 0.4],
        [0.3, 0.5, 0.7, 0.8, 0.8, 0.7, 0.3, 0.5],
        [0.4, 0.6, 0.7, 0.8, 0.8, 0.7, 0.4, 0.6],
        [0.4, 0.5, 0.6, 0.7, 0.7, 0.6, 0.4, 0.5],
        [0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.3],
        [0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1]
    ]
}



class ChessEngine:
    def __init__(self, chess):
        self.chess = chess
    
    def calculate_move(self, initial_board_matrix, en_passant_square, move_counter):
        temp_board = copy.deepcopy(initial_board_matrix)
        promotion_piece = None
        best_promotion_piece = ChessPiece.QUEEN_BLACK
        possible_moves = []
        best_move_eval = -100000
        from_best_move = None
        to_best_move = None
        
        
        for r in range(8):
            for c in range(8):
                if self.chess.is_valid_square((r, c), initial_board_matrix, Color.BLACK):
                    for move in self.chess.calculate_possible_moves((r, c), initial_board_matrix, en_passant_square, Color.BLACK):
                        if (move[0] == 7 and self.chess.get_piece((r, c), temp_board) == ChessPiece.PAWN_BLACK):
                            for promotion_piece in (ChessPiece.ROOK_BLACK, ChessPiece.KNIGHT_BLACK, ChessPiece.BISHOP_BLACK, ChessPiece.QUEEN_BLACK):
                                temp_board = copy.deepcopy(initial_board_matrix)
                                temp_board, en_passant_square = self.chess.move_piece((r, c), move, temp_board, en_passant_square, Color.BLACK, promotion_piece)
                                new_eval =  self.minimax(temp_board, en_passant_square, promotion_piece, 1, -10000, 10000, False, move_counter + 1)
                                if new_eval > best_move_eval:
                                    from_best_move = (r, c)
                                    to_best_move = move
                                    best_promotion_piece = promotion_piece
                            continue
                        temp_board = copy.deepcopy(initial_board_matrix)
                        temp_board, en_passant_square = self.chess.move_piece((r, c), move, temp_board, en_passant_square, Color.BLACK)
                        new_eval =  self.minimax(temp_board, en_passant_square, 1, -10000, 10000, False, move_counter + 1)
                        if new_eval > best_move_eval:
                            from_best_move = (r, c)
                            to_best_move = move
                            best_move_eval = new_eval
    
        return from_best_move, to_best_move, best_promotion_piece
    
    def evaluate(self, board_matrix, player, move_counter, en_passant_square):
        evaluation = 0
        if self.chess.is_checkmate(board_matrix, en_passant_square, player):
            return -100000
        if self.chess.is_checkmate(board_matrix, en_passant_square, Color.WHITE if player == Color.BLACK else Color.BLACK):
            return 100000
        
        for r in range(8):
            for c in range(8):
                piece = self.chess.get_piece((r, c), board_matrix)
                if piece == ChessPiece.EMPTY:
                    continue
                if piece.value[1] == Piece.PAWN.value:
                    temp_eval = PIECE_WORTH[Piece.PAWN.value]
                    temp_eval += PAWN_POS_WEIGHT * PAWN_POS_BONUS[piece.value[0]][r][c]
                if piece.value[1] == Piece.BISHOP.value:
                    temp_eval = PIECE_WORTH[Piece.BISHOP.value]
                    temp_eval += BISHOP_POS_WEIGHT * BISHOP_POS_BONUS[r][c]
                if piece.value[1] == Piece.KNIGHT.value:
                    temp_eval = PIECE_WORTH[Piece.KNIGHT.value]
                    temp_eval += KNIGHT_POS_WEIGHT * KNIGHT_POS_BONUS[r][c]
                if piece.value[1] == Piece.ROOK.value:
                    temp_eval = PIECE_WORTH[Piece.ROOK.value]
                if piece.value[1] == Piece.QUEEN.value:
                    temp_eval = PIECE_WORTH[Piece.QUEEN.value]
                    temp_eval += QUEEN_POS_WEIGHT * QUEEN_POS_BONUS[r][c]
                if piece.value[1] == Piece.KING.value:
                    if move_counter < 80:
                        temp_eval = KING_POS_WEIGHT * KING_POS_BONUS_OPENING[piece.value[0]][r][c]
                    else:
                        temp_eval = KING_POS_WEIGHT * KING_POS_BONUS_ENDGAME[piece.value[0]][r][c]
                evaluation += temp_eval if piece.value[0] == player.value else - temp_eval
                
        if self.chess.is_in_check(board_matrix, player):
            evaluation += IN_CHECK_BONUS
        if self.chess.is_in_check(board_matrix, Color.WHITE if player == Color.BLACK else Color.BLACK):
            evaluation += IN_CHECK_BONUS

        return evaluation
                
    def minimax(self, board_matrix, en_passant_square, depth, alpha, beta, maximazingPlayer, move_counter):
        temp_board = copy.deepcopy(board_matrix)
        if depth == 0 or self.chess.is_checkmate(temp_board, en_passant_square, Color.BLACK if maximazingPlayer else Color.WHITE):
            return self.evaluate(temp_board, Color.BLACK if maximazingPlayer else Color.WHITE, move_counter, en_passant_square)
        
        if maximazingPlayer:
            maxEval = -10000
            for r in range(8):
                for c in range(8):
                    if self.chess.is_valid_square((r, c), temp_board, Color.BLACK):
                        possible_moves = self.chess.calculate_possible_moves((r, c), temp_board, en_passant_square, Color.BLACK)
                        for move in possible_moves:
                            if (move[0] == 7 and self.chess.get_piece((r, c), temp_board) == ChessPiece.PAWN_BLACK):
                                for promotion_piece in (ChessPiece.ROOK_BLACK, ChessPiece.KNIGHT_BLACK, ChessPiece.BISHOP_BLACK, ChessPiece.QUEEN_BLACK):
                                    temp_board, en_passant_square = self.chess.move_piece((r, c), move, temp_board, en_passant_square, Color.BLACK, promotion_piece)
                                    eval = self.minimax(temp_board, en_passant_square, depth -1, alpha, beta, False, move_counter + 1)
                                    maxEval = max(maxEval, eval)
                                    alpha = max(alpha, eval)
                                    if beta <= alpha:
                                        break
                                continue
                            temp_board, en_passant_square = self.chess.move_piece((r, c), move, temp_board, en_passant_square, Color.BLACK)
                            eval = self.minimax(temp_board, en_passant_square, depth -1, alpha, beta, False, move_counter + 1)
                            maxEval = max(maxEval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
                        
            return maxEval
        else:
            minEval = 10000
            for r in range(8):
                for c in range(8):
                    if self.chess.is_valid_square((r, c), temp_board, Color.WHITE):
                        possible_moves = self.chess.calculate_possible_moves((r, c), temp_board, en_passant_square, Color.WHITE)
                        for move in possible_moves:
                            if (move[0] == 7 and self.chess.get_piece((r, c), temp_board) == ChessPiece.PAWN_WHITE):
                                for promotion_piece in (ChessPiece.ROOK_WHITE, ChessPiece.KNIGHT_WHITE, ChessPiece.BISHOP_WHITE, ChessPiece.QUEEN_WHITE):
                                    temp_board, en_passant_square = self.chess.move_piece((r, c), move, temp_board, en_passant_square, Color.WHITE, promotion_piece)
                                    eval = self.minimax(temp_board, en_passant_square, depth -1, alpha, beta, True, move_counter + 1)
                                    minEval = min(minEval, eval)
                                    beta = min(beta, eval)
                                    if beta <= alpha:
                                        break
                                continue
                            temp_board, en_passant_square = self.chess.move_piece((r, c), move, temp_board, en_passant_square, Color.WHITE)
                            eval = self.minimax(temp_board, en_passant_square, depth -1, alpha, beta, True, move_counter + 1)
                            minEval = min(minEval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
            return minEval

             
                