import pygame
import sys
import math
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
        self.en_passant_position = []
        self.check_position = None
        self.winner_positions = []
        self.move_counter = 0
        self.board = Board()
        self.board.update_board(self.board_matrix, None, [], None, [])
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
                    selected_square = self.chess.square_to_position((row, col))
                    if selected_square in possible_moves:
                        self.chess.move_piece(origin_square, selected_square, self.board_matrix)
                        possible_moves = []
                        selected_square = None
                    elif not self.chess.is_empty_position(self.board_matrix, selected_square):
                        possible_moves = self.chess.calculate_possible_moves(self.board_matrix, selected_square)
                        origin_square = selected_square
                    else:
                        possible_moves = []
            self.board.update_board(self.board_matrix, selected_square, possible_moves, self.check_position, self.winner_positions)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
        
    def end_trun(self):
        self.check_position = None
        
        self.move_counter += 1
        self.white_turn = not self.white_turn
        
        if self.chess.is_in_check(self.white_turn, self.board_matrix):
            if self.chess.is_in_checkmate():
                pass
            else:
                self.check_position = self.board_matrix["KING_" + "WHITE" if self.white_turn else "BLACK"]