from board import Board
import pygame
import sys

board = Board()
pygame.init()
running = True
board_matrix = {'PAWN_BLACK': 326400, 'ROOK_BLACK': 129, 'KNIGHT_BLACK': 66, 'BISHOP_BLACK': 36, 'QUEEN_BLACK': 8, 'KING_BLACK': 16, 'PAWN_WHITE': 67272588153323520, 'ROOK_WHITE': 9295429630892703744, 'KNIGHT_WHITE': 144150372447944704, 'BISHOP_WHITE': 2594073385365405696, 'QUEEN_WHITE': 576460752303423488, 'KING_WHITE': 1152921504606846976, 'casteling_rights': 15, 'en_passant_position': None, 'last_capture_or_pawn_move': None, 'all_pieces': 13830308233769974783}

board.update_board(board_matrix, None, [], None, [], None, 0)
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
sys.exit()
