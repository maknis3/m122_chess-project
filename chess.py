import pygame
import sys
import copy
from collections import Counter
from board import Board
from pieces import ChessPiece, Color

class Chess:
    def __init__(self, board):
        self.castling_rights = {
            Color.WHITE: {'kingside': True, 'queenside': True},
            Color.BLACK: {'kingside': True, 'queenside': True}
        }
        self.board_archive = []
        self.last_capture_or_pawn_move = 0
        self.board = board

    def is_valid_square(self, square, board_matrix, player):
        piece = self.get_piece(square, board_matrix)
        return (piece != ChessPiece.EMPTY) and (piece.value[0] == player.value)

    def get_piece(self, square, board_matrix):
        row, col = square
        return board_matrix[row][col]

    def move_piece(self, from_square, to_square, board_matrix, local_en_passant_square, player, promotion_piece = None, actual_move = False, move_counter = -1):
        new_board_matrix = copy.deepcopy(board_matrix)
        from_row, from_col = from_square
        to_row, to_col = to_square
        piece = self.get_piece(from_square, new_board_matrix)
        
        if actual_move and ((piece in (ChessPiece.PAWN_BLACK, ChessPiece.PAWN_WHITE)) or self.get_piece(to_square, new_board_matrix) != ChessPiece.EMPTY):
            self.last_capture_or_pawn_move = move_counter

        # en passant & promotion:
        if piece in (ChessPiece.PAWN_BLACK, ChessPiece.PAWN_WHITE):
            if to_square == local_en_passant_square:
                new_board_matrix[from_row][to_col] = ChessPiece.EMPTY
            if abs(from_row - to_row) == 2:
                local_en_passant_square = (from_row + (to_row - from_row) // 2, from_col)
            else:
                local_en_passant_square = None
            if to_row in (0, 7):
                return (self.promotion(to_square, new_board_matrix, promotion_piece, player), local_en_passant_square)
        else:
            local_en_passant_square = None

        # castle:
        if piece in [ChessPiece.KING_BLACK, ChessPiece.KING_WHITE, ChessPiece.ROOK_WHITE, ChessPiece.ROOK_BLACK]:
            if self.can_castle_kingside(new_board_matrix, player) and ((from_col == 4 and to_col == 7) or (from_col == 7 and to_col == 4)):
                new_board_matrix = self.perform_castle_kingside(new_board_matrix, actual_move, player)
                return (new_board_matrix, local_en_passant_square) 
            if self.can_castle_queenside(new_board_matrix, player) and ((from_col == 4 and to_col == 0) or (from_col == 0 and to_col == 4)):
                new_board_matrix = self.perform_castle_queenside(new_board_matrix, actual_move, player)
                return (new_board_matrix, local_en_passant_square)
        if actual_move and (piece in (ChessPiece.KING_BLACK, ChessPiece.KING_WHITE)):
            self.castling_rights[player]['kingside'] = False
            self.castling_rights[player]['queenside'] = False
        if actual_move and (piece in (ChessPiece.ROOK_WHITE, ChessPiece.ROOK_BLACK)):
            if from_col == 0:
                self.castling_rights[player]['queenside'] = False
            elif from_col == 7:
                self.castling_rights[player]['kingside'] = False

        #basic move:
        new_board_matrix[to_row][to_col] = new_board_matrix[from_row][from_col]
        new_board_matrix[from_row][from_col] = ChessPiece.EMPTY
            
        return (new_board_matrix, local_en_passant_square)

    def calculate_possible_moves(self, active_square, board_matrix, temp_en_passant_square, player):
        row, col = active_square
        piece = self.get_piece(active_square, board_matrix)
        possible_moves = []

        if piece in (ChessPiece.PAWN_BLACK, ChessPiece.PAWN_WHITE):
            direction = -1 if piece.value[0] == Color.WHITE.value else 1
            possible_moves += self.calculate_pawn_moves(row, col, direction, board_matrix, temp_en_passant_square, player)
        elif piece in (ChessPiece.ROOK_WHITE, ChessPiece.ROOK_BLACK):
            possible_moves += self.calculate_rook_moves(row, col, board_matrix, player)
        elif piece in (ChessPiece.KNIGHT_WHITE, ChessPiece.KNIGHT_BLACK):
            possible_moves += self.calculate_knight_moves(row, col, board_matrix, player)
        elif piece in (ChessPiece.BISHOP_WHITE, ChessPiece.BISHOP_BLACK):
            possible_moves += self.calculate_bishop_moves(row, col, board_matrix, player)
        elif piece in (ChessPiece.QUEEN_WHITE, ChessPiece.QUEEN_BLACK):
            possible_moves += self.calculate_rook_moves(row, col, board_matrix, player)
            possible_moves += self.calculate_bishop_moves(row, col, board_matrix, player)
        elif piece in (ChessPiece.KING_WHITE, ChessPiece.KING_BLACK):
            possible_moves += self.calculate_king_moves(row, col, board_matrix, player)

        return list(filter(lambda move: not self.move_does_cause_check(active_square, move, board_matrix, temp_en_passant_square, player), possible_moves))

    def calculate_pawn_moves(self, row, col, direction, board_matrix, temp_en_passant_square, player):
        possible_moves = []

        for d_col in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + d_col < 8:
                target_square = (row + direction, col + d_col)
                target_piece = self.get_piece(target_square, board_matrix)
                if (target_piece != ChessPiece.EMPTY and target_piece.value[0] != player.value) or (target_square == temp_en_passant_square):
                    possible_moves.append(target_square)

        if 0 <= row + direction < 8 and self.is_square_empty((row + direction, col), board_matrix):
            possible_moves.append((row + direction, col))

            if row == 6 and direction == -1 and self.is_square_empty((row + direction * 2, col), board_matrix):
                possible_moves.append((row + direction * 2, col))
            elif row == 1 and direction == 1 and self.is_square_empty((row + direction * 2, col), board_matrix):
                possible_moves.append((row + direction * 2, col))

        return possible_moves

    def calculate_rook_moves(self, row, col, board_matrix, player):
        possible_moves = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_square = (r, c)
                target_piece = self.get_piece(target_square, board_matrix)
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append(target_square)
                elif target_piece.value[0] != player.value:
                    possible_moves.append(target_square)
                    break
                else:
                    break
                r += dr
                c += dc

        if (col == 7 and self.can_castle_kingside(board_matrix, player)) or (col == 0 and self.can_castle_queenside(board_matrix, player)):
            possible_moves.append((row, 4))

        return possible_moves

    def calculate_knight_moves(self, row, col, board_matrix, player):
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        possible_moves = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_square = (r, c)
                target_piece = self.get_piece(target_square, board_matrix)
                if target_piece == ChessPiece.EMPTY or target_piece.value[0] != player.value:
                    possible_moves.append(target_square)

        return possible_moves

    def calculate_bishop_moves(self, row, col, board_matrix, player):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        possible_moves = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_square = (r, c)
                target_piece = self.get_piece(target_square, board_matrix)
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append(target_square)
                elif target_piece.value[0] != player.value:
                    possible_moves.append(target_square)
                    break
                else:
                    break
                r += dr
                c += dc

        return possible_moves

    def calculate_king_moves(self, row, col, board_matrix, player):
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        possible_moves = []

        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_square = (r, c)
                target_piece = self.get_piece(target_square, board_matrix)
                if target_piece == ChessPiece.EMPTY or target_piece.value[0] != player.value:
                    possible_moves.append(target_square)

        castle_row_factor = 0 if player == Color.BLACK else 7

        if self.can_castle_kingside(board_matrix, player):
            possible_moves.append((castle_row_factor, 7))

        if self.can_castle_queenside(board_matrix, player):
            possible_moves.append((castle_row_factor, 0))

        return possible_moves

    def is_square_empty(self, square, board_matrix):
        return self.get_piece(square, board_matrix) == ChessPiece.EMPTY
    
    def is_valid_move(self, from_square, to_square, board_matrix, en_passant_square, player):
        possible_moves = self.calculate_possible_moves(from_square, board_matrix, en_passant_square, player)
        return to_square in possible_moves

    def is_protected(self, square, board_matrix, player):
        opponent_impact = []

        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c), board_matrix)
                if piece != ChessPiece.EMPTY and piece.value[0] != player.value:
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

    def can_castle_kingside(self, board_matrix, player):
        if not self.castling_rights[player]['kingside']:
            return False

        castle_row_factor = 0 if player == Color.BLACK else 7
        
        if not self.is_square_empty((castle_row_factor, 5), board_matrix) or not self.is_square_empty((castle_row_factor, 6), board_matrix):
            return False
        if self.is_protected((castle_row_factor, 4), board_matrix, player) or self.is_protected((castle_row_factor, 5), board_matrix, player) or self.is_protected((castle_row_factor, 6), board_matrix, player):
            return False

        return True

    def can_castle_queenside(self, board_matrix, player):
        if not self.castling_rights[player]['queenside']:
            return False

        castle_row_factor = 0 if player == Color.BLACK else 7

        if not self.is_square_empty((castle_row_factor, 3), board_matrix) or not self.is_square_empty((castle_row_factor, 2), board_matrix) or not self.is_square_empty((castle_row_factor, 1), board_matrix):
            return False
        if self.is_protected((castle_row_factor, 4), board_matrix, player) or self.is_protected((castle_row_factor, 3), board_matrix, player) or self.is_protected((castle_row_factor, 2), board_matrix, player):
            return False

        return True

    def perform_castle_kingside(self, board_matrix, actual_move, player):
        temp_board = copy.deepcopy(board_matrix)
        row_factor = 7 if player == Color.WHITE else 0
        temp_board[row_factor][4] = ChessPiece.EMPTY
        temp_board[row_factor][7] = ChessPiece.EMPTY
        temp_board[row_factor][6] = ChessPiece.KING_WHITE if player == Color.WHITE else ChessPiece.KING_BLACK
        temp_board[row_factor][5] = ChessPiece.ROOK_WHITE if player == Color.WHITE else ChessPiece.ROOK_BLACK
        if actual_move:
            self.castling_rights[player]['kingside'] = False
            self.castling_rights[player]['queenside'] = False
        return temp_board

    def perform_castle_queenside(self, board_matrix, actual_move, player):
        temp_board = copy.deepcopy(board_matrix)
        row_factor = 7 if player == Color.WHITE else 0
        temp_board[row_factor][4] = ChessPiece.EMPTY
        temp_board[row_factor][0] = ChessPiece.EMPTY
        temp_board[row_factor][2] = ChessPiece.KING_WHITE if player == Color.WHITE else ChessPiece.KING_BLACK
        temp_board[row_factor][3] = ChessPiece.ROOK_WHITE if player == Color.WHITE else ChessPiece.ROOK_BLACK
        if actual_move:
            self.castling_rights[player]['kingside'] = False
            self.castling_rights[player]['queenside'] = False
        return temp_board

    def promotion(self, promotion_square, board_matrix, promotion_piece, player):
        row, col = promotion_square
        if promotion_piece == None:
            promotion_piece = self.board.select_promotion_piece(player)
        board_matrix[row][col] = promotion_piece
        return board_matrix
        
    def get_king_square(self, color, board_matrix):
        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c), board_matrix)
                if (piece == ChessPiece.KING_BLACK and color == Color.BLACK) or (piece ==ChessPiece.KING_WHITE and color == Color.WHITE):
                    return (r, c)

    def is_in_check(self, board_matrix, player):
        return self.is_protected(self.get_king_square(player, board_matrix), board_matrix, player)
    
    def is_checkmate(self, board_matrix, en_passant_square, player):
        temp_board = copy.deepcopy(board_matrix)
        temp_en_passant_square = en_passant_square
        
        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c), board_matrix)
                if piece != ChessPiece.EMPTY and piece.value[0] == player.value:
                    for move in self.calculate_possible_moves((r, c), board_matrix, temp_en_passant_square, player):
                        if piece in (ChessPiece.PAWN_BLACK, ChessPiece.PAWN_WHITE) and r in (1, 6):
                            promotion_piece = ChessPiece.QUEEN_BLACK if player == Color.BLACK else ChessPiece.QUEEN_WHITE
                            temp_board = copy.deepcopy(board_matrix)
                            temp_en_passant_square = en_passant_square
                            (temp_board, temp_en_passant_square) = self.move_piece((r, c), move, temp_board, temp_en_passant_square, player, promotion_piece)
                            if self.is_in_check(temp_board, player) == False:
                                return False
                            continue
                        temp_en_passant_square = en_passant_square
                        temp_board = copy.deepcopy(board_matrix)
                        (temp_board, temp_en_passant_square) = self.move_piece((r, c), move, temp_board, temp_en_passant_square, player)
                        if self.is_in_check(temp_board, player) == False:
                            return False
        return True
    
    def move_does_cause_check(self, from_square, to_square, board_matrix, temp_en_passant_square, player):
        temp_board = copy.deepcopy(board_matrix)
        promotion_piece = ChessPiece.QUEEN_BLACK if player == Color.BLACK else ChessPiece.QUEEN_WHITE
        
        (temp_board, temp_en_passant_square) = self.move_piece(from_square, to_square, temp_board, temp_en_passant_square, player, promotion_piece)
        
        return self.is_in_check(temp_board, player)
    
    def is_stalemate(self, board_matrix, en_passant_square, player):
        for r in range(8):
            for c in range(8):
                piece = self.get_piece((r, c), board_matrix)
                if piece != ChessPiece.EMPTY and piece.value[0] == player.value:
                    if len(self.calculate_possible_moves((r, c), board_matrix, en_passant_square, player)) > 0:
                        return False
        return True
    
    def archive_board(self, board_matrix):
        self.board_archive.append(hash(str(board_matrix)))
        
    def check_threefold_repetition(self):
        if Counter(self.board_archive).most_common(1)[0][1] >= 3:
            return True
        return False
        
    def check_50_move_rule(self, move_counter):
        if move_counter - self.last_capture_or_pawn_move >= 100:
            return True
        return False
        