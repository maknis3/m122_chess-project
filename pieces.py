from enum import Enum

class Color(Enum):
    WHITE = "W"
    BLACK = "B"
    
class Piece(Enum):
    PAWN = "P"
    KNIGHT = "N"
    BISHOP = "B"
    ROOK = "R"
    QUEEN = "Q"
    KING = "K"

class ChessPiece(Enum):
    EMPTY = ""
    PAWN_WHITE = Color.WHITE.value + Piece.PAWN.value
    KNIGHT_WHITE = Color.WHITE.value + Piece.KNIGHT.value
    BISHOP_WHITE = Color.WHITE.value + Piece.BISHOP.value
    ROOK_WHITE = Color.WHITE.value + Piece.ROOK.value
    QUEEN_WHITE = Color.WHITE.value + Piece.QUEEN.value
    KING_WHITE = Color.WHITE.value + Piece.KING.value
    
    PAWN_BLACK = Color.BLACK.value + Piece.PAWN.value
    KNIGHT_BLACK = Color.BLACK.value + Piece.KNIGHT.value
    BISHOP_BLACK = Color.BLACK.value + Piece.BISHOP.value
    ROOK_BLACK = Color.BLACK.value + Piece.ROOK.value
    QUEEN_BLACK = Color.BLACK.value + Piece.QUEEN.value
    KING_BLACK = Color.BLACK.value + Piece.KING.value
