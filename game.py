import pygame
import sys
import copy
from board import Board
from pieces import ChessPiece, Color

class ChessGame:
    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.board = Board()
        self.initialize_board()
        self.possible_moves = []
        self.current_player = Color.WHITE
        self.move_counter = 0
        self.castling_rights = {
            Color.WHITE: {'kingside': True, 'queenside': True},
            Color.BLACK: {'kingside': True, 'queenside': True}
        }
        self.en_passant_square = None
        self.check_square = None
        self.winner_square = None
        
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
                        self.board_matrix = self.move_piece(selected_square, clicked_square, self.board_matrix)
                        selected_square = None
                        self.possible_moves = []
                        self.switch_current_player()
                        if self.is_in_check(self.board_matrix):
                            if self.is_checkmate(self.board_matrix):
                                pass
                            self.check_square = self.get_king_square(self.current_player, self.board_matrix)
                        else:
                            self.check_square = None
                        self.move_counter += 1
                    elif self.is_valid_square(clicked_square, self.board_matrix):
                        piece = self.get_piece(clicked_square, self.board_matrix)
                        if piece.value[0] == self.current_player.value:
                            selected_square = clicked_square
                            self.possible_moves = self.calculate_possible_moves(selected_square, self.board_matrix)
                    
                            
            self.board.update_board(self.board_matrix, selected_square, self.possible_moves, self.check_square, self.winner_square)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def is_valid_square(self, square, board_matrix):
        return self.get_piece(square, board_matrix) != ChessPiece.EMPTY

    def get_piece(self, square, board_matrix):
        row, col = square
        return board_matrix[row][col]

    def move_piece(self, from_square, to_square, board_matrix):
        new_board_matrix = copy.deepcopy(board_matrix)
        from_row, from_col = from_square
        to_row, to_col = to_square
        piece = self.get_piece(from_square, new_board_matrix)
        en_passant_possible = False

        if piece == ChessPiece.KING_BLACK or ChessPiece.KING_WHITE or ChessPiece.ROOK_WHITE or ChessPiece.ROOK_BLACK:
            if self.castling_rights[self.current_player]['kingside'] and (
                    (from_col == 4 and to_col == 7) or (from_col == 7 and to_col == 4)):
                return self.perform_castle_kingside(new_board_matrix)
            if self.castling_rights[self.current_player]['queenside'] and (
                    (from_col == 4 and to_col == 0) or (from_col == 0 and to_col == 4)):
                return self.perform_castle_queenside(new_board_matrix)

        new_board_matrix[to_row][to_col] = new_board_matrix[from_row][from_col]
        new_board_matrix[from_row][from_col] = ChessPiece.EMPTY

        if piece in (ChessPiece.PAWN_BLACK, ChessPiece.PAWN_WHITE):
            if abs(from_row - to_row) == 2:
                self.en_passant_square = (from_row + (to_row - from_row) // 2, from_col)
                en_passant_possible = True
            if to_square == self.en_passant_square:
                new_board_matrix[from_row][to_col] = ChessPiece.EMPTY
            if to_row in (0, 7):
                return self.promotion(to_square, new_board_matrix)

        if piece in (ChessPiece.KING_BLACK, ChessPiece.KING_WHITE):
            self.castling_rights[self.current_player]['kingside'] = False
            self.castling_rights[self.current_player]['queenside'] = False
        if piece in (ChessPiece.ROOK_WHITE, ChessPiece.ROOK_BLACK):
            if from_col == 0:
                self.castling_rights[self.current_player]['queenside'] = False
            elif from_col == 7:
                self.castling_rights[self.current_player]['kingside'] = False
        if not en_passant_possible:
            self.en_passant_square = None
            
        return new_board_matrix

    def switch_current_player(self):
        self.current_player = Color.WHITE if self.current_player == Color.BLACK else Color.BLACK

    def calculate_possible_moves(self, active_square, board_matrix):
        row, col = active_square
        piece = self.get_piece(active_square, board_matrix)
        possible_moves = []

        if piece in (ChessPiece.PAWN_BLACK, ChessPiece.PAWN_WHITE):
            direction = -1 if piece.value[0] == Color.WHITE.value else 1
            possible_moves += self.calculate_pawn_moves(row, col, direction, board_matrix)
        elif piece in (ChessPiece.ROOK_WHITE, ChessPiece.ROOK_BLACK):
            possible_moves += self.calculate_rook_moves(row, col, board_matrix)
        elif piece in (ChessPiece.KNIGHT_WHITE, ChessPiece.KNIGHT_BLACK):
            possible_moves += self.calculate_knight_moves(row, col, board_matrix)
        elif piece in (ChessPiece.BISHOP_WHITE, ChessPiece.BISHOP_BLACK):
            possible_moves += self.calculate_bishop_moves(row, col, board_matrix)
        elif piece in (ChessPiece.QUEEN_WHITE, ChessPiece.QUEEN_BLACK):
            possible_moves += self.calculate_rook_moves(row, col, board_matrix)
            possible_moves += self.calculate_bishop_moves(row, col, board_matrix)
        elif piece in (ChessPiece.KING_WHITE, ChessPiece.KING_BLACK):
            possible_moves += self.calculate_king_moves(row, col, board_matrix)

        return possible_moves

    def calculate_pawn_moves(self, row, col, direction, board_matrix):
        possible_moves = []

        if 0 <= row + direction < 8 and self.is_square_empty((row + direction, col), board_matrix):
            possible_moves.append((row + direction, col))

            if row == 6 and direction == -1 and self.is_square_empty((row + direction * 2, col), board_matrix):
                possible_moves.append((row + direction * 2, col))
            elif row == 1 and direction == 1 and self.is_square_empty((row + direction * 2, col), board_matrix):
                possible_moves.append((row + direction * 2, col))

        for d_col in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + d_col < 8:
                target_square = (row + direction, col + d_col)
                target_piece = self.get_piece(target_square, board_matrix)
                if (target_piece != ChessPiece.EMPTY and target_piece.value[0] != self.current_player.value) or (
                        target_square == self.en_passant_square):
                    possible_moves.append(target_square)

        return possible_moves

    def calculate_rook_moves(self, row, col, board_matrix):
        possible_moves = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_square = (r, c)
                target_piece = self.get_piece(target_square, board_matrix)
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append(target_square)
                elif target_piece.value[0] != self.current_player.value:
                    possible_moves.append(target_square)
                    break
                else:
                    break
                r += dr
                c += dc

        if col == 7 and self.can_castle_kingside(board_matrix):
            possible_moves.append((7, 4))

        if col == 0 and self.can_castle_queenside(board_matrix):
            possible_moves.append((7, 4))

        return possible_moves

    def calculate_knight_moves(self, row, col, board_matrix):
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        possible_moves = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_square = (r, c)
                target_piece = self.get_piece(target_square, board_matrix)
                if target_piece == ChessPiece.EMPTY or target_piece.value[0] != self.current_player.value:
                    possible_moves.append(target_square)

        return possible_moves

    def calculate_bishop_moves(self, row, col, board_matrix):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        possible_moves = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_square = (r, c)
                target_piece = self.get_piece(target_square, board_matrix)
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append(target_square)
                elif target_piece.value[0] != self.current_player.value:
                    possible_moves.append(target_square)
                    break
                else:
                    break
                r += dr
                c += dc

        return possible_moves

    def calculate_king_moves(self, row, col, board_matrix):
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        possible_moves = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_square = (r, c)
                target_piece = self.get_piece(target_square, board_matrix)
                if target_piece == ChessPiece.EMPTY or target_piece.value[0] != self.current_player.value:
                    if not self.is_protected(target_square, board_matrix):
                        possible_moves.append(target_square)

        castle_row_factor = 0 if self.current_player == Color.BLACK else 7

        if self.can_castle_kingside(board_matrix):
            possible_moves.append((castle_row_factor, 7))

        if self.can_castle_queenside(board_matrix):
            possible_moves.append((castle_row_factor, 0))

        return possible_moves

    def is_square_empty(self, square, board_matrix):
        return self.get_piece(square, board_matrix) == ChessPiece.EMPTY

    def is_protected(self, square, board_matrix):
        opponent_impact = []

        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c), board_matrix)
                if piece != ChessPiece.EMPTY and piece.value[0] != self.current_player.value:
                    possible_impact_squares = []
                    
                    if piece in (ChessPiece.PAWN_BLACK, ChessPiece.PAWN_WHITE):
                        direction = -1 if piece.value[0] == Color.WHITE.value else 1
                        possible_impact_squares += self.calculate_pawn_impact(r, c, direction, board_matrix)
                    elif piece in (ChessPiece.ROOK_WHITE, ChessPiece.ROOK_BLACK):
                        possible_impact_squares += self.calculate_rook_impact(r, c, board_matrix)
                    elif piece in (ChessPiece.KNIGHT_WHITE, ChessPiece.KNIGHT_BLACK):
                        possible_impact_squares += self.calculate_knight_impact(r, c, board_matrix)
                    elif piece in (ChessPiece.BISHOP_WHITE, ChessPiece.BISHOP_BLACK):
                        possible_impact_squares += self.calculate_bishop_impact(r, c, board_matrix)
                    elif piece in (ChessPiece.QUEEN_WHITE, ChessPiece.QUEEN_BLACK):
                        possible_impact_squares += self.calculate_rook_impact(r, c, board_matrix)
                        possible_impact_squares += self.calculate_bishop_impact(r, c, board_matrix)
                    elif piece in (ChessPiece.KING_WHITE, ChessPiece.KING_BLACK):
                        possible_impact_squares += self.calculate_king_impact(r, c, board_matrix)

                    opponent_impact += possible_impact_squares
                    

        return square in opponent_impact

    def calculate_pawn_impact(self, row, col, direction, board_matrix):
        impact_squares = []

        for d_col in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + d_col < 8:
                impact_squares.append((row + direction, col + d_col))

        return impact_squares

    def calculate_rook_impact(self, row, col, board_matrix):
        impact_squares = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if not self.is_square_empty((r, c), board_matrix):
                    impact_squares.append((r, c))
                    break
                impact_squares.append((r, c))
                r += dr
                c += dc

        return impact_squares

    def calculate_knight_impact(self, row, col, board_matrix):
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        impact_squares = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                impact_squares.append((r, c))

        return impact_squares

    def calculate_bishop_impact(self, row, col, board_matrix):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        impact_squares = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if not self.is_square_empty((r, c), board_matrix):
                    impact_squares.append((r, c))
                    break
                impact_squares.append((r, c))
                r += dr
                c += dc

        return impact_squares

    def calculate_king_impact(self, row, col, board_matrix):
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        impact_squares = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                impact_squares.append((r, c))

        return impact_squares

    def can_castle_kingside(self, board_matrix):
        if not self.castling_rights[self.current_player]['kingside']:
            return False

        row_factor = 7 if self.current_player == Color.WHITE else 0
        if not self.is_square_empty((row_factor, 5), board_matrix) or not self.is_square_empty((row_factor, 6), board_matrix):
            return False
        if self.is_protected((row_factor, 4), board_matrix) or self.is_protected((row_factor, 5), board_matrix) or self.is_protected((row_factor, 6), board_matrix):
            return False

        return True

    def can_castle_queenside(self, board_matrix):
        if not self.castling_rights[self.current_player]['queenside']:
            return False

        row_factor = 7 if self.current_player == Color.WHITE else 0
        if not self.is_square_empty((row_factor, 3), board_matrix) or not self.is_square_empty((row_factor, 2), board_matrix) or not self.is_square_empty((row_factor, 1), board_matrix):
            return False
        if self.is_protected((row_factor, 4), board_matrix) or self.is_protected((row_factor, 3), board_matrix) or self.is_protected((row_factor, 2), board_matrix):
            return False

        return True

    def perform_castle_kingside(self, board_matrix):
        row_factor = 7 if self.current_player == Color.WHITE else 0
        board_matrix[row_factor][4] = ChessPiece.EMPTY
        board_matrix[row_factor][7] = ChessPiece.EMPTY
        board_matrix[row_factor][6] = ChessPiece.KING_WHITE if self.current_player == Color.WHITE else ChessPiece.KING_BLACK
        board_matrix[row_factor][5] = ChessPiece.ROOK_WHITE if self.current_player == Color.WHITE else ChessPiece.ROOK_BLACK
        return board_matrix

    def perform_castle_queenside(self, board_matrix):
        row_factor = 7 if self.current_player == Color.WHITE else 0
        board_matrix[row_factor][4] = ChessPiece.EMPTY
        board_matrix[row_factor][0] = ChessPiece.EMPTY
        board_matrix[row_factor][2] = ChessPiece.KING_WHITE if self.current_player == Color.WHITE else ChessPiece.KING_BLACK
        board_matrix[row_factor][3] = ChessPiece.ROOK_WHITE if self.current_player == Color.WHITE else ChessPiece.ROOK_BLACK
        return board_matrix

    def promotion(self, promotion_square, board_matrix):
        row, col = promotion_square
        promotion_piece = self.board.select_promotion_piece(self.current_player)
        board_matrix[row][col] = promotion_piece
        return board_matrix
        
    def get_king_square(self, color, board_matrix):
        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c), board_matrix)
                if (piece == ChessPiece.KING_BLACK and color == Color.BLACK) or (piece ==ChessPiece.KING_WHITE and color == Color.WHITE):
                    return (r, c)

    def is_in_check(self, board_matrix):
        return self.is_protected(self.get_king_square(self.current_player, board_matrix), board_matrix)
    
    def is_checkmate(self, board_matrix):
        king_square = self.get_king_square(self.current_player, board_matrix)
        temp_board = copy.deepcopy(board_matrix)
        
        
        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c), board_matrix)
                if piece != ChessPiece.EMPTY and piece.value[0] == self.current_player.value:
                    for move in self.calculate_possible_moves((r, c), board_matrix):
                        temp_board = self.move_piece((r, c), move, temp_board)
                        if self.is_in_check(temp_board) == False:
                            return False
                        temp_board = copy.deepcopy(board_matrix)
        
        self.winner_square = self.get_king_square(Color.BLACK if self.current_player == Color.WHITE else Color.WHITE, board_matrix)
        
        return True
    
    def move_doesnt_cause_check(self):
        #vell spass zuekonfts dani