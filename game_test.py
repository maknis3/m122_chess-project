import unittest
from game import ChessGame
from pieces import ChessPiece, Color
from board import Board

class TestChessGame(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame()
        self.game.board_matrix = [[ChessPiece.EMPTY for _ in range(8)] for _ in range(8)]
    
    def test_board_setup(self):
        self.game.initialize_board()
        expected_board_matrix = [
            [ChessPiece.ROOK_BLACK, ChessPiece.KNIGHT_BLACK, ChessPiece.BISHOP_BLACK, ChessPiece.QUEEN_BLACK, ChessPiece.KING_BLACK, ChessPiece.BISHOP_BLACK, ChessPiece.KNIGHT_BLACK, ChessPiece.ROOK_BLACK],
            [ChessPiece.PAWN_BLACK] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.PAWN_WHITE] * 8,
            [ChessPiece.ROOK_WHITE, ChessPiece.KNIGHT_WHITE, ChessPiece.BISHOP_WHITE, ChessPiece.QUEEN_WHITE, ChessPiece.KING_WHITE, ChessPiece.BISHOP_WHITE, ChessPiece.KNIGHT_WHITE, ChessPiece.ROOK_WHITE],
        ]
        self.assertEqual(self.game.board_matrix, expected_board_matrix, "Board should initialize with pieces in the correct positions.")

    def test_player_assignment(self):
        self.assertEqual(self.game.current_player, Color.WHITE, "The current player should be white at the start of the game.")
        self.game.switch_current_player()
        self.assertEqual(self.game.current_player, Color.BLACK, "The current player should be black after player switch.")
        
    def test_pawn_movement(self):
        self.game.board_matrix[6][2] = ChessPiece.PAWN_WHITE
        self.assertTrue(self.game.is_valid_move((6, 2), (5, 2), self.game.board_matrix, None), "Pawn should move forward one square.")
        self.assertTrue(self.game.is_valid_move((6, 2), (4, 2), self.game.board_matrix, None), "Pawn should move forward two squares.")
        self.game.board_matrix[5][1] = ChessPiece.PAWN_BLACK  
        self.assertTrue(self.game.is_valid_move((6, 2), (5, 1), self.game.board_matrix, None), "Pawn should capture diagonally.")

    def test_rook_movement(self):
        self.game.board_matrix[4][4] = ChessPiece.ROOK_WHITE
        self.assertTrue(self.game.is_valid_move((4, 4), (4, 6), self.game.board_matrix, None), "Rook should move horizontally.")
        self.assertTrue(self.game.is_valid_move((4, 4), (6, 4), self.game.board_matrix, None), "Rook should move vertically.")

    def test_knight_movement(self):
        self.game.board_matrix[0][1] = ChessPiece.KNIGHT_WHITE
        self.assertTrue(self.game.is_valid_move((0, 1), (2, 2), self.game.board_matrix, None), "Knight should move in L shape (2 up, 1 right).")
        self.assertTrue(self.game.is_valid_move((0, 1), (1, 3), self.game.board_matrix, None), "Knight should move in L shape (1 up, 2 right).")

    def test_bishop_movement(self):
        self.game.board_matrix[2][0] = ChessPiece.BISHOP_WHITE
        self.assertTrue(self.game.is_valid_move((2, 0), (5, 3), self.game.board_matrix, None), "Bishop should move diagonally.")

    def test_queen_movement(self):
        self.game.board_matrix[0][3] = ChessPiece.QUEEN_WHITE
        self.assertTrue(self.game.is_valid_move((0, 3), (0, 5), self.game.board_matrix, None), "Queen should move horizontally.")
        self.assertTrue(self.game.is_valid_move((0, 3), (5, 3), self.game.board_matrix, None), "Queen should move vertically.")
        self.assertTrue(self.game.is_valid_move((0, 3), (3, 6), self.game.board_matrix, None), "Queen should move diagonally.")

    def test_king_movement(self):
        self.game.board_matrix[4][4] = ChessPiece.KING_WHITE
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = 4 + dr, 4 + dc
            self.assertTrue(self.game.is_valid_move((4, 4), (r, c), self.game.board_matrix, None), f"King should move one square in any direction. Failed at direction {dr},{dc}")
            
    def test_pawn_promotion_white_queen(self):
        self.game.board_matrix[1][0] = ChessPiece.PAWN_WHITE
        self.game.board_matrix, placeHolder = self.game.move_piece((1, 0), (0, 0), self.game.board_matrix, None, ChessPiece.QUEEN_WHITE)
        self.assertNotEqual(self.game.board_matrix[0][0], ChessPiece.PAWN_WHITE, "Pawn should not be a pawn after promotion.")
        self.assertEqual(self.game.board_matrix[0][0], ChessPiece.QUEEN_WHITE, "Pawn should be promoted to a queen.")
            
    def test_pawn_promotion_white_bishop(self):
        self.game.board_matrix[1][0] = ChessPiece.PAWN_WHITE
        self.game.board_matrix, placeHolder = self.game.move_piece((1, 0), (0, 0), self.game.board_matrix, None, ChessPiece.BISHOP_WHITE)
        self.assertNotEqual(self.game.board_matrix[0][0], ChessPiece.PAWN_WHITE, "Pawn should not be a pawn after promotion.")
        self.assertEqual(self.game.board_matrix[0][0], ChessPiece.BISHOP_WHITE, "Pawn should be promoted to a bishop.")
            
    def test_pawn_promotion_white_knight(self):
        self.game.board_matrix[1][0] = ChessPiece.PAWN_WHITE
        self.game.board_matrix, placeHolder = self.game.move_piece((1, 0), (0, 0), self.game.board_matrix, None, ChessPiece.KNIGHT_WHITE)
        self.assertNotEqual(self.game.board_matrix[0][0], ChessPiece.PAWN_WHITE, "Pawn should not be a pawn after promotion.")
        self.assertEqual(self.game.board_matrix[0][0], ChessPiece.KNIGHT_WHITE, "Pawn should be promoted knight.")
            
    def test_pawn_promotion_white_rook(self):
        self.game.board_matrix[1][0] = ChessPiece.PAWN_WHITE
        self.game.board_matrix, placeHolder = self.game.move_piece((1, 0), (0, 0), self.game.board_matrix, None, ChessPiece.ROOK_WHITE)
        self.assertNotEqual(self.game.board_matrix[0][0], ChessPiece.PAWN_WHITE, "Pawn should not be a pawn after promotion.")
        self.assertEqual(self.game.board_matrix[0][0], ChessPiece.ROOK_WHITE, "Pawn should be promoted to a rook.")
            
    def test_pawn_promotion_black_queen(self):
        self.game.board_matrix[6][0] = ChessPiece.PAWN_BLACK
        self.game.board_matrix, placeHolder = self.game.move_piece((6, 0), (7, 0), self.game.board_matrix, None, ChessPiece.QUEEN_BLACK)
        self.assertNotEqual(self.game.board_matrix[7][0], ChessPiece.PAWN_BLACK, "Pawn should not be a pawn after promotion.")
        self.assertEqual(self.game.board_matrix[7][0], ChessPiece.QUEEN_BLACK, "Pawn should be promoted to a queen.")
            
    def test_pawn_promotion_black_bishop(self):
        self.game.board_matrix[6][0] = ChessPiece.PAWN_BLACK
        self.game.board_matrix, placeHolder = self.game.move_piece((6, 0), (7, 0), self.game.board_matrix, None, ChessPiece.BISHOP_BLACK)
        self.assertNotEqual(self.game.board_matrix[7][0], ChessPiece.PAWN_BLACK, "Pawn should not be a pawn after promotion.")
        self.assertEqual(self.game.board_matrix[7][0], ChessPiece.BISHOP_BLACK, "Pawn should be promoted to a bishop.")
            
    def test_pawn_promotion_black_knight(self):
        self.game.board_matrix[6][0] = ChessPiece.PAWN_BLACK
        self.game.board_matrix, placeHolder = self.game.move_piece((6, 0), (7, 0), self.game.board_matrix, None, ChessPiece.KNIGHT_BLACK)
        self.assertNotEqual(self.game.board_matrix[7][0], ChessPiece.PAWN_BLACK, "Pawn should not be a pawn after promotion.")
        self.assertEqual(self.game.board_matrix[7][0], ChessPiece.KNIGHT_BLACK, "Pawn should be promoted knight.")
            
    def test_pawn_promotion_black_rook(self):
        self.game.board_matrix[6][0] = ChessPiece.PAWN_BLACK
        self.game.board_matrix, placeHolder = self.game.move_piece((6, 0), (7, 0), self.game.board_matrix, None, ChessPiece.ROOK_BLACK)
        self.assertNotEqual(self.game.board_matrix[7][0], ChessPiece.PAWN_BLACK, "Pawn should not be a pawn after promotion.")
        self.assertEqual(self.game.board_matrix[7][0], ChessPiece.ROOK_BLACK, "Pawn should be promoted to a rook.")

    def test_en_passant_white(self):
        self.game.board_matrix[3][0] = ChessPiece.PAWN_WHITE  
        self.game.board_matrix[1][1] = ChessPiece.PAWN_BLACK 
        self.game.board_matrix, self.game.en_passant_square = self.game.move_piece((1, 1), (3, 1), self.game.board_matrix, self.game.en_passant_square, None, True)
        self.game.board_matrix, self.game.en_passant_square = self.game.move_piece((3, 0), (2, 1), self.game.board_matrix, self.game.en_passant_square, None, True)
        self.assertEqual(self.game.board_matrix[2][1], ChessPiece.PAWN_WHITE, "White pawn should capture black pawn en passant.")
        self.assertEqual(self.game.board_matrix[3][1], ChessPiece.EMPTY, "Black pawn should be captured.")

    def test_en_passant_black(self):
        self.game.board_matrix[4][0] = ChessPiece.PAWN_BLACK  
        self.game.board_matrix[6][1] = ChessPiece.PAWN_WHITE 
        self.game.board_matrix, self.game.en_passant_square = self.game.move_piece((6, 1), (4, 1), self.game.board_matrix, self.game.en_passant_square, None, True)
        self.game.board_matrix, self.game.en_passant_square = self.game.move_piece((4, 0), (5, 1), self.game.board_matrix, self.game.en_passant_square, None, True)
        self.assertEqual(self.game.board_matrix[5][1], ChessPiece.PAWN_BLACK, "Black pawn should capture white pawn en passant.")
        self.assertEqual(self.game.board_matrix[4][1], ChessPiece.EMPTY, "White pawn should be captured.")

    def test_castling_kingside_white_as_king(self):
        self.game.board_matrix[7][4] = ChessPiece.KING_WHITE
        self.game.board_matrix[7][7] = ChessPiece.ROOK_WHITE
        self.assertTrue(self.game.can_castle_kingside(self.game.board_matrix), "Should be able to castle kingside.")
        self.game.board_matrix, placeHolder = self.game.move_piece((7, 4), (7, 7), self.game.board_matrix, None, None, True)
        self.assertEqual(self.game.board_matrix[7][6], ChessPiece.KING_WHITE, "King should move to kingside castling position.")
        self.assertEqual(self.game.board_matrix[7][5], ChessPiece.ROOK_WHITE, "Rook should move to kingside castling position.")
        self.assertFalse(self.game.can_castle_kingside(self.game.board_matrix), "Should no longer be able to castle kingside.")

    def test_castling_queenside_white_as_king(self):
        self.game.board_matrix[7][4] = ChessPiece.KING_WHITE
        self.game.board_matrix[7][0] = ChessPiece.ROOK_WHITE
        self.assertTrue(self.game.can_castle_queenside(self.game.board_matrix), "Should be able to castle kingside.")
        self.game.board_matrix, placeHolder = self.game.move_piece((7, 4), (7, 0), self.game.board_matrix, None, None, True)
        self.assertEqual(self.game.board_matrix[7][2], ChessPiece.KING_WHITE, "King should move to kingside castling position.")
        self.assertEqual(self.game.board_matrix[7][3], ChessPiece.ROOK_WHITE, "Rook should move to kingside castling position.")
        self.assertFalse(self.game.can_castle_queenside(self.game.board_matrix), "Should no longer be able to castle kingside.")

    def test_castling_kingside_white_as_rook(self):
        self.game.board_matrix[7][4] = ChessPiece.KING_WHITE
        self.game.board_matrix[7][7] = ChessPiece.ROOK_WHITE
        self.assertTrue(self.game.can_castle_kingside(self.game.board_matrix), "Should be able to castle kingside.")
        self.game.board_matrix, placeHolder = self.game.move_piece((7, 7), (7, 4), self.game.board_matrix, None, None, True)
        self.assertEqual(self.game.board_matrix[7][6], ChessPiece.KING_WHITE, "King should move to kingside castling position.")
        self.assertEqual(self.game.board_matrix[7][5], ChessPiece.ROOK_WHITE, "Rook should move to kingside castling position.")
        self.assertFalse(self.game.can_castle_kingside(self.game.board_matrix), "Should no longer be able to castle kingside.")

    def test_castling_queenside_white_as_rook(self):
        self.game.board_matrix[7][4] = ChessPiece.KING_WHITE
        self.game.board_matrix[7][0] = ChessPiece.ROOK_WHITE
        self.assertTrue(self.game.can_castle_queenside(self.game.board_matrix), "Should be able to castle kingside.")
        self.game.board_matrix, placeHolder = self.game.move_piece((7, 0), (7, 4), self.game.board_matrix, None, None, True)
        self.assertEqual(self.game.board_matrix[7][2], ChessPiece.KING_WHITE, "King should move to kingside castling position.")
        self.assertEqual(self.game.board_matrix[7][3], ChessPiece.ROOK_WHITE, "Rook should move to kingside castling position.")
        self.assertFalse(self.game.can_castle_queenside(self.game.board_matrix), "Should no longer be able to castle kingside.")

    def test_castling_kingside_black_as_king(self):
        self.game.switch_current_player()
        self.game.board_matrix[0][4] = ChessPiece.KING_BLACK
        self.game.board_matrix[0][7] = ChessPiece.ROOK_BLACK
        self.assertTrue(self.game.can_castle_kingside(self.game.board_matrix), "Should be able to castle kingside.")
        self.game.board_matrix, placeHolder = self.game.move_piece((0, 4), (0, 7), self.game.board_matrix, None, None, True)
        self.assertEqual(self.game.board_matrix[0][6], ChessPiece.KING_BLACK, "King should move to kingside castling position.")
        self.assertEqual(self.game.board_matrix[0][5], ChessPiece.ROOK_BLACK, "Rook should move to kingside castling position.")
        self.assertFalse(self.game.can_castle_kingside(self.game.board_matrix), "Should no longer be able to castle kingside.")

    def test_castling_queenside_black_as_king(self):
        self.game.switch_current_player()
        self.game.board_matrix[0][4] = ChessPiece.KING_BLACK
        self.game.board_matrix[0][0] = ChessPiece.ROOK_BLACK
        self.assertTrue(self.game.can_castle_queenside(self.game.board_matrix), "Should be able to castle kingside.")
        self.game.board_matrix, placeHolder = self.game.move_piece((0, 4), (0, 0), self.game.board_matrix, None, None, True)
        self.assertEqual(self.game.board_matrix[0][2], ChessPiece.KING_BLACK, "King should move to kingside castling position.")
        self.assertEqual(self.game.board_matrix[0][3], ChessPiece.ROOK_BLACK, "Rook should move to kingside castling position.")
        self.assertFalse(self.game.can_castle_queenside(self.game.board_matrix), "Should no longer be able to castle kingside.")

    def test_castling_kingside_black_as_rook(self):
        self.game.switch_current_player()
        self.game.board_matrix[0][4] = ChessPiece.KING_BLACK
        self.game.board_matrix[0][7] = ChessPiece.ROOK_BLACK
        self.assertTrue(self.game.can_castle_kingside(self.game.board_matrix), "Should be able to castle kingside.")
        self.game.board_matrix, placeHolder = self.game.move_piece((0, 7), (0, 4), self.game.board_matrix, None, None, True)
        self.assertEqual(self.game.board_matrix[0][6], ChessPiece.KING_BLACK, "King should move to kingside castling position.")
        self.assertEqual(self.game.board_matrix[0][5], ChessPiece.ROOK_BLACK, "Rook should move to kingside castling position.")
        self.assertFalse(self.game.can_castle_kingside(self.game.board_matrix), "Should no longer be able to castle kingside.")

    def test_castling_queenside_black_as_rook(self):
        self.game.switch_current_player()
        self.game.board_matrix[0][4] = ChessPiece.KING_BLACK
        self.game.board_matrix[0][0] = ChessPiece.ROOK_BLACK
        self.assertTrue(self.game.can_castle_queenside(self.game.board_matrix), "Should be able to castle kingside.")
        self.game.board_matrix, placeHolder = self.game.move_piece((0, 0), (0, 4), self.game.board_matrix, None, None, True)
        self.assertEqual(self.game.board_matrix[0][2], ChessPiece.KING_BLACK, "King should move to kingside castling position.")
        self.assertEqual(self.game.board_matrix[0][3], ChessPiece.ROOK_BLACK, "Rook should move to kingside castling position.")
        self.assertFalse(self.game.can_castle_queenside(self.game.board_matrix), "Should no longer be able to castle kingside.")

    def test_detects_checkmate_white(self):
        self.game.board_matrix = [
            [ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.ROOK_BLACK],
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.PAWN_WHITE, ChessPiece.PAWN_WHITE, ChessPiece.PAWN_WHITE, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY],
            [ChessPiece.KING_WHITE, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY]
            ]
        self.assertFalse(self.game.is_checkmate(self.game.board_matrix, None))
        self.game.board_matrix, placeHolder = self.game.move_piece((0, 7), (7, 7), self.game.board_matrix, None, None, True)
        self.assertTrue(self.game.is_checkmate(self.game.board_matrix, None))

    def test_detects_checkmate_black(self):
        self.game.switch_current_player()
        self.game.board_matrix = [
            [ChessPiece.KING_BLACK, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY],
            [ChessPiece.PAWN_BLACK, ChessPiece.PAWN_BLACK, ChessPiece.PAWN_BLACK, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY],
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.ROOK_WHITE]
            ]
        self.assertFalse(self.game.is_checkmate(self.game.board_matrix, None))
        self.game.board_matrix, placeHolder = self.game.move_piece((7, 7), (0, 7), self.game.board_matrix, None, None, True)
        self.assertTrue(self.game.is_checkmate(self.game.board_matrix, None))

    def test_not_checkmate_if_en_passant_possible(self):
        self.game.board_matrix = [
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.KING_BLACK, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.PAWN_BLACK, ChessPiece.KNIGHT_BLACK, ChessPiece.EMPTY],
            [ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.QUEEN_BLACK],
            [ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.PAWN_WHITE, ChessPiece.EMPTY, ChessPiece.EMPTY],
            [ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.KING_WHITE, ChessPiece.EMPTY],
            [ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.ROOK_BLACK, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY, ChessPiece.EMPTY],
            [ChessPiece.EMPTY] * 8,
            [ChessPiece.EMPTY] * 8
            ]
        self.assertFalse(self.game.is_checkmate(self.game.board_matrix, self.game.en_passant_square))
        self.game.board_matrix, self.game.en_passant_square = self.game.move_piece((1, 5), (3, 5), self.game.board_matrix, None, None, True)
        self.assertTrue(self.game.is_in_check(self.game.board_matrix))
        self.assertFalse(self.game.is_checkmate(self.game.board_matrix, self.game.en_passant_square))


if __name__ == '__main__':
    unittest.main()
