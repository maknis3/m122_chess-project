import pygame
import sys

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
DARK_GRAY = (64, 64, 64)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")

# Load chess piece images
pieces = {
    "wp": pygame.image.load("images/white-pawn.png"),
    "wki": pygame.image.load("images/white-king.png"),
    "wq": pygame.image.load("images/white-queen.png"),
    "wr": pygame.image.load("images/white-rook.png"),
    "wb": pygame.image.load("images/white-bishop.png"),
    "wkn": pygame.image.load("images/white-knight.png"),
    "bp": pygame.image.load("images/black-pawn.png"),
    "bki": pygame.image.load("images/black-king.png"),
    "bq": pygame.image.load("images/black-queen.png"),
    "br": pygame.image.load("images/black-rook.png"),
    "bb": pygame.image.load("images/black-bishop.png"),
    "bkn": pygame.image.load("images/black-knight.png")
}

class Board:
    def __init__(self):
        self.rows = 8
        self.cols = 8
        self.square_size = WIDTH // self.cols
        self.colors = [(255, 255, 255), (169, 169, 169)]
        self.chess_pieces = [
            ["wr", "wkn", "wb", "wq", "wki", "wb", "wkn", "wr"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["br", "bkn", "bb", "bq", "bki", "bb", "bkn", "br"]
        ]

    def update_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.colors[(row + col) % 2]
                pygame.draw.rect(screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

                piece = self.chess_pieces[row][col]
                if piece:
                    piece_image = pieces.get(piece)
                    if piece_image:
                        screen.blit(piece_image, (col * self.square_size, row * self.square_size))
