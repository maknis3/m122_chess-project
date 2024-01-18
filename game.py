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
            "KING_WHITE": 0b0001000000000000000000000000000000000000000000000000000000000000,
            "casteling_rights": 0b1111, #white-queenside, white-kingside, black-queenside, black-kingside
            "en_passant_position": 0,
            "last_capture_or_pawn_move": 0
        }
        self.white_turn = True
        self.check_position = None
        self.winner_positions = []
        self.move_counter = 0
        self.board = Board()
        pygame.init()
        self.board.update_board(self.board_matrix, None, [], None, [], None, 0)
        self.chess = Chess(self.board)

    def start_game(self):
        running = True
        selected_position = None
        origin_position = None
        possible_moves = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    
                    if (x < 800) and self.winner_positions == []:
                        selected_position, possible_moves, origin_position = self.chess_interaction(x, y, possible_moves, origin_position)
                    else: 
                        self.menu_iteraction((x, y))

            self.board.update_board(self.board_matrix, selected_position, possible_moves, self.check_position, self.winner_positions, self.white_turn, self.move_counter)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
        
        
        
    def chess_interaction(self, x, y, possible_moves, origin_position):
        col = x // self.board.square_size
        row = y // self.board.square_size
        
        selected_position = self.chess.square_to_position((row, col))
        print("selected position: " + str(selected_position))
        
        if selected_position in possible_moves:
            self.chess.move_piece(origin_position, selected_position, self.board_matrix, None, self.move_counter)
            possible_moves = []
            selected_position = None
            self.end_turn()
        elif self.chess.is_own_piece(selected_position, "WHITE" if self.white_turn else "BLACK", self.board_matrix):
            possible_moves = self.chess.calculate_possible_moves(self.board_matrix, selected_position)
            origin_position = selected_position
        else:
            possible_moves = []
        
        return selected_position, possible_moves, origin_position
        
    def end_turn(self):
        self.check_position = None
        self.chess.archive_board(self.board_matrix)
        if self.chess.check_threefold_repetition() or self.chess.check_fifty_move_rule(self.move_counter, self.board_matrix):
            self.proclaim_draw()
            return
        
        self.move_counter += 1
        self.white_turn = not self.white_turn
        
        if self.chess.is_in_check(self.white_turn, self.board_matrix):
            if self.chess.is_in_checkmate(self.white_turn, self.board_matrix):
                opponent_color = "BLACK" if self.white_turn else "WHITE"
                self.winner_positions = [self.board_matrix["KING_" + opponent_color]]
                return
            else:
                own_color = "WHITE" if self.white_turn else "BLACK"
                self.check_position = self.board_matrix["KING_" + own_color]
        elif self.chess.is_stalemate(self.white_turn, self.board_matrix):
            self.proclaim_draw()
            
    def proclaim_draw(self):
        self.winner_positions = [self.board_matrix["KING_WHITE"], self.board_matrix["KING_BLACK"]]
            
    def menu_iteraction(self, coordinates):
        x, y = coordinates
        buttons = self.board.get_menu_buttons()
        displayed_move = self.move_counter
        running = True

        for button_type, button in buttons.items():
            if button.collidepoint((x, y)) and button_type == "left":
                displayed_move -= 1

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button_type, button in buttons.items():
                        if button.collidepoint((x, y)):
                            if button_type == "left":
                                displayed_move -= 1
                            elif button_type == "right":
                                displayed_move += 1
                            elif button_type == "far_right":
                                displayed_move = self.move_counter
                            else:
                                continue
                            archived_board = self.chess.get_archived_board(displayed_move)
                            archived_white_turn = (displayed_move % 2) == 0
                            archived_check_position = None
                            if self.chess.is_in_check(archived_white_turn, archived_board):
                                own_color = "WHITE" if archived_white_turn else "BLACK"
                                archived_check_position = archived_board["KING_" + own_color]
                            self.board.update_board(archived_board, None, None, archived_check_position, [], None, displayed_move)
                            pygame.display.flip()

            if displayed_move == self.move_counter:
                running = False