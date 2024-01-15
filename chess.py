import pygame
import sys
import copy
import math
from collections import Counter
from board import Board

class Chess:
    def __init__(self):
        self.casteling_rights = 0b1111 #white-queenside, white-kingside, black-queenside, black-kingside
    
    def get_position(self, square):
        position = (2**square[1]) << square[0]*8
        return position
    
    def is_empty_square(self, board_matrix, position):
        for piece in board_matrix:
            if (board_matrix[piece] & position) != 0:
                return False
        return True
    
    def square_to_position(self, square):
        # Convert a square (row, col) to a position (bit index)
        return 1 << (square[0] * 8 + square[1])

    def position_to_square(self, position):
        # Convert a position (bit index) to a square (row, col)
        row = int(math.log(position, 2) // 8)
        col = int(math.log(position, 2) % 8)
        return row, col
    
    def identify_piece(self, position, board_matrix):
        for piece in board_matrix:
            if (board_matrix[piece] & position) == position:
                piece = piece.split('_')
                piece_type = piece[0]
                piece_color = piece[1]
                return piece_type, piece_color
        return None, None

    def calculate_possible_moves(self, board_matrix, square):
        position = self.get_position(square)
        piece_type, piece_color = self.identify_piece(position, board_matrix)
        print(piece_type, piece_color, position)
        if piece_type:
            if piece_type == "PAWN":
                return self.calculate_pawn_moves(piece_color, position, board_matrix)
            if piece_type == "ROOK":
                return self.calculate_rook_moves(piece_color, position, board_matrix)
            if piece_type == "BISHOP":
                return self.calculate_bishop_moves(piece_color, position, board_matrix)
            # Add conditions for other pieces here...
        return []

    
    def calculate_pawn_moves(self, piece_color, position, board_matrix):
        moves = []
        direction = False if piece_color=="WHITE" else True
        for delta_col in [9, 7]:
            capture_square = (position << delta_col) if direction else (position >> delta_col)
            if not self.is_opponent_piece(capture_square, piece_color, board_matrix) and (math.log(position,2)/8 == math.log(capture_square,2)/8):
                moves.append(capture_square)
                
        forward_square = (position << 8) if direction else (position >> 8)
        if self.is_empty_square(board_matrix, forward_square):
            moves.append(forward_square)
            if self.position_to_square(position)[0] in (6, 1):
                double_forward_square = (position << 16) if direction else (position >> 16)
                if self.is_empty_square(board_matrix, double_forward_square):
                    moves.append(double_forward_square)
        return moves

    def calculate_rook_moves(self, piece_color, position, board_matrix):
        moves = []
        row, col = self.position_to_square(position)

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for d_row, d_col in directions:
            for i in range(1, 8):
                new_row, new_col = row + d_row * i, col + d_col * i
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    new_position = self.square_to_position((new_row, new_col))
                    if self.is_empty_square(board_matrix, new_position):
                        moves.append(new_position)
                    else:
                        if self.is_opponent_piece(new_position, piece_color, board_matrix):
                            moves.append(new_position)
                        break
                else:
                    break

        return moves
    
    def calculate_bishop_moves(self, piece_color, position, board_matrix):
        moves = []
        row, col = self.position_to_square(position)

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_position = self.square_to_position((r, c))
                if self.is_empty_square(board_matrix, target_position):
                    moves.append(target_position)
                elif self.is_opponent_piece(target_position, piece_color, board_matrix):
                    moves.append(target_position)
                    break
                else:
                    break
                r += dr
                c += dc

        return moves


    def is_opponent_piece(self, position, piece_color, board_matrix):
        _, other_piece_color = self.identify_piece(position, board_matrix)
        return other_piece_color and other_piece_color != piece_color
    
    def move_piece_square(self, start_square, end_square, board_matrix):
        start_position = self.get_position(start_square)
        end_position = self.get_position(end_square)

        moved_piece_type, moved_piece_color = self.identify_piece(start_position, board_matrix)
        
        if not self.is_empty_square(board_matrix, end_position):
            target_piece_type, target_piece_color = self.identify_piece(end_position, board_matrix)
            board_matrix[target_piece_type + "_" + target_piece_color] &= ~(end_position) # Clear the captured piece

        board_matrix[moved_piece_type + "_" + moved_piece_color] &= ~(start_position) # Clear the start position
        board_matrix[moved_piece_type + "_" + moved_piece_color] |= (end_position) # Set the end position