import pygame
from pygame.locals import *
from pieces import ChessPiece, Color

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

class Board:
    def __init__(self):
        self.rows = 8
        self.cols = 8
        self.colors = [WHITE, GRAY]
        self.square_size = WIDTH // self.cols
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chessboard")
        self.pieces_images = {
            ChessPiece.PAWN_WHITE: pygame.image.load("images/white-pawn.png"),
            ChessPiece.KING_WHITE: pygame.image.load("images/white-king.png"),
            ChessPiece.QUEEN_WHITE: pygame.image.load("images/white-queen.png"),
            ChessPiece.ROOK_WHITE: pygame.image.load("images/white-rook.png"),
            ChessPiece.BISHOP_WHITE: pygame.image.load("images/white-bishop.png"),
            ChessPiece.KNIGHT_WHITE: pygame.image.load("images/white-knight.png"),
            ChessPiece.PAWN_BLACK: pygame.image.load("images/black-pawn.png"),
            ChessPiece.KING_BLACK: pygame.image.load("images/black-king.png"),
            ChessPiece.QUEEN_BLACK: pygame.image.load("images/black-queen.png"),
            ChessPiece.ROOK_BLACK: pygame.image.load("images/black-rook.png"),
            ChessPiece.BISHOP_BLACK: pygame.image.load("images/black-bishop.png"),
            ChessPiece.KNIGHT_BLACK: pygame.image.load("images/black-knight.png")
        }

    def update_board(self, chess_pieces, clicked_square, possible_moves, check_square, winner_square):
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.colors[(row + col) % 2]
                if (row, col) == check_square:
                    color = ORANGE
                elif winner_square != None and ((row, col) == winner_square or (row, col) in winner_square):
                    color = GREEN
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

                piece = chess_pieces[row][col]

                if piece:
                    piece_image = self.pieces_images.get(piece)
                    if piece_image:
                        self.screen.blit(piece_image, (col * self.square_size, row * self.square_size))

        if clicked_square is not None:
            row, col = clicked_square
            pygame.draw.rect(self.screen, RED, (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3)  # Highlight the clicked square in red

        for square in possible_moves:
            row, col = square
            pygame.draw.rect(self.screen, BLUE, (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3)
            
    def reset_screen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chessboard")
            
    def select_promotion_piece(self, current_player):

        promotion_screen = pygame.display.set_mode((400, 100))
        pygame.display.set_caption("Promotion")

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return None
                if event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 0 <= mouse_x <= 100:
                        self.reset_screen()
                        return ChessPiece.ROOK_BLACK if current_player == Color.BLACK else ChessPiece.ROOK_WHITE 
                    elif 100 < mouse_x <= 200:
                        self.reset_screen()
                        return ChessPiece.KNIGHT_BLACK if current_player == Color.BLACK else ChessPiece.KNIGHT_WHITE 
                    elif 200 < mouse_x <= 300:
                        self.reset_screen()
                        return ChessPiece.BISHOP_BLACK if current_player == Color.BLACK else ChessPiece.BISHOP_WHITE 
                    elif 300 < mouse_x <= 400:
                        self.reset_screen()
                        return ChessPiece.QUEEN_BLACK if current_player == Color.BLACK else ChessPiece.QUEEN_WHITE 

            promotion_screen.fill(WHITE)
            
            if current_player == Color.BLACK:
                pieces = (ChessPiece.ROOK_BLACK, ChessPiece.KNIGHT_BLACK, ChessPiece.BISHOP_BLACK,  ChessPiece.QUEEN_BLACK)
            else:
                pieces = (ChessPiece.ROOK_WHITE, ChessPiece.KNIGHT_WHITE, ChessPiece.BISHOP_WHITE, ChessPiece.QUEEN_WHITE)
            
            for col in range(4):
                color = self.colors[col % 2]
                pygame.draw.rect(self.screen, color, (col * self.square_size, 0, self.square_size, self.square_size))
                piece_image = self.pieces_images.get(pieces[col])
                if piece_image:
                    self.screen.blit(piece_image, (col * self.square_size, 0))

            pygame.display.flip()