import pygame
from chess_game import ChessGame
from pieces import ChessPiece, Color

if __name__ == "__main__":
    game = ChessGame()
    game.board_matrix = [
        [ChessPiece.EMPTY] * 8,
        [ChessPiece.EMPTY] * 8,
        [ChessPiece.EMPTY] * 8,
        [ChessPiece.EMPTY] * 8,
        [ChessPiece.EMPTY] * 8,
        [ChessPiece.EMPTY] * 8,
        [ChessPiece.EMPTY] * 8,
        [ChessPiece.EMPTY] * 8
    ]
    pygame.init()
    game.board.update_board(game.board_matrix, (-1, -1), (), None, None)
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.quit()
