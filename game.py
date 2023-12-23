import pygame
import sys
from board import Board
from pieces import ChessPiece, Color

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
                        if piece.value[0] == self.current_player.value:
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
        
        if 0 <= row + direction < 8 and self.board_matrix[row + direction][col] == ChessPiece.EMPTY:
            possible_moves.append((row + direction, col))
            
            if row == 6 and direction == -1 and self.board_matrix[row + direction * 2][col] == ChessPiece.EMPTY:
                possible_moves.append((row + direction * 2, col))
            elif row == 1 and direction == 1 and self.board_matrix[row + direction * 2][col] == ChessPiece.EMPTY:
                possible_moves.append((row + direction * 2, col))
            
        for d_col in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + d_col < 8:
                target_piece = self.board_matrix[row + direction][col + d_col]
                if target_piece != ChessPiece.EMPTY and target_piece.value[0] != self.current_player.value:
                    possible_moves.append((row + direction, col + d_col))
        
        return possible_moves
    
    def calculate_rook_moves(self, row, col):
        possible_moves = []
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_piece = self.board_matrix[r][c]
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append((r, c))
                elif self.is_opponent_piece(self.board_matrix[row][col], target_piece):
                    possible_moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        
        return possible_moves
    
    def calculate_knight_moves(self, row, col):
        moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        possible_moves = []
        
        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = self.board_matrix[r][c]
                if target_piece == ChessPiece.EMPTY or self.is_opponent_piece(self.board_matrix[row][col], target_piece):
                    possible_moves.append((r, c))
        
        return possible_moves
    
    def calculate_bishop_moves(self, row, col):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        possible_moves = []
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target_piece = self.board_matrix[r][c]
                if target_piece == ChessPiece.EMPTY:
                    possible_moves.append((r, c))
                elif self.is_opponent_piece(self.board_matrix[row][col], target_piece):
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
                target_piece = self.board_matrix[r][c]
                opponent_color = Color.BLACK if self.board_matrix[row][col] == ChessPiece.KING_WHITE else Color.WHITE
                if target_piece == ChessPiece.EMPTY or self.is_opponent_piece(self.board_matrix[row][col], target_piece):
                    # Check if the square is not attacked by an opponent
                    if not self.square_attacked_by_opponent((r, c), opponent_color):
                        possible_moves.append((r, c))
        
        return possible_moves
    
    def square_attacked_by_opponent(self, square, opponent_color):
        target_row, target_col = square

        if opponent_color == self.current_player:
            return False
        
        for row in range(8):
            for col in range(8):
                piece = self.board_matrix[row][col]

                if piece != ChessPiece.EMPTY and piece.value[0] == opponent_color.value:
                    moves = self.calculate_possible_moves((row, col))
                    if square in moves:
                        return True

        return False
    
    def move_piece(self, from_square, to_square):
        from_row, from_col = from_square
        to_row, to_col = to_square
        self.board_matrix[to_row][to_col] = self.board_matrix[from_row][from_col]
        self.board_matrix[from_row][from_col] = ChessPiece.EMPTY
