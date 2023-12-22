import os
import pygame
from pygame.locals import *
import sys
from board import Board
from pieces import ChessPiece
from pieces import Color

pygame.init()

class Game:
    def __init__(self):
        self.board_matrix = [
            [ChessPiece.ROOK_BLACK, ChessPiece.KNIGHT_BLACK, ChessPiece.BISHOP_BLACK, ChessPiece.QUEEN_BLACK, ChessPiece.KING_BLACK, ChessPiece.BISHOP_BLACK, ChessPiece.KNIGHT_BLACK, ChessPiece.ROOK_BLACK],
            [ChessPiece.PAWN_BLACK] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.PAWN_WHITE] * 8,
            [ChessPiece.ROOK_WHITE, ChessPiece.KNIGHT_WHITE, ChessPiece.BISHOP_WHITE, ChessPiece.QUEEN_WHITE, ChessPiece.KING_WHITE, ChessPiece.BISHOP_WHITE, ChessPiece.KNIGHT_WHITE, ChessPiece.ROOK_WHITE],
        ]
        self.board = Board()
        self.clicked_square = None
        self.possible_moves = []
        self.current_player = Color.WHITE
        self.move_counter = 0

    def start_game(self):
        running = True
        selected_square = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    col = x // self.board.square_size
                    row = y // self.board.square_size
                    clicked_square = (row, col)

                    if clicked_square in self.possible_moves:
                        self.move_piece(selected_square, clicked_square)
                        selected_square = None
                        self.possible_moves = []
                        self.current_player = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK
                        self.move_counter += 1
                    elif self.is_valid_square(clicked_square):
                        piece = self.board_matrix[row][col]
                        if piece.value[0] == self.current_player.value:  # Use .value to compare the Color enum
                            selected_square = clicked_square
                            self.possible_moves = self.calculate_possible_moves(selected_square)

            self.board.update_board(self.board_matrix, selected_square, self.possible_moves)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

        
    def is_valid_square(self, square):
        row, col = square
        return self.board_matrix[row][col] != ChessPiece.EMPTY
    
    def is_opponent_piece(self, piece1, piece2):
        return piece1 != ChessPiece.EMPTY and piece2 != ChessPiece.EMPTY and piece1.value[0] != piece2.value[0]

    def calculate_possible_moves(self, active_square):
        row, col = active_square
        piece = self.board_matrix[row][col]
        possible_moves = []

        if piece == ChessPiece.PAWN_WHITE:
            if row - 1 >= 0 and self.board_matrix[row - 1][col] == ChessPiece.EMPTY:
                possible_moves.append((row - 1, col))
            if row == 6 and self.board_matrix[row - 2][col] == ChessPiece.EMPTY:
                possible_moves.append((row - 2, col))
            
            # Pawn captures diagonally
            if col - 1 >= 0 and self.is_opponent_piece(piece, self.board_matrix[row - 1][col - 1]):
                possible_moves.append((row - 1, col - 1))
            if col + 1 < 8 and self.is_opponent_piece(piece, self.board_matrix[row - 1][col + 1]):
                possible_moves.append((row - 1, col + 1))
            
        elif piece == ChessPiece.PAWN_BLACK:
            if row + 1 < 8 and self.board_matrix[row + 1][col] == ChessPiece.EMPTY:
                possible_moves.append((row + 1, col))
            if row == 1:
                if self.board_matrix[row + 1][col] == ChessPiece.EMPTY:
                    possible_moves.append((row + 1, col))
                if self.board_matrix[row + 2][col] == ChessPiece.EMPTY:
                    possible_moves.append((row + 2, col))
            
            # Pawn captures diagonally
            if col - 1 >= 0 and self.is_opponent_piece(piece, self.board_matrix[row + 1][col - 1]):
                possible_moves.append((row + 1, col - 1))
            if col + 1 < 8 and self.is_opponent_piece(piece, self.board_matrix[row + 1][col + 1]):
                possible_moves.append((row + 1, col + 1))
        
        elif piece == ChessPiece.ROOK_WHITE or piece == ChessPiece.ROOK_BLACK:
            # Rook can move horizontally and vertically
            for r in range(row - 1, -1, -1):  # Up
                if self.is_opponent_piece(piece, self.board_matrix[r][col]):
                    possible_moves.append((r, col))
                    break
                if self.board_matrix[r][col] != ChessPiece.EMPTY:
                    break

            for r in range(row + 1, 8):  # Down
                if self.is_opponent_piece(piece, self.board_matrix[r][col]):
                    possible_moves.append((r, col))
                    break
                if self.board_matrix[r][col] != ChessPiece.EMPTY:
                    break

            for c in range(col - 1, -1, -1):  # Left
                if self.is_opponent_piece(piece, self.board_matrix[row][c]):
                    possible_moves.append((row, c))
                    break
                if self.board_matrix[row][c] != ChessPiece.EMPTY:
                    break

            for c in range(col + 1, 8):  # Right
                if self.is_opponent_piece(piece, self.board_matrix[row][c]):
                    possible_moves.append((row, c))
                    break
                if self.board_matrix[row][c] != ChessPiece.EMPTY:
                    break

        elif piece == ChessPiece.KNIGHT_WHITE or piece == ChessPiece.KNIGHT_BLACK:
            # Knight moves in an L-shape (8 possible moves)
            moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
            for dr, dc in moves:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target_piece = self.board_matrix[r][c]
                    if target_piece == ChessPiece.EMPTY or self.is_opponent_piece(piece, target_piece):
                        possible_moves.append((r, c))

        elif piece == ChessPiece.BISHOP_WHITE or piece == ChessPiece.BISHOP_BLACK:
            # Bishop can move diagonally
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    target_piece = self.board_matrix[r][c]
                    if target_piece == ChessPiece.EMPTY or self.is_opponent_piece(piece, target_piece):
                        possible_moves.append((r, c))
                        if target_piece != ChessPiece.EMPTY:
                            break
                    else:
                        break
                    r += dr
                    c += dc

        elif piece == ChessPiece.QUEEN_WHITE or piece == ChessPiece.QUEEN_BLACK:
            # Queen can move horizontally, vertically, and diagonally (combining rook and bishop moves)
            for r in range(row - 1, -1, -1):  # Up
                target_piece = self.board_matrix[r][col]
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append((r, col))
                elif self.is_opponent_piece(piece, target_piece):
                    possible_moves.append((r, col))
                    break
                else:
                    break
                
            for r in range(row + 1, 8):  # Down
                target_piece = self.board_matrix[r][col]
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append((r, col))
                elif self.is_opponent_piece(piece, target_piece):
                    possible_moves.append((r, col))
                    break
                else:
                    break
                
            for c in range(col - 1, -1, -1):  # Left
                target_piece = self.board_matrix[row][c]
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append((row, c))
                elif self.is_opponent_piece(piece, target_piece):
                    possible_moves.append((row, c))
                    break
                else:
                    break
                
            for c in range(col + 1, 8):  # Right
                target_piece = self.board_matrix[row][c]
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append((row, c))
                elif self.is_opponent_piece(piece, target_piece):
                    possible_moves.append((row, c))
                    break
                else:
                    break
                
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8:
                    target_piece = self.board_matrix[r][c]
                    if target_piece == ChessPiece.EMPTY:
                        possible_moves.append((r, c))
                    elif self.is_opponent_piece(piece, target_piece):
                        possible_moves.append((r, c))
                        break
                    else:
                        break
                    r += dr
                    c += dc

        elif piece == ChessPiece.KING_WHITE or piece == ChessPiece.KING_BLACK:
            # King can move one step in any direction
            moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in moves:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target_piece = self.board_matrix[r][c]
                    if target_piece == ChessPiece.EMPTY or self.is_opponent_piece(piece, target_piece):
                        possible_moves.append((r, c))


        return possible_moves
    
    def move_piece(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        self.board_matrix[to_row][to_col] = self.board_matrix[from_row][from_col]
        self.board_matrix[from_row][from_col] = ChessPiece.EMPTY