import os
import pygame
from pygame.locals import *
import sys
from board import Board

pygame.init()

class Game:
    def __init__(self):
        self.board = Board()

    def start_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.board.update_board()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
