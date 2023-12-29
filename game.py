import pygame
import sys
import copy
from collections import Counter
from board import Board
from pieces import ChessPiece, Color
from chess_engine import ChessEngine
from chess import Chess

class ChessGame:
    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.board = Board()
        self.initialize_board()
        self.possible_moves = []
        self.current_player = Color.WHITE
        self.move_counter = 0
        self.en_passant_square = None
        self.check_square = None
        self.winner_square = None
        self.chess = Chess(self.board)
        self.engine = ChessEngine(self.chess)
        
    def initialize_board(self):
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

    def start_game(self):
        pygame.init()
        running = True
        selected_square = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.winner_square == None:
                    x, y = event.pos
                    col = x // self.board.square_size
                    row = y // self.board.square_size
                    clicked_square = (row, col)
                    if clicked_square in self.possible_moves:
                        (self.board_matrix, self.en_passant_square) = self.chess.move_piece(selected_square, clicked_square, self.board_matrix, self.en_passant_square, self.current_player, None, True, self.move_counter)
                        selected_square = None
                        self.possible_moves = []
                        self.end_of_turn()
                        self.chess_engine_turn()
                        self.end_of_turn()
                    elif self.chess.is_valid_square(clicked_square, self.board_matrix, self.current_player):
                        piece = self.chess.get_piece(clicked_square, self.board_matrix)
                        if piece.value[0] == self.current_player.value:
                            selected_square = clicked_square
                            self.possible_moves = self.chess.calculate_possible_moves(selected_square, self.board_matrix, self.en_passant_square, self.current_player)
                    else:
                        selected_square = None
                        self.possible_moves = []
                    
                            
            self.board.update_board(self.board_matrix, selected_square, self.possible_moves, self.check_square, self.winner_square)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
        
    def switch_current_player(self):
        self.current_player = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK
        
    def end_of_turn(self):
        self.switch_current_player()
        self.chess.archive_board(self.board_matrix)
        self.check_game_state()
        self.move_counter += 1
        
    def check_game_state(self):
        if self.chess.is_in_check(self.board_matrix, self.current_player):
            self.check_square = self.chess.get_king_square(self.current_player, self.board_matrix)
            if self.chess.is_checkmate(self.board_matrix, self.en_passant_square, self.current_player):
                self.invoke_win()
        else:
            self.check_square = None
        if self.chess.is_stalemate(self.board_matrix, self.en_passant_square, self.current_player):
            self.invoke_draw()
        if self.chess.check_50_move_rule(self.move_counter):
            self.invoke_draw()
        if self.chess.check_threefold_repetition():
            self.invoke_draw()
                    
    def invoke_draw(self):
        self.winner_square = self.chess.get_king_square(Color.BLACK, self.board_matrix)
        self.winner_square = self.chess.get_king_square(Color.WHITE, self.board_matrix)
        
    def invoke_win(self):
        self.winner_square = self.chess.get_king_square(Color.BLACK if self.current_player == Color.WHITE else Color.WHITE, self.board_matrix)
        
    def chess_engine_turn(self):
        from_square, to_square, promotion_piece = self.engine.calculate_move(self.board_matrix, self.en_passant_square)
        if self.chess.is_valid_move(from_square, to_square, self.board_matrix, self.en_passant_square, self.current_player):
            (self.board_matrix, self.en_passant_square) = self.chess.move_piece(from_square, to_square, self.board_matrix,self.en_passant_square, self.current_player, promotion_piece, True, self.move_counter)
        else:
            raise ValueError(f"Engine tried to make invalid move: {from_square}, {to_square}, {promotion_piece}")