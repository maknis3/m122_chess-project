import pygame
from pygame.locals import *
from pieces import ChessPiece, Color

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class Board:
    def __init__(self):
        self.rows = 8
        self.cols = 8
        self.square_size = WIDTH // self.cols
        self.colors = [WHITE, GRAY]
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

    def update_board(self, chess_pieces, clicked_square, possible_moves):
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.colors[(row + col) % 2]
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
