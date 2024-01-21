import pygame
import sys
import math
import functools
from collections import Counter
from board import Board

class Chess:
    def __init__(self, board):
        self.board = board
        self.hash_board_archive = []
        self.board_archive = []
        self.possible_moves_cache = {}
    
    def is_empty_position(self, board_matrix, position):
        return (board_matrix["all_pieces"] & position) == 0
    
    @functools.cache
    def square_to_position(self, square): # Convert a square (row, col) to a position (bit index)
        return 1 << (square[0] * 8 + square[1])

    @functools.cache
    def position_to_square(self, position): # Convert a position (bit index) to a square (row, col)
        return int(math.log(position, 2) // 8), int(math.log(position, 2) % 8)
    
    def identify_piece(self, position, board_matrix):
        if (board_matrix["all_pieces"] & position) == 0:
            return None, None
        for piece, piece_position in board_matrix.items():
            if piece in ("casteling_rights", "en_passant_position", "last_capture_or_pawn_move", "all_pieces"):
                continue
            if (piece_position & position) == position:
                return piece.split('_')
        return None, None

    def calculate_possible_moves(self, board_matrix, position):
        hashed_move = hash(str(board_matrix) + str(position))
        if (hashed_move) in self.possible_moves_cache:
            return self.possible_moves_cache[hashed_move]
        
        piece_type, piece_color = self.identify_piece(position, board_matrix)
        moves = []

        if piece_type:
            if piece_type == "PAWN":
                moves += self.calculate_pawn_moves(piece_color, position, board_matrix)
            elif piece_type == "ROOK":
                moves += self.calculate_rook_moves(piece_color, position, board_matrix)
            elif piece_type == "BISHOP":
                moves += self.calculate_bishop_moves(piece_color, position, board_matrix)
            elif piece_type == "KNIGHT":
                moves += self.calculate_knight_moves(piece_color, position, board_matrix)
            elif piece_type == "QUEEN":
                moves += self.calculate_queen_moves(piece_color, position, board_matrix)
            elif piece_type == "KING":
                moves += self.calculate_king_moves(piece_color, position, board_matrix)
        
        filtered_moves = list(filter(lambda move: not self.move_will_cause_check(piece_color, board_matrix, position, move), moves))
        self.possible_moves_cache[hashed_move] = filtered_moves

        return filtered_moves

    def calculate_pawn_moves(self, piece_color, position, board_matrix, only_impact = False):
        
        moves = []
        direction = False if piece_color=="WHITE" else True
        
        if only_impact:
            for delta_col in [9, 7]:
                capture_position = (position << delta_col) if direction else (position >> delta_col)
                if abs(int(math.log(position,2))%8 - int(math.log(capture_position,2))%8) ==1:
                    moves.append(capture_position)
            return moves
        
        for delta_col in [9, 7]:
            capture_position = (position << delta_col) if direction else (position >> delta_col)
            if (self.is_opponent_piece(capture_position, piece_color, board_matrix) or (board_matrix["en_passant_position"] == capture_position)) and (int(math.log(position,2))%8 - int(math.log(capture_position,2))%8) in (-1, 1):
                moves.append(capture_position)
                
        forward_square = (position << 8) if direction else (position >> 8)
        if self.is_empty_position(board_matrix, forward_square):
            moves.append(forward_square)
            if (71776119061282560 | position) == 71776119061282560:
                double_forward_position = (position << 16) if direction else (position >> 16)
                if self.is_empty_position(board_matrix, double_forward_position):
                    moves.append(double_forward_position)
        return moves

    def calculate_rook_moves(self, piece_color, position, board_matrix, only_impact = False):
        moves = []
        row, col = self.position_to_square(position)

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for d_row, d_col in directions:
            for i in range(1, 8):
                new_row, new_col = row + d_row * i, col + d_col * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_position = self.square_to_position((new_row, new_col))
                    _, target_piece_color = self.identify_piece(target_position, board_matrix)
                    if target_piece_color == None:
                        moves.append(target_position)
                    elif target_piece_color != piece_color:
                        moves.append(target_position)
                        break
                    else:
                        break
                else:
                    break
                
        if not only_impact:
            if position in (1, 72057594037927936) and self.can_castle_queenside(piece_color, board_matrix):
                moves.append(1152921504606846976 if piece_color == "WHITE" else 16)
            if position in (128, 9223372036854775808) and self.can_castle_kingside(piece_color, board_matrix):
                moves.append(1152921504606846976 if piece_color == "WHITE" else 16)
                
        return moves
    
    def calculate_bishop_moves(self, piece_color, position, board_matrix):
        moves = []
        row, col = self.position_to_square(position)

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_position = self.square_to_position((r, c))
                _, target_piece_color = self.identify_piece(target_position, board_matrix)
                if target_piece_color == None:
                    moves.append(target_position)
                elif target_piece_color != piece_color:
                    moves.append(target_position)
                    break
                else:
                    break
                r += dr
                c += dc

        return moves

    def calculate_knight_moves(self, piece_color, position, board_matrix):
        moves = []
        row, col = self.position_to_square(position)
        
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_position = self.square_to_position((r, c))
                _, target_piece_color = self.identify_piece(target_position, board_matrix)
                if target_piece_color != piece_color:
                    moves.append(target_position)

        return moves
    
    def calculate_queen_moves(self, piece_color, position, board_matrix):
        moves = []
        
        moves += self.calculate_bishop_moves(piece_color, position, board_matrix)
        moves += self.calculate_rook_moves(piece_color, position, board_matrix)
        
        return moves
    
    def calculate_king_moves(self, piece_color, position, board_matrix, only_impact = False):
        moves = []
        row, col = self.position_to_square(position)
        opponent_color = "WHITE" if piece_color == "BLACK" else "BLACK"

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_position = self.square_to_position((r, c))
                _, target_piece_color = self.identify_piece(target_position, board_matrix)
                if target_piece_color != piece_color:
                    if only_impact or not self.is_position_attacked_by(opponent_color, target_position, board_matrix):
                        moves.append(target_position)
                        
        if not only_impact:
            if position == 1152921504606846976 and piece_color == "WHITE":
                if self.can_castle_queenside(piece_color, board_matrix):
                    moves.append(72057594037927936)
                if self.can_castle_kingside(piece_color, board_matrix):
                    moves.append(9223372036854775808)
            elif position == 16 and piece_color == "BLACK":
                if self.can_castle_queenside(piece_color, board_matrix):
                    moves.append(1)
                if self.can_castle_kingside(piece_color, board_matrix):
                    moves.append(128)

        return moves

    def is_opponent_piece(self, position, piece_color, board_matrix):
        _, other_piece_color = self.identify_piece(position, board_matrix)
        return other_piece_color and other_piece_color != piece_color

    def is_own_piece(self, position, piece_color, board_matrix):
        _, other_piece_color = self.identify_piece(position, board_matrix)
        return other_piece_color == piece_color
    
    def move_piece(self, start_position, end_position, board_matrix, promotion_piece_type = "QUEEN", move_counter = None):
        moved_piece_type, moved_piece_color = self.identify_piece(start_position, board_matrix)
        target_piece_type, target_piece_color = self.identify_piece(end_position, board_matrix)
        
        is_interesting_move = target_piece_type in ("ROOK", "KNIGHT", "BISHOP", "QUEEN", "PAWN")
        
        if not target_piece_color in (None, moved_piece_color): # Clear the captured piece
            board_matrix[target_piece_type + "_" + target_piece_color] &= ~(end_position) 
            board_matrix["last_capture_or_pawn_move"] = move_counter

        if moved_piece_type in ("KING", "ROOK"): # Casteling logic
            if (start_position in (72057594037927936, 1152921504606846976, 1, 16)) and (end_position in (72057594037927936, 1152921504606846976, 1, 16)) and self.can_castle_queenside(moved_piece_color, board_matrix):
                self.perform_castle_queenside(moved_piece_color, board_matrix)
                self.sum_pieces(board_matrix)
                board_matrix["en_passant_position"] = 0
                return False
            elif (start_position in (1152921504606846976, 9223372036854775808, 16, 128)) and (end_position in (1152921504606846976, 9223372036854775808, 16, 128)) and self.can_castle_kingside(moved_piece_color, board_matrix):
                self.perform_castle_kingside(moved_piece_color, board_matrix)
                self.sum_pieces(board_matrix)
                board_matrix["en_passant_position"] = 0
                return False
            self.update_casteling_rights(start_position, moved_piece_color, board_matrix)
        
        if moved_piece_type == "PAWN":
            board_matrix["last_capture_or_pawn_move"] = move_counter
            if end_position == board_matrix["en_passant_position"]: # Remove pawn if en passant move
                if moved_piece_color == "WHITE":
                    board_matrix["PAWN_BLACK"] &= ~(end_position << 8)
                else:
                    board_matrix["PAWN_WHITE"] &= ~(end_position >> 8)
            board_matrix["en_passant_position"] = None
            if (start_position | 71776119061282560) == 71776119061282560 and (end_position | 1099494850560) == 1099494850560: # Save en passant position if pawn moved 2 ranks
                if moved_piece_color == "WHITE":
                    board_matrix["en_passant_position"] = (start_position >> 8)
                else:
                    board_matrix["en_passant_position"] = (start_position << 8)
            if (end_position | -72057594037927681) == -72057594037927681: # Promote pawn on last rank
                self.pawn_promotion(start_position, end_position, board_matrix, moved_piece_color, promotion_piece_type)
                board_matrix["en_passant_position"] = 0
                return False
        else:
            board_matrix["en_passant_position"] = None
                
        board_matrix[moved_piece_type + "_" + moved_piece_color] &= ~(start_position) # Clear the start position
        board_matrix[moved_piece_type + "_" + moved_piece_color] |= (end_position) # Set the end position

        self.sum_pieces(board_matrix)
        
        return is_interesting_move
        
    def is_position_attacked_by(self, color, position, board_matrix):
        for position_factor in range(64):
            lookup_position = (1 << position_factor)
            lookup_piece_type, lookup_piece_color = self.identify_piece(lookup_position, board_matrix)
            if color == lookup_piece_color:
                if lookup_piece_type == "PAWN":
                    if position in self.calculate_pawn_moves(lookup_piece_color, lookup_position, board_matrix, True):
                        return True
                if lookup_piece_type == "ROOK":
                    if position in self.calculate_rook_moves(lookup_piece_color, lookup_position, board_matrix, True):
                        return True
                if lookup_piece_type == "BISHOP":
                    if position in self.calculate_bishop_moves(lookup_piece_color, lookup_position, board_matrix):
                        return True
                if lookup_piece_type == "KNIGHT":
                    if position in self.calculate_knight_moves(lookup_piece_color, lookup_position, board_matrix):
                        return True
                if lookup_piece_type == "QUEEN":
                    if position in self.calculate_queen_moves(lookup_piece_color, lookup_position, board_matrix):
                        return True
                if lookup_piece_type == "KING":
                    if position in self.calculate_king_moves(lookup_piece_color, lookup_position, board_matrix, True):
                        return True
                
        return False
    
    def move_will_cause_check(self, piece_color, board_matrix, start_position, end_position):
        temp_board_matrix = board_matrix.copy()
        self.move_piece(start_position, end_position, temp_board_matrix)
        
        return self.is_in_check(piece_color == "WHITE", temp_board_matrix)
    
    def is_in_check(self, white_turn, board_matrix):
        own_color = "WHITE" if white_turn else "BLACK"
        opponent_color = "BLACK" if white_turn else "WHITE"
        
        return self.is_position_attacked_by(opponent_color, board_matrix["KING_" + own_color], board_matrix)
    
    def is_in_checkmate(self, white_turn, board_matrix):
        own_color = "WHITE" if white_turn else "BLACK"
        temp_board_matrix = board_matrix.copy()
        if not self.is_in_check(white_turn, temp_board_matrix):
            return False
        for position_factor in range(64):
            lookup_position = (1 << position_factor)
            if self.is_own_piece(lookup_position, own_color, temp_board_matrix):
                if self.calculate_possible_moves(temp_board_matrix, lookup_position) != []:
                    return False
        return True
    
    def is_stalemate(self, white_turn, board_matrix):
        own_color = "WHITE" if white_turn else "BLACK"
        for position_factor in range(64):
            lookup_position = (1 << position_factor)
            if self.is_own_piece(lookup_position, own_color, board_matrix):
                if self.calculate_possible_moves(board_matrix, lookup_position) != []:
                    return False
        return True
    
    def can_castle_queenside(self, color, board_matrix):
        if color == "WHITE":
            if not ((board_matrix["casteling_rights"] & 8) == 8):
                return False
            elif not (self.is_empty_position(board_matrix, 144115188075855872) and self.is_empty_position(board_matrix, 288230376151711744) and self.is_empty_position(board_matrix, 576460752303423488)):
                return False
            elif self.is_position_attacked_by("BLACK", 144115188075855872, board_matrix) or self.is_position_attacked_by("BLACK", 288230376151711744, board_matrix) or self.is_position_attacked_by("BLACK", 576460752303423488, board_matrix):
                return False
        else:
            if not ((board_matrix["casteling_rights"] & 2) == 2):
                return False
            elif not (self.is_empty_position(board_matrix, 2) and self.is_empty_position(board_matrix, 4) and self.is_empty_position(board_matrix, 8)):
                return False
            elif self.is_position_attacked_by("WHITE", 2, board_matrix) or self.is_position_attacked_by("WHITE", 4, board_matrix) or self.is_position_attacked_by("WHITE", 8, board_matrix):
                return False
        return True
    
    def can_castle_kingside(self, color, board_matrix):
        if color == "WHITE":
            if not ((board_matrix["casteling_rights"] & 4) == 4):
                return False
            elif not (self.is_empty_position(board_matrix, 2305843009213693952) and self.is_empty_position(board_matrix, 4611686018427387904)):
                return False
            elif self.is_position_attacked_by("BLACK", 2305843009213693952, board_matrix) or self.is_position_attacked_by("BLACK", 4611686018427387904, board_matrix):
                return False
        else:
            if not ((board_matrix["casteling_rights"] & 1) == 1):
                return False
            elif not (self.is_empty_position(board_matrix, 32) and self.is_empty_position(board_matrix, 64)):
                return False
            elif self.is_position_attacked_by("WHITE", 32, board_matrix) or self.is_position_attacked_by("WHITE", 64, board_matrix):
                return False
        return True
    
    def update_casteling_rights(self, start_position, moved_piece_color, board_matrix):
        if moved_piece_color == "WHITE":
            if start_position == 1152921504606846976:
                board_matrix["casteling_rights"] &= ~(12)
                return
            elif start_position == 72057594037927936:
                board_matrix["casteling_rights"] &= ~(8)
                return
            elif start_position == 9223372036854775808:
                board_matrix["casteling_rights"] &= ~(4)
                return
        else:
            if start_position == 16:
                board_matrix["casteling_rights"] &= ~(3)
                return
            elif start_position == 1:
                board_matrix["casteling_rights"] &= ~(2)
                return
            elif start_position == 128:
                board_matrix["casteling_rights"] &= ~(1)
                return
            
    def perform_castle_queenside(self, piece_color, board_matrix):
        if piece_color == "WHITE":
            board_matrix["KING_WHITE"] &= ~(1152921504606846976)
            board_matrix["KING_WHITE"] |= (288230376151711744)
            board_matrix["ROOK_WHITE"] &= ~(72057594037927936)
            board_matrix["ROOK_WHITE"] |= (576460752303423488)
            board_matrix["casteling_rights"] &= ~(12)
        else:
            board_matrix["KING_BLACK"] &= ~(16)
            board_matrix["KING_BLACK"] |= (4)
            board_matrix["ROOK_BLACK"] &= ~(1)
            board_matrix["ROOK_BLACK"] |= (8)
            board_matrix["casteling_rights"] &= ~(3)
    
    def perform_castle_kingside(self, piece_color, board_matrix):
        if piece_color == "WHITE":
            board_matrix["KING_WHITE"] &= ~(1152921504606846976)
            board_matrix["KING_WHITE"] |= (4611686018427387904)
            board_matrix["ROOK_WHITE"] &= ~(9223372036854775808)
            board_matrix["ROOK_WHITE"] |= (2305843009213693952)
            board_matrix["casteling_rights"] &= ~(12)
        else:
            board_matrix["KING_BLACK"] &= ~(16)
            board_matrix["KING_BLACK"] |= (64)
            board_matrix["ROOK_BLACK"] &= ~(128)
            board_matrix["ROOK_BLACK"] |= (32)
            board_matrix["casteling_rights"] &= ~(3)
            
    def pawn_promotion(self, start_position, end_position, board_matrix, moved_piece_color, promotion_piece_type):
        if not promotion_piece_type:
            promotion_piece_type = self.board.get_promotion_piece(moved_piece_color)
        board_matrix["PAWN_" + moved_piece_color] &= ~(start_position)
        board_matrix[promotion_piece_type + "_" + moved_piece_color] |= (end_position)
        
    def archive_board(self, board_matrix):
        self.board_archive.append(board_matrix.copy())
        self.hash_board_archive.append(hash(str(board_matrix)))
        
    def check_threefold_repetition(self):
        return Counter(self.hash_board_archive).most_common(1)[0][1] >= 3
    
    def check_fifty_move_rule(self, move_counter, board_matrix):
        return (move_counter - board_matrix["last_capture_or_pawn_move"]) >= 100
    
    def get_archived_board(self, move):
        return self.board_archive[move]
    
    def sum_pieces(self, board_matrix):
        all_pieces = 0
        for piece, piece_position in board_matrix.items():
            if piece in ("casteling_rights", "en_passant_position", "last_capture_or_pawn_move", "all_pieces"):
                continue
            else:
                all_pieces |= piece_position
        board_matrix["all_pieces"] = all_pieces