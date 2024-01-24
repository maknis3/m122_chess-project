import pygame
import sys
from pygame.locals import *
import math

CHESS_WIDTH, CHESS_HEIGHT = 800, 800
MENU_WIDTH = 350
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
DARK_GRAY = (120, 120, 120)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (191, 239, 255)
DARK_BLUE = (104, 131, 139)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

class Board:
    def __init__(self):
        self.square_size = CHESS_HEIGHT // 8
        self.screen = pygame.display.set_mode((CHESS_WIDTH + MENU_WIDTH, CHESS_HEIGHT))
        pygame.display.set_caption("Chessboard")
        self.pieces_images = {
            "PAWN_WHITE": pygame.image.load("images/white-pawn.png"),
            "KING_WHITE": pygame.image.load("images/white-king.png"),
            "QUEEN_WHITE": pygame.image.load("images/white-queen.png"),
            "ROOK_WHITE": pygame.image.load("images/white-rook.png"),
            "BISHOP_WHITE": pygame.image.load("images/white-bishop.png"),
            "KNIGHT_WHITE": pygame.image.load("images/white-knight.png"),
            "PAWN_BLACK": pygame.image.load("images/black-pawn.png"),
            "KING_BLACK": pygame.image.load("images/black-king.png"),
            "QUEEN_BLACK": pygame.image.load("images/black-queen.png"),
            "ROOK_BLACK": pygame.image.load("images/black-rook.png"),
            "BISHOP_BLACK": pygame.image.load("images/black-bishop.png"),
            "KNIGHT_BLACK": pygame.image.load("images/black-knight.png")
        }
        self.menu_images = {
            "left": pygame.image.load("images/left.png"),
            "right": pygame.image.load("images/right.png"),
            "far_right": pygame.image.load("images/far_right.png")
        }
        self.color_selection_options = {
            "WHITE": pygame.image.load("images/white_selection.png"),
            "BLACK": pygame.image.load("images/black_selection.png")
        }
        self.playmode_selection_icons = {
            "SINGLE": pygame.image.load("images/singleplayer_icon.png"),
            "MULTI": pygame.image.load("images/multiplayer_icon.png")
        }
        self.menu_buttons = {}
        self.board_flip = False

    def update_board(self, chess_pieces, selected_square, possible_moves, check_position, winner_positions, white_turn, move_counter):
        self.draw_board(check_position, winner_positions, possible_moves)
        self.draw_pieces(chess_pieces)
        if selected_square:
            self.mark_selected_square(selected_square)
        self.load_menu(white_turn, move_counter, winner_positions != [])

    def draw_board(self, check_position, winner_positions, possible_moves):
        check_square = None
        winner_squares = []
        possible_squares = []
        
        for move in possible_moves:
            square = self.position_to_square(move)
            
            if self.board_flip:
                y = (7 - square[0])
                x = (7 - square[1])
            else:
                y = square[0]
                x = square[1]
                
            possible_squares.append((y, x))
        
        if check_position:
            check_square = self.position_to_square(check_position)
        if winner_positions != []:
            for position in winner_positions:
                winner_squares.append(self.position_to_square(position))
        square_colors = [WHITE, GRAY]
        possible_square_colors = [LIGHT_BLUE, DARK_BLUE]
        
        for row in range(8):
            for col in range(8):
                color = square_colors[(row + col) % 2]
                if (row, col) == check_square:
                    color = ORANGE
                elif (row, col) in winner_squares:
                    color = GREEN
                elif (row, col) in possible_squares:
                    color = possible_square_colors[(row + col) % 2]
                
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def draw_pieces(self, board_matrix):
        for piece, bitboard in board_matrix.items():
            if piece in ("casteling_rights", "en_passant_position", "last_capture_or_pawn_move", "all_pieces"):
                continue
            for position in range(64):
                if self.board_flip:
                    row = 7 - (position // 8)
                    col = 7 - (position % 8)
                else:
                    row = position // 8
                    col = position % 8
                if bitboard & (1 << position):
                    x = col * self.square_size
                    y = row * self.square_size
                    self.screen.blit(self.pieces_images[piece], (x, y))
                    
    def mark_selected_square(self, selected_square):
        row, col = self.position_to_square(selected_square)
        x = col * self.square_size
        y = row * self.square_size
        
        pygame.draw.rect(self.screen, RED, (x, y, self.square_size, self.square_size), 4)
        
    def position_to_square(self, position): # Convert a position (bit index) to a square (row, col)
        return int(math.log(position, 2) // 8), int(math.log(position, 2) % 8)

    def load_menu(self, white_turn, move_counter, game_finished):
        pygame.draw.rect(self.screen, DARK_GRAY, (CHESS_WIDTH, 0, MENU_WIDTH, CHESS_HEIGHT))
        
        circle_radius = 35
        circle_distance_border = 50
        if self.board_flip:
            white_circle_pos = (CHESS_WIDTH + circle_distance_border, circle_distance_border)
            black_circle_pos = (CHESS_WIDTH + circle_distance_border, CHESS_HEIGHT - circle_distance_border)
        else:
            white_circle_pos = (CHESS_WIDTH + circle_distance_border, CHESS_HEIGHT - circle_distance_border)
            black_circle_pos = (CHESS_WIDTH + circle_distance_border, circle_distance_border)
        
        if white_turn != None and not game_finished:
            if white_turn:
                pygame.draw.circle(self.screen, WHITE, white_circle_pos, circle_radius)
            else:
                pygame.draw.circle(self.screen, BLACK, black_circle_pos, circle_radius)
        
        border_gap = 30
        
        font_size = 42
        text_x, text_y = CHESS_WIDTH + border_gap, (CHESS_HEIGHT / 2) - (font_size - 5)
        font = pygame.font.SysFont(None, font_size)
        text_surface = font.render("move: " + str(int(move_counter/2) + 1), True, WHITE, None)
        self.screen.blit(text_surface, (text_x, text_y))
        
        buttons = {}
        button_list = ["left", "right", "far_right"]
        color_button = GRAY
        button_width, button_height = 84, 84
        button_gap = 20
        start_x, start_y = CHESS_WIDTH + border_gap, (CHESS_HEIGHT / 2) + 10
        x = start_x
        for button_type in button_list:
            rect = pygame.Rect(x, start_y, button_width, button_height)
            buttons[button_type] = rect
            pygame.draw.rect(self.screen, color_button, rect)
            self.screen.blit(self.menu_images[button_type], (x + 10, start_y + 10))
            
            x += button_width + button_gap
        
        self.menu_buttons = buttons
        
    def get_menu_buttons(self):
        return self.menu_buttons
                
        
    def get_promotion_piece(self, color):
        promotion_pieces = ["QUEEN", "ROOK", "BISHOP", "KNIGHT"]
        selected_piece_type = None

        button_width, button_height = 120, 120
        button_gap = 20
        start_x = CHESS_WIDTH + (MENU_WIDTH - button_width) / 2
        start_y = (CHESS_HEIGHT - (len(promotion_pieces) * button_height) - ((len(promotion_pieces) - 1) * button_gap)) / 2  # Adjust as necessary to fit in your menu

        buttons = {}

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for piece, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            selected_piece_type = piece
                            running = False

            color_button = GRAY
            pygame.draw.rect(self.screen, DARK_GRAY, (CHESS_WIDTH, 0, MENU_WIDTH, CHESS_HEIGHT))
            text_x, text_y = start_x - 25, start_y - 70
            font_size = 42
            font = pygame.font.SysFont(None, font_size)
            text_surface = font.render("pick a piece", True, WHITE, None)
            self.screen.blit(text_surface, (text_x, text_y))
            y = start_y
            for piece in promotion_pieces:
                rect = pygame.Rect(start_x, y, button_width, button_height)
                buttons[piece] = rect
                pygame.draw.rect(self.screen, color_button, rect)
                self.screen.blit(self.pieces_images[piece + "_" + color], (start_x + 10, y + 10))

                y += button_height + button_gap 

            pygame.display.flip()

        return selected_piece_type

    def color_selection(self):
        selected_color = None
        
        button_type = ["WHITE", "BLACK"]
        button_width, button_height = 200, 200
        button_gap = (CHESS_HEIGHT / 2) - button_height
        start_x = (CHESS_WIDTH + MENU_WIDTH - button_width) / 2
        start_y = ((CHESS_HEIGHT / 2) - button_height) / 2

        buttons = {}
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for color, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            selected_color = color
                            running = False

            pygame.draw.rect(self.screen, GRAY, (0, 0, MENU_WIDTH + CHESS_WIDTH, CHESS_HEIGHT/2))
            pygame.draw.rect(self.screen, WHITE, (0, CHESS_HEIGHT/2, MENU_WIDTH + CHESS_WIDTH, CHESS_HEIGHT))

            text_one_x, text_one_y = (CHESS_WIDTH / 2) + 25, (CHESS_HEIGHT / 2) - 50
            text_two_x, text_two_y = (CHESS_WIDTH / 2) + 55, (CHESS_HEIGHT / 2) + 20
            font_size = 42
            font = pygame.font.SysFont(None, font_size)
            text_surface = font.render("welcome to mychess", True, BLACK, None)
            self.screen.blit(text_surface, (text_one_x, text_one_y))
            text_surface = font.render("select your color", True, BLACK, None)
            self.screen.blit(text_surface, (text_two_x, text_two_y))
            
            y = start_y
            for color in button_type:
                rect = pygame.Rect(start_x, y, button_width, button_height)
                buttons[color] = rect
                button_color = WHITE if color == "WHITE" else GRAY
                pygame.draw.rect(self.screen, button_color, rect)
                self.screen.blit(self.color_selection_options[color], (start_x + 20, y + 20))

                y += button_height + button_gap

            pygame.display.flip()

        if selected_color == "BLACK":
            self.board_flip = True
        
        return selected_color
    
    def playmode_selection(self):
        selected_mode = None
        
        button_type = ["SINGLE", "MULTI"]
        button_width, button_height = 200, 200
        button_gap = (CHESS_HEIGHT / 2) - button_height
        start_x = (CHESS_WIDTH + MENU_WIDTH - button_width) / 2
        start_y = ((CHESS_HEIGHT / 2) - button_height) / 2

        buttons = {}
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for mode, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            selected_mode = mode
                            running = False

            pygame.draw.rect(self.screen, GRAY, (0, 0, MENU_WIDTH + CHESS_WIDTH, CHESS_HEIGHT/2))
            pygame.draw.rect(self.screen, WHITE, (0, CHESS_HEIGHT/2, MENU_WIDTH + CHESS_WIDTH, CHESS_HEIGHT))

            text_one_x, text_one_y = (CHESS_WIDTH / 2) + 25, (CHESS_HEIGHT / 2) - 50
            text_two_x, text_two_y = (CHESS_WIDTH / 2) + 55, (CHESS_HEIGHT / 2) + 20
            font_size = 42
            font = pygame.font.SysFont(None, font_size)
            text_surface = font.render("welcome to mychess", True, BLACK, None)
            self.screen.blit(text_surface, (text_one_x, text_one_y))
            text_surface = font.render("select play-mode", True, BLACK, None)
            self.screen.blit(text_surface, (text_two_x, text_two_y))
            
            y = start_y
            for mode in button_type:
                rect = pygame.Rect(start_x, y, button_width, button_height)
                buttons[mode] = rect
                button_color = WHITE if mode == "SINGLE" else GRAY
                pygame.draw.rect(self.screen, button_color, rect)
                self.screen.blit(self.playmode_selection_icons[mode], (start_x + 36, y + 36))

                y += button_height + button_gap

            pygame.display.flip()

        if selected_mode == "MULTI":
            self.board_flip = False
        
        return selected_mode == "SINGLE"