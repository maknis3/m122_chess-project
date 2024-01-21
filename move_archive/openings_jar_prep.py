import json
from chess import Chess
import time

def parse_move_to_bit(move, chess, board_matrix, white_turn):
    try:
        if move in ("O-O", "O-O-O"):
            king_position = chess.square_to_position((7, 4)) if white_turn else chess.square_to_position((0, 4))
            rook_position = None
            if move == "O-O":
                rook_position = chess.square_to_position((7, 7)) if white_turn else chess.square_to_position((0, 7))
            elif move == "O-O-O":
                rook_position = chess.square_to_position((7, 0)) if white_turn else chess.square_to_position((0, 0))
            return king_position, rook_position
        else:
            from_square, to_square = convert_algebraic_to_squares(move, chess, board_matrix, white_turn)
            from_position = chess.square_to_position(from_square)
            to_position = chess.square_to_position(to_square)
            return from_position, to_position
    except Exception as e:
        print(f"Error in parsing move {move}: {e}")
        return None, None

def convert_algebraic_to_squares(move, chess, board_matrix, white_turn):
    try:
        if "+" in move:
            move = move.replace("+", "")
        if len(move) == 2:
            col = ord(move[0]) - ord('a')
            row = 8 - int(move[1])
            from_row = row + 1 if white_turn else row - 1
            if not chess.identify_piece(chess.square_to_position((from_row, col)), board_matrix)[0] == "PAWN":
                from_row += 1 if white_turn else -1
            return (from_row, col), (row, col)
        elif "x" in move:
            to_col = ord(move[-2]) - ord('a')
            to_row = 8 - int(move[-1])
            to_position = chess.square_to_position((to_row, to_col))

            if move[0].isupper(): 
                piece_type = {
                    "R": "ROOK",
                    "N": "KNIGHT",
                    "B": "BISHOP",
                    "Q": "QUEEN",
                    "K": "KING"
                }.get(move[0], None)

                for row in range(8):
                    for col in range(8):
                        from_position = chess.square_to_position((row, col))
                        current_piece, current_color = chess.identify_piece(from_position, board_matrix)
                        if current_piece == piece_type and ((current_color == "WHITE") == white_turn):
                            if to_position in chess.calculate_possible_moves(board_matrix, from_position):
                                return (row, col), (to_row, to_col)
            else:  # Pawn capture, e.g., "dxe4"
                from_col = ord(move[0]) - ord('a')
                from_row = to_row + 1 if white_turn else to_row - 1
                return (from_row, from_col), (to_row, to_col)
        else:
            to_col = ord(move[-2]) - ord('a')
            to_row = 8 - int(move[-1])
            to_position = chess.square_to_position((to_row, to_col))
            
            piece_type = {
                "R": "ROOK",
                "N": "KNIGHT",
                "B": "BISHOP",
                "Q": "QUEEN",
                "K": "KING"
            }.get(move[0], "PAWN")

            for row in range(8):
                for col in range(8):
                    from_position = chess.square_to_position((row, col))
                    current_piece, current_color = chess.identify_piece(from_position, board_matrix)
                    if current_piece == piece_type and ((current_color == "WHITE") == white_turn):
                        if to_position in chess.calculate_possible_moves(board_matrix, from_position):
                            return (row, col), (to_row, to_col)
        return None, None
    
    except Exception as e:
        print(f"Error in converting move {move}: {e}")
        return None, None

def process_games(games):
    opening_moves_black = {}
    opening_moves_white = {}
    chess = Chess(None) 
    number_of_games = len(games)
    number_of_processed_games = 0
    number_of_skipped_games = 0
    number_of_processed_moves = 0
    initial_board_matrix = {
        "PAWN_BLACK": 0b0000000000000000000000000000000000000000000000001111111100000000,
        "ROOK_BLACK": 0b0000000000000000000000000000000000000000000000000000000010000001,
        "KNIGHT_BLACK": 0b0000000000000000000000000000000000000000000000000000000001000010,
        "BISHOP_BLACK": 0b0000000000000000000000000000000000000000000000000000000000100100,
        "QUEEN_BLACK": 0b0000000000000000000000000000000000000000000000000000000000001000,
        "KING_BLACK": 0b0000000000000000000000000000000000000000000000000000000000010000,
        "PAWN_WHITE": 0b0000000011111111000000000000000000000000000000000000000000000000,
        "ROOK_WHITE": 0b1000000100000000000000000000000000000000000000000000000000000000,
        "KNIGHT_WHITE": 0b0100001000000000000000000000000000000000000000000000000000000000,
        "BISHOP_WHITE": 0b0010010000000000000000000000000000000000000000000000000000000000,
        "QUEEN_WHITE": 0b0000100000000000000000000000000000000000000000000000000000000000,
        "KING_WHITE": 0b0001000000000000000000000000000000000000000000000000000000000000,
        "casteling_rights": 0b1111, #white-queenside, white-kingside, black-queenside, black-kingside
        "en_passant_position": 0,
        "last_capture_or_pawn_move": 0, 
        "all_pieces": -281474976645121
    }
    
    for game in games:
        board_matrix = initial_board_matrix.copy()
        white_turn = True

        for move_num in range(min(10, len(game))):
            try:
                move = game[move_num]
                board_hash = hash(str(board_matrix))
                from_position, to_position = parse_move_to_bit(move, chess, board_matrix, white_turn)

                if from_position is None or to_position is None:
                    print(f"Skipping move {move} in game {game} due to parsing error. white_turn: {white_turn}, Board: {str(board_matrix)}")
                    number_of_skipped_games += 1
                    break
                
                if to_position in chess.calculate_possible_moves(board_matrix, from_position):
                    chess.move_piece(from_position, to_position, board_matrix)
                else: 
                    print(f"Invalid move detected! Tried {move} on board = {board_matrix}")

                number_of_processed_moves += 1
                
                if white_turn:
                    if board_hash not in opening_moves_white.keys():
                        opening_moves_white[board_hash] = [(from_position, to_position)]
                    elif (from_position, to_position) not in opening_moves_white[board_hash]:
                        opening_moves_white[board_hash].append((from_position, to_position))
                    white_turn = False
                elif not white_turn:
                    board_hash = hash(str(board_matrix))
                    if board_hash not in opening_moves_black.keys():
                        opening_moves_black[board_hash] = [(from_position, to_position)]
                    elif (from_position, to_position) not in opening_moves_black[board_hash]:
                        opening_moves_black[board_hash].append((from_position, to_position))
                    white_turn = True
        
                
            except Exception as e:
                print(f"Error processing the {move_num}. move, move {move} in game {game}: {e}")
                number_of_skipped_games += 1
                break

        number_of_processed_games += 1
        print(f"processed {round((number_of_processed_games/number_of_games)*100, 2)}% games")
            
    return opening_moves_black, opening_moves_white, number_of_skipped_games, number_of_processed_moves















# Conversion-functions call:

start_time = time.time()

try:
    with open('extracted_moves.json', 'r') as file:
        data = json.load(file)
except Exception as e:
    print(f"Error loading JSON file: {e}")

try:
    opening_moves_black, opening_moves_white, number_of_skipped_games, number_of_processed_moves = process_games(data["games"])
except Exception as e:
    print(f"Error processing games: {e}")

new_data = {"BLACK": opening_moves_black, "WHITE": opening_moves_white}

try:
    with open('processed_opening_moves.json', 'w') as file:
        json.dump(new_data, file, indent=4)
except Exception as e:
    print(f"Error writing to JSON file: {e}")

print(f"Finished move conversion for {number_of_processed_moves} moves")
print(f"Time spent: {time.time() - start_time}")
print(f"Games skipped or partially skipped: {number_of_skipped_games}")

