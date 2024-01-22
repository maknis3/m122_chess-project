from collections import Counter
from mychess import Chess
import time
import os
import json
import random

class Engine:
    def __init__(self, chess):
        self.chess = chess
        self.number_of_evaluations = 0
        self.board_evaluations = {}
        self.opening_moves_prep = {}
        self.load_openings()
    
    def calculate_move(self, initial_board_matrix, move_counter):
        timestamp = time.time()
        
        if move_counter <= OPENING_THRESHOLD:
            key = ""
            for piece_type, piece_position in initial_board_matrix.items():
                if piece_type in ("en_passant_position", "last_capture_or_pawn_move"):
                    continue
                else:
                    key += str(piece_position)
            color = "BLACK"
            
            if key in self.opening_moves_prep[color]:
                from_position, to_position = random.choice(self.opening_moves_prep[color][key])
                print("Move found in opening preparation")
                print(f"Search time: {time.time() - timestamp}")
                return from_position, to_position
            else:
                print("No suitable move found in opening prep for key: " + key)
        
        best_eval = -100000
        best_from_position = None
        best_to_position = None
        self.number_of_evaluations = 0
        self.board_evaluations = {}
        depth = 2
        
        if move_counter > ENDGAME_THRESHOLD:
            depth += int(move_counter/ENDGAME_THRESHOLD)
        
        for position_exponent in range(64):
            from_position = (1 << position_exponent)
            if self.chess.is_own_piece(from_position, "BLACK", initial_board_matrix):
                for to_position in self.chess.calculate_possible_moves(initial_board_matrix, from_position):
                    temp_board = initial_board_matrix.copy()
                    self.chess.move_piece(from_position, to_position, temp_board)
                    new_eval = self.minimax(temp_board, depth, best_eval, 1000, False, move_counter + 1)
                    if new_eval > best_eval:
                        best_from_position = from_position
                        best_to_position = to_position
                        best_eval = new_eval
        
        print("number of evaluate calls: " + str(self.number_of_evaluations))
        print(f"calculation time: {time.time() - timestamp}")
        return best_from_position, best_to_position
    
    def evaluate(self, board_matrix, maximazing_player, move_counter):
        board_matrix_hashed = hash(str(board_matrix))
        if board_matrix_hashed in self.board_evaluations:
            return self.board_evaluations[board_matrix_hashed]
        
        eval = 0
        self.number_of_evaluations += 1
        #pov_color = "BLACK" if maximazing_player else "WHITE"
        
        if self.chess.is_in_check(not maximazing_player, board_matrix):
            if self.chess.is_in_checkmate(not maximazing_player, board_matrix):
                return -10000
            else:
                eval -= IN_CHECK_BONUS
        elif self.chess.is_in_check(maximazing_player, board_matrix):
            if self.chess.is_in_checkmate(maximazing_player, board_matrix):
                return 10000
            else:
                eval += IN_CHECK_BONUS
        
        for position_exponent in range(64):
            position = (1 << position_exponent)
            piece_type, piece_color = self.chess.identify_piece(position, board_matrix)
            
            if piece_type:
                temp_eval = 0
                if piece_type == "PAWN":
                    temp_eval += PAWN_VALUE
                    if move_counter > ENDGAME_THRESHOLD:
                        temp_eval += PAWN_END_POS_BONUS[position_exponent if maximazing_player else (63 - position_exponent)]
                    else:
                        temp_eval += PAWN_START_POS_BONUS[position_exponent if maximazing_player else (63 - position_exponent)]
                elif piece_type == "ROOK":
                    temp_eval += ROOK_VALUE + ROOK_POS_BONUS[position_exponent if maximazing_player else (63 - position_exponent)]
                elif piece_type == "KNIGHT":
                    temp_eval += KNIGHT_VALUE + KNIGHT_POS_BONUS[position_exponent]
                elif piece_type == "BISHOP":
                    temp_eval += BISHOP_VALUE + BISHOP_POS_BONUS[position_exponent]
                elif piece_type == "QUEEN":
                    temp_eval += QUEEN_VALUE + BISHOP_POS_BONUS[position_exponent]
                elif piece_type == "KING":
                    if move_counter > ENDGAME_THRESHOLD:
                        temp_eval += KING_END_POS_BONUS[position_exponent if maximazing_player else (63 - position_exponent)]
                    else:
                        temp_eval += KING_START_POS_BONUS[position_exponent if maximazing_player else (63 - position_exponent)]
                eval += temp_eval if maximazing_player else -temp_eval
            else:
                continue
        self.board_evaluations[board_matrix_hashed] = eval
        return eval
    
    def minimax(self, board_matrix, depth, alpha, beta, maximazing_player, move_counter):
        if depth == 0:
            return self.evaluate(board_matrix, maximazing_player, move_counter)
        
        if maximazing_player:
            maxEval = -100000
            for position_exponent in range(64):
                from_position = (1 << position_exponent)
                if self.chess.is_own_piece(from_position, "BLACK", board_matrix):
                    for to_position in self.chess.calculate_possible_moves(board_matrix, from_position):
                        temp_board = board_matrix.copy()
                        if self.chess.move_piece(from_position, to_position, temp_board) and depth == 1:
                            depth += 1
                        eval = self.minimax(temp_board, depth - 1, alpha, beta, False, move_counter + 1)
                        maxEval = max(maxEval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return maxEval
        else:
            minEval = 100000
            for position_exponent in range(64):
                from_position = (1 << position_exponent)
                if self.chess.is_own_piece(from_position, "WHITE", board_matrix):
                    for to_position in self.chess.calculate_possible_moves(board_matrix, from_position):
                        temp_board = board_matrix.copy()
                        self.chess.move_piece(from_position, to_position, temp_board)
                        eval = self.minimax(temp_board, depth - 1, alpha, beta, True, move_counter + 1)
                        minEval = min(minEval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return minEval
             
    def load_openings(self):
        
        filepath = os.getcwd() + "/" + OPENING_MOVES_JSON_RELATIVE_PATH
        
        try:
            with open(filepath, 'r') as file:
                self.opening_moves_prep = json.load(file)
            print("Opening moves loaded successfully.")
        except FileNotFoundError:
            print(f"File not found: {filepath}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {filepath}")
        except Exception as e:
            print(f"An error occurred while loading the file: {e}")



# Engine config:

OPENING_MOVES_JSON_RELATIVE_PATH = "move_archive/openings.json"

PAWN_VALUE = 1
BISHOP_VALUE = 3
KNIGHT_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 7

IN_CHECK_BONUS = 2

OPENING_THRESHOLD = 10
ENDGAME_THRESHOLD = 50

KNIGHT_POS_BONUS = [-0.5,-0.4, -0.2, -0.1, -0.1, -0.2, -0.4, -0.5, -0.4, -0.2, -0.1, 0.1, 0.1, -0.1, -0.2, -0.4, -0.2, -0.1, 0.1, 0.3, 0.3, 0.1, -0.1, -0.2, -0.1, 0.1, 0.3, 0.5, 0.5, 0.3, 0.1, -0.1, -0.1, 0.1, 0.3, 0.5, 0.5, 0.3, 0.1, -0.1, -0.2, -0.1, 0.1, 0.3, 0.3, 0.1, -0.1, -0.2, -0.4, -0.2, -0.1, 0.1, 0.1, -0.1, -0.2, -0.4, -0.5, -0.4, -0.2, -0.1, -0.1, -0.2, -0.4, -0.5]
BISHOP_POS_BONUS = [-0.2, -0.1, 0, 0.1, 0.1, 0, -0.1, -0.2, -0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, -0.1, 0, 0.2, 0.4, 0.4, 0.4, 0.4, 0.2, 0, 0.1, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.1, 0.1, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.1, 0, 0.2, 0.4, 0.4, 0.4, 0.4, 0.2, 0, -0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, -0.1, -0.2, -0.1, 0, 0.1, 0.1, 0, -0.1, -0.2]
QUEEN_POS_BONUS = [-0.4, -0.2, 0, 0.2, 0.2, 0, -0.2, -0.4, -0.2, 0, 0.2, 0.4, 0.4, 0.2, 0, -0.2, 0, 0.2, 0.4, 0.5, 0.5, 0.4, 0.2, 0, 0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2, 0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2, 0, 0.2, 0.4, 0.5, 0.5, 0.4, 0.2, 0, -0.2, 0, 0.2, 0.4, 0.4, 0.2, 0, -0.2, -0.4, -0.2, 0, 0.2, 0.2, 0, -0.2, -0.4]
PAWN_START_POS_BONUS = [0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.2, 0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1, 0, 0, 0, 0.2, 0.2, 0, 0, 0, 0.1, 0, -0.1, 0, 0, -0.1, 0, 0.1, 0.1, 0.2, 0.2, -0.2, -0.2, 0.2, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0]
PAWN_END_POS_BONUS = [0, 0, 0, 0, 0, 0, 0, 0, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
KING_START_POS_BONUS = [-0.5, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.5, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.2, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.2, -0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1, 0, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, 0, 0, 0.2, 0, 0, 0, 0, 0.2, 0, 0.2, 0.3, 0.2, 0.2, 0.2, 0.2, 0.3, 0.2, 0.2, 0.4, 0.7, 0.4, 0.2, 0.4, 0.7, 0.2]
KING_END_POS_BONUS = [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2, -0.1, 0, 0.1, 0.1, 0.1, 0.1, 0, -0.1, -0.1, -0.1, 0.3, 0.4, 0.4, 0.3, -0.1, -0.1, -0.1, -0.1, 0.4, 0.5, 0.5, 0.4, -0.1, -0.1, -0.1, -0.1, 0.2, 0.4, 0.4, 0.2, -0.1, -0.1, -0.2, -0.1, 0, 0.2, 0.2, 0, -0.1, -0.2, -0.3, -0.2, -0.1, 0, 0, -0.1, -0.2, -0.3, -0.4, -0.3, -0.2, -0.2, -0.2, -0.2, -0.3, -0.4]
ROOK_POS_BONUS = [0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.2, 0, 0, 0.3, 0, 0.3, 0, -0.2]
