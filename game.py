import pygame
import sys
from board import Board
from pieces import ChessPiece, Color

class ChessGame:
    def __init__(self):
        self.initialize_board()
        self.board = Board()
        self.clicked_square = None
        self.possible_moves = []
        self.current_player = Color.WHITE
        self.move_counter = 0
        self.kingside_castling_rights = {Color.WHITE: True, Color.BLACK: True}
        self.queenside_castling_rights = {Color.WHITE: True, Color.BLACK: True}
        self.en_passant_squere = None

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
                        self.switch_current_player()
                        self.move_counter += 1
                    elif self.is_valid_square(clicked_square):
                        piece = self.get_piece(clicked_square)
                        if piece.value[0] == self.current_player.value:
                            selected_square = clicked_square
                            self.possible_moves = self.calculate_possible_moves(selected_square)

            self.board.update_board(self.board_matrix, selected_square, self.possible_moves)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def is_valid_square(self, square):
        row, col = square
        return self.get_piece(square) != ChessPiece.EMPTY

    def get_piece(self, square):
        row, col = square
        return self.board_matrix[row][col]

    def move_piece(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        piece = self.get_piece(from_square)
        castle_performed = False
        en_passant_possible = False
        #castle:
        if piece == ChessPiece.KING_BLACK or piece == ChessPiece.KING_WHITE or piece == ChessPiece.ROOK_BLACK or piece == ChessPiece.ROOK_WHITE:
            if self.kingside_castling_rights[self.current_player] and ((from_col == 4 and to_col == 7) or (from_col == 7 and to_col == 4)):
                self.perform_castle_kingside()
                castle_performed = True
            if self.queenside_castling_rights[self.current_player] and ((from_col == 4 and to_col == 0) or (from_col == 0 and to_col == 4)):
                self.perform_castle_queenside()
                castle_performed = True
        #normal move:
        if not castle_performed:
            self.board_matrix[to_row][to_col] = self.board_matrix[from_row][from_col]
            self.board_matrix[from_row][from_col] = ChessPiece.EMPTY
            #enpassant:
            if piece == ChessPiece.PAWN_BLACK or piece == ChessPiece.PAWN_WHITE:
                if (from_row - to_row == 2 or from_row - to_row == -2):
                    self.en_passant_squere = None
                    self.en_passant_squere = (from_row + ((to_row - from_row)/2), from_col)
                    en_passant_possible = True
                if to_square == self.en_passant_squere:
                    self.board_matrix[from_row][to_col] = ChessPiece.EMPTY
        #update castle rights:
        if piece == ChessPiece.KING_BLACK or piece == ChessPiece.KING_WHITE or castle_performed:
            self.kingside_castling_rights[self.current_player] = False
            self.queenside_castling_rights[self.current_player] = False
        if piece == ChessPiece.ROOK_BLACK or piece == ChessPiece.ROOK_WHITE:
            if from_col == 0:
                self.queenside_castling_rights[self.current_player] = False
            elif from_col == 7:
                self.kingside_castling_rights[self.current_player] = False
        if not en_passant_possible:
            self.en_passant_squere = None

    def switch_current_player(self):
        self.current_player = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK

    def calculate_possible_moves(self, active_square):
        row, col = active_square
        piece = self.get_piece(active_square)
        possible_moves = []

        if piece == ChessPiece.PAWN_WHITE:
            possible_moves += self.calculate_pawn_moves(row, col, -1)
        elif piece == ChessPiece.PAWN_BLACK:
            possible_moves += self.calculate_pawn_moves(row, col, 1)
        elif piece in (ChessPiece.ROOK_WHITE, ChessPiece.ROOK_BLACK):
            possible_moves += self.calculate_rook_moves(row, col)
        elif piece in (ChessPiece.KNIGHT_WHITE, ChessPiece.KNIGHT_BLACK):
            possible_moves += self.calculate_knight_moves(row, col)
        elif piece in (ChessPiece.BISHOP_WHITE, ChessPiece.BISHOP_BLACK):
            possible_moves += self.calculate_bishop_moves(row, col)
        elif piece in (ChessPiece.QUEEN_WHITE, ChessPiece.QUEEN_BLACK):
            possible_moves += self.calculate_rook_moves(row, col)
            possible_moves += self.calculate_bishop_moves(row, col)
        elif piece in (ChessPiece.KING_WHITE, ChessPiece.KING_BLACK):
            possible_moves += self.calculate_king_moves(row, col)

        return possible_moves

    def calculate_pawn_moves(self, row, col, direction):
        possible_moves = []

        if 0 <= row + direction < 8 and self.get_piece((row + direction, col)) == ChessPiece.EMPTY:
            possible_moves.append((row + direction, col))

            if row == 6 and direction == -1 and self.get_piece((row + direction * 2, col)) == ChessPiece.EMPTY:
                possible_moves.append((row + direction * 2, col))
            elif row == 1 and direction == 1 and self.get_piece((row + direction * 2, col)) == ChessPiece.EMPTY:
                possible_moves.append((row + direction * 2, col))

        for d_col in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + d_col < 8:
                target_squere = (row + direction, col + d_col)
                target_piece = self.get_piece(target_squere)
                if (target_piece != ChessPiece.EMPTY and target_piece.value[0] != self.current_player.value) or (target_squere == self.en_passant_squere):
                    possible_moves.append(target_squere)

        return possible_moves

    def calculate_rook_moves(self, row, col):
        possible_moves = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_piece = self.get_piece((r, c))
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append((r, c))
                elif target_piece.value[0] != self.current_player.value:
                    possible_moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

        if col == 7 and self.can_castle_kingside():
            possible_moves.append((7, 4))

        if col == 0 and self.can_castle_queenside():
            possible_moves.append((7, 4))

        return possible_moves

        return possible_moves

    def calculate_knight_moves(self, row, col):
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        possible_moves = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = self.get_piece((r, c))
                if target_piece == ChessPiece.EMPTY or target_piece.value[0] != self.current_player.value:
                    possible_moves.append((r, c))

        return possible_moves

    def calculate_bishop_moves(self, row, col):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        possible_moves = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_piece = self.get_piece((r, c))
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append((r, c))
                elif target_piece.value[0] != self.current_player.value:
                    possible_moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

        return possible_moves

    def calculate_king_moves(self, row, col):
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        possible_moves = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = self.get_piece((r, c))
                if target_piece == ChessPiece.EMPTY or target_piece.value[0] != self.current_player.value:
                    if not self.is_protected((r, c)):
                        possible_moves.append((r, c))

        castle_row_factor = 0 if self.current_player == Color.BLACK else 7
        
        if self.can_castle_kingside():
            possible_moves.append((castle_row_factor, 7))

        if self.can_castle_queenside():
            possible_moves.append((castle_row_factor, 0))

        return possible_moves

    def is_square_empty(self, square):
        return self.get_piece(square) == ChessPiece.EMPTY

    def is_protected(self, square):
        row, col = square
        opponent_impact = []

        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c))
                if piece != ChessPiece.EMPTY and piece.value[0] != self.current_player.value:
                    possible_impact_squares = []

                    if piece == ChessPiece.PAWN_WHITE:
                        possible_impact_squares += self.calculate_pawn_impact(r, c, -1)
                    elif piece == ChessPiece.PAWN_BLACK:
                        possible_impact_squares += self.calculate_pawn_impact(r, c, 1)
                    elif piece in (ChessPiece.ROOK_WHITE, ChessPiece.ROOK_BLACK):
                        possible_impact_squares += self.calculate_rook_impact(r, c)
                    elif piece in (ChessPiece.KNIGHT_WHITE, ChessPiece.KNIGHT_BLACK):
                        possible_impact_squares += self.calculate_knight_impact(r, c)
                    elif piece in (ChessPiece.BISHOP_WHITE, ChessPiece.BISHOP_BLACK):
                        possible_impact_squares += self.calculate_bishop_impact(r, c)
                    elif piece in (ChessPiece.QUEEN_WHITE, ChessPiece.QUEEN_BLACK):
                        possible_impact_squares += self.calculate_rook_impact(r, c)
                        possible_impact_squares += self.calculate_bishop_impact(r, c)
                    elif piece in (ChessPiece.KING_WHITE, ChessPiece.KING_BLACK):
                        possible_impact_squares += self.calculate_king_impact(r, c)

                    opponent_impact += possible_impact_squares

        return square in opponent_impact

    def calculate_pawn_impact(self, row, col, direction):
        impact_squares = []

        for d_col in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + d_col < 8:
                impact_squares.append((row + direction, col + d_col))

        return impact_squares

    def calculate_rook_impact(self, row, col):
        impact_squares = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if not self.is_square_empty((r, c)):
                    impact_squares.append((r, c))
                    break
                impact_squares.append((r, c))
                r += dr
                c += dc

        return impact_squares

    def calculate_knight_impact(self, row, col):
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        impact_squares = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                impact_squares.append((r, c))

        return impact_squares

    def calculate_bishop_impact(self, row, col):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        impact_squares = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if not self.is_square_empty((r, c)):
                    impact_squares.append((r, c))
                    break
                impact_squares.append((r, c))
                r += dr
                c += dc

        return impact_squares

    def calculate_king_impact(self, row, col):
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        impact_squares = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                impact_squares.append((r, c))

        return impact_squares

    def can_castle_kingside(self):
        if self.kingside_castling_rights[self.current_player] == False:
            return False

        if self.current_player == Color.WHITE:
            if not self.is_square_empty((7, 5)) or not self.is_square_empty((7, 6)):
                return False
            if self.is_protected((7, 4)) or self.is_protected((7, 5)) or self.is_protected((7, 6)):
                return False
        else:
            if not self.is_square_empty((0, 5)) or not self.is_square_empty((0, 6)):
                return False
            if self.is_protected((0, 4)) or self.is_protected((0, 5)) or self.is_protected((0, 6)):
                return False

        return True

    def can_castle_queenside(self):
        if self.queenside_castling_rights[self.current_player] == False:
            return False
        if self.current_player == Color.WHITE:
            if not self.is_square_empty((7, 3)) or not self.is_square_empty((7, 2)) or not self.is_square_empty((7, 1)):
                return False
            if self.is_protected((7, 4)) or self.is_protected((7, 3)) or self.is_protected((7, 2)):
                return False
        else:
            if not self.is_square_empty((0, 3)) or not self.is_square_empty((0, 2)) or not self.is_square_empty((0, 1)):
                return False
            if self.is_protected((0, 4)) or self.is_protected((0, 3)) or self.is_protected((0, 2)):
                return False

        return True

    def perform_castle_kingside(self):
        if self.current_player == Color.WHITE:
            self.board_matrix[7][4] = ChessPiece.EMPTY
            self.board_matrix[7][7] = ChessPiece.EMPTY
            self.board_matrix[7][6] = ChessPiece.KING_WHITE
            self.board_matrix[7][5] = ChessPiece.ROOK_WHITE
        else:
            self.board_matrix[0][4] = ChessPiece.EMPTY
            self.board_matrix[0][7] = ChessPiece.EMPTY
            self.board_matrix[0][6] = ChessPiece.KING_BLACK
            self.board_matrix[0][5] = ChessPiece.ROOK_BLACK 
        
    def perform_castle_queenside(self):
        if self.current_player == Color.WHITE:
            self.board_matrix[7][4] = ChessPiece.EMPTY
            self.board_matrix[7][0] = ChessPiece.EMPTY
            self.board_matrix[7][2] = ChessPiece.KING_WHITE
            self.board_matrix[7][3] = ChessPiece.ROOK_WHITE
        else:
            self.board_matrix[0][4] = ChessPiece.EMPTY
            self.board_matrix[0][0] = ChessPiece.EMPTY
            self.board_matrix[0][2] = ChessPiece.KING_BLACK
            self.board_matrix[0][3] = ChessPiece.ROOK_BLACK 
        
