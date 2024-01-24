import pygame
import sys
from board import Board
from mychess import Chess
from engine import Engine

class ChessGame:
    def __init__(self):
        self.board_matrix = {
            "PAWN_BLACK": 0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000,
            "ROOK_BLACK": 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001,
            "KNIGHT_BLACK": 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010,
            "BISHOP_BLACK": 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100,
            "QUEEN_BLACK": 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000,
            "KING_BLACK": 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000,
            "PAWN_WHITE": 0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000,
            "ROOK_WHITE": 0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
            "KNIGHT_WHITE": 0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
            "BISHOP_WHITE": 0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
            "QUEEN_WHITE": 0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
            "KING_WHITE": 0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
            "casteling_rights": 0b1_1_1_1, #white-queenside, white-kingside, black-queenside, black-kingside
            "en_passant_position": 0,
            "last_capture_or_pawn_move": 0, 
            "all_pieces": 0b1111_1111_1111_1111_0000_0000_0000_0000_0000_0000_0000_0000_1111_1111_1111_1111
        }
        self.white_turn = True
        self.check_position = None
        self.winner_positions = []
        self.move_counter = 0
        self.board = Board()
        pygame.init()
        self.player_color = self.board.color_selection()
        self.board_flip = True if self.player_color == "BLACK" else False
        self.chess = Chess(self.board)
        self.engine = Engine(self.chess, self.player_color)

    def start_game(self):
        self.board.update_board(self.board_matrix, None, [], None, [], None, 0)
        running = True
        displayed_selected_position = None
        origin_position = None
        possible_moves = []
        self.chess.archive_board(self.board_matrix)
        
        if self.player_color == "BLACK":
            self.engine_turn()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    
                    if (x < 800) and self.winner_positions == []:
                        displayed_selected_position, possible_moves, origin_position = self.chess_interaction(x, y, possible_moves, origin_position)
                    else: 
                        self.menu_iteraction((x, y))

            self.board.update_board(self.board_matrix, displayed_selected_position, possible_moves, self.check_position, self.winner_positions, self.white_turn, self.move_counter)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
        
    def chess_interaction(self, x, y, possible_moves, origin_position):
        col = x // self.board.square_size
        row = y // self.board.square_size
        
        displayed_selected_position = self.chess.square_to_position((row, col))
        if self.board_flip:
            calculation_selected_position = self.reverse_bits(displayed_selected_position)
        else:
            calculation_selected_position = displayed_selected_position
        
        if calculation_selected_position in possible_moves:
            self.chess.move_piece(origin_position, calculation_selected_position, self.board_matrix, None, self.move_counter)
            possible_moves = []
            calculation_selected_position = None
            displayed_selected_position = None
            self.end_turn()
            if self.winner_positions == []:
                self.engine_turn()
            
        elif self.chess.is_own_piece(calculation_selected_position, self.player_color, self.board_matrix):
            possible_moves = self.chess.calculate_possible_moves(self.board_matrix, calculation_selected_position)
            origin_position = calculation_selected_position
        else:
            possible_moves = []
        
        return displayed_selected_position, possible_moves, origin_position
    
    def engine_turn(self):
        self.board.update_board(self.board_matrix, None, [], self.check_position, self.winner_positions, self.white_turn, self.move_counter)
        pygame.display.flip()
        engine_from_position, engine_to_position = self.engine.calculate_move(self.board_matrix, self.move_counter)
        self.chess.move_piece(engine_from_position, engine_to_position, self.board_matrix, "QUEEN", self.move_counter)
        self.end_turn()
        
    def end_turn(self):
        self.check_position = None
        self.chess.archive_board(self.board_matrix)
        if self.chess.check_threefold_repetition() or self.chess.check_fifty_move_rule(self.move_counter, self.board_matrix):
            print("is threefold or fifty")
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
            
    def menu_iteraction(self, clicked_coordinates):
        x, y = clicked_coordinates
        buttons = self.board.get_menu_buttons()
        displayed_move = self.move_counter
        running = True

        for button_type, button in buttons.items():
            if button.collidepoint((x, y)) and button_type == "left" and displayed_move > 0:
                displayed_move -= 1
                self.remember_archived_board(displayed_move)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for button_type, button in buttons.items():
                        if button.collidepoint((x, y)):
                            if button_type == "left" and displayed_move > 0:
                                displayed_move -= 1
                            elif button_type == "right" and displayed_move < self.move_counter:
                                displayed_move += 1
                            elif button_type == "far_right":
                                displayed_move = self.move_counter
                            if displayed_move == self.move_counter:
                                return
                            else:
                                self.remember_archived_board(displayed_move)
                                

            if displayed_move == self.move_counter:
                return
            
    def remember_archived_board(self, displayed_move):
        archived_board = self.chess.get_archived_board(displayed_move)
        archived_check_position = None
        if self.chess.is_in_check(True, archived_board):
            archived_check_position = archived_board["KING_WHITE"]
        elif self.chess.is_in_check(False, archived_board):
            archived_check_position = archived_board["KING_BLACK"]
        self.board.update_board(archived_board, None, [], archived_check_position, [], None, displayed_move)
        pygame.display.flip()
        
    def reverse_bits(self, n):
        result = 0
        for i in range(64):
            result <<= 1
            result |= n & 1
            n >>= 1
        return result