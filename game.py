import pygame
import sys
from board import Board
from chess import Chess

class ChessGame:
    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.board_matrix = {
            "PAWN_BLACK": 0b0000000000000000000000000000000000000000000000001111111100000000,
            "ROOK_BLACK": 0b0000000000000000000000000000000000000000000000000000000010000001,
            "KNIGHT_BLACK": 0b0000000000000000000000000000000000000000000000000000000001000010,
            "BISHOP_BLACK": 0b0000000000000000000000000000000000000000000000000000000000100100,
            "QUEEN_BLACK": 0b0000000000000000000000000000000000000000000000000000000000001000,
            "KING_BLACK": 0b0000000000000000000000000000000000000000000000000000000000010000,
            "PAWN_WHITE": 0b0000000011111111000000000000000000000000000000000000000000000000,
            "ROOK_WHITE": 0b1000000100000000000000000000000000000000000000000000000000000000,
            "KNIGHT_WHITE": 0b0100001000000000000000000000000000000000000000000000000000000000,
            "BISHOP_WHITE": 0b0010010000000000000000000000000000000000000000000000000000000000,
            "QUEEN_WHITE": 0b0000100000000000000000000000000000000000000000000000000000000000,
            "KING_WHITE": 0b0001000000000000000000000000000000000000000000000000000000000000
        }
        self.white_turn = True
        self.en_passant_square = None
        self.move_counter = 0
        self.board = Board()
        self.board.update_board(self.board_matrix, None, [])
        self.chess = Chess()

    def start_game(self):
        pygame.init()
        running = True
        selected_square = None
        possible_moves = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    col = x // self.board.square_size
                    row = y // self.board.square_size
                    selected_square = (row, col)
                    if selected_square in possible_moves:
                        self.chess.move_piece_square(origin_square, selected_square, self.board_matrix)
                        possible_moves = []
                        selected_square = None
                    elif not self.chess.is_empty_square(self.board_matrix, self.chess.get_position(selected_square)):
                        possible_moves = self.positions_to_squares(self.chess.calculate_possible_moves(self.board_matrix, selected_square))
                        origin_square = selected_square
                    else:
                        possible_moves = []
            self.board.update_board(self.board_matrix, selected_square, possible_moves)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
    
    def positions_to_squares(self, positions):
        squares = []
        for possibility in range(64):
            for position in positions:
                if position & (1 << possibility):
                    row = possibility % 8
                    col = possibility // 8
                    squares.append((row, col))
        return squares