import pygame
from pygame.locals import *
import math

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

class Board:
    def __init__(self):
        self.colors = [WHITE, GRAY]
        self.square_size = WIDTH // 8
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chessboard")
        self.pieces_images = {
            "PAWN_WHITE": pygame.image.load("images/white-pawn.png"),
            "KING_WHITE": pygame.image.load("images/white-king.png"),
            "QUEEN_WHITE": pygame.image.load("images/white-queen.png"),
            "ROOK_WHITE": pygame.image.load("images/white-rook.png"),
            "BISHOP_WHITE": pygame.image.load("images/white-bishop.png"),
            "KNIGHT_WHITE": pygame.image.load("images/white-knight.png"),
            "PAWN_BLACK": pygame.image.load("images/black-pawn.png"),
            "KING_BLACK": pygame.image.load("images/black-king.png"),
            "QUEEN_BLACK": pygame.image.load("images/black-queen.png"),
            "ROOK_BLACK": pygame.image.load("images/black-rook.png"),
            "BISHOP_BLACK": pygame.image.load("images/black-bishop.png"),
            "KNIGHT_BLACK": pygame.image.load("images/black-knight.png")
        }

    def update_board(self, chess_pieces, selected_square, possible_moves, check_position, winner_positions):
        self.draw_board(check_position, winner_positions)
        self.draw_pieces(chess_pieces)
        if selected_square:
            self.mark_selected_square(selected_square)
        if possible_moves != []:
            self.mark_possible_moves(possible_moves)

    def draw_board(self, check_position, winner_positions):
        check_square = None
        winner_squares = []
        
        if check_position:
            check_square = self.position_to_square(check_position)
        if winner_positions != []:
            for position in winner_positions:
                winner_squares.append(self.position_to_square(position))
                
        for row in range(8):
            for col in range(8):
                color = self.colors[(row + col) % 2]
                if (row, col) == check_square:
                    color = ORANGE
                elif (row, col) in winner_squares:
                    color = GREEN
                
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def draw_pieces(self, board_matrix):
        for piece, bitboard in board_matrix.items():
            for position in range(64):
                row = position // 8
                col = position % 8
                if bitboard & (1 << position):
                    x = col * self.square_size
                    y = row * self.square_size
                    self.screen.blit(self.pieces_images[piece], (x, y))
                    
    def mark_selected_square(self, selected_square):
        row, col = self.position_to_square(selected_square)
        x = col * self.square_size
        y = row * self.square_size
        cross_color = RED
        
        thickness = 5
        
        center_x, center_y = x + self.square_size // 2, y + self.square_size // 2

        offset = self.square_size // 6

        start_line1 = (center_x - offset, center_y - offset)
        end_line1 = (center_x + offset, center_y + offset)
        start_line2 = (center_x - offset, center_y + offset)
        end_line2 = (center_x + offset, center_y - offset)
        
        pygame.draw.line(self.screen, cross_color, start_line1, end_line1, thickness)
        pygame.draw.line(self.screen, cross_color, start_line2, end_line2, thickness)
        
    def mark_possible_moves(self, possible_moves):
        for move in possible_moves:
            square = self.position_to_square(move)
            y = square[0] * self.square_size
            x = square[1] * self.square_size

            center_x, center_y = x + self.square_size // 2, y + self.square_size // 2

            radius = self.square_size // 2 - 25
            pygame.draw.circle(self.screen, BLUE, (center_x, center_y), radius, 5)

    def reset_screen(self):
        self.screen.fill(WHITE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chessboard")
        
    def position_to_square(self, position):
        # Convert a position (bit index) to a square (row, col)
        row = int(math.log(position, 2) // 8)
        col = int(math.log(position, 2) % 8)
        return row, col
