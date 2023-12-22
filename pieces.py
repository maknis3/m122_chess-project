from enum import Enum

class Color(Enum):
    WHITE = "W"
    BLACK = "B"

class ChessPiece(Enum):
    EMPTY = ""
    PAWN_WHITE = Color.WHITE.value + "P"
    KNIGHT_WHITE = Color.WHITE.value + "N"
    BISHOP_WHITE = Color.WHITE.value + "B"
    ROOK_WHITE = Color.WHITE.value + "R"
    QUEEN_WHITE = Color.WHITE.value + "Q"
    KING_WHITE = Color.WHITE.value + "K"
    
    PAWN_BLACK = Color.BLACK.value + "P"
    KNIGHT_BLACK = Color.BLACK.value + "N"
    BISHOP_BLACK = Color.BLACK.value + "B"
    ROOK_BLACK = Color.BLACK.value + "R"
    QUEEN_BLACK = Color.BLACK.value + "Q"
    KING_BLACK = Color.BLACK.value + "K"
