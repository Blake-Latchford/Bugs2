import gameboard
import unittest
import piece


class GameBoardTestCase(unittest.TestCase):

    def setUp(self):
        self.game_board = gameboard.GameBoard()

        # Setup to test various move options.
        # Layout is as follows, with white spider 0 (ws0) at 0,0.
        # bB0 is black bee zero, and bb0 is black beetle zero.
        #
        #               wB0
        # wa1 ba0 bb0 ws0
        #       bB0     wa0
        #             ba1

        self.white_spider_0 = piece.Piece(
            piece.PieceType.SPIDER,
            piece.Color.WHITE,
            0,
            0, 0)
        self.white_bee_0 = piece.Piece(
            piece.PieceType.BEE,
            piece.Color.WHITE,
            0,
            1, -1)
        self.white_ant_0 = piece.Piece(
            piece.PieceType.ANT,
            piece.Color.WHITE,
            0,
            0, 1)
        self.white_ant_1 = piece.Piece(
            piece.PieceType.ANT,
            piece.Color.WHITE,
            1,
            -3, 0)

        self.black_beetle_0 = piece.Piece(
            piece.PieceType.BEETLE,
            piece.Color.BLACK,
            0,
            -1, 0)
        self.black_bee_0 = piece.Piece(
            piece.PieceType.BEE,
            piece.Color.BLACK,
            0,
            -2, 1)
        self.black_ant_0 = piece.Piece(
            piece.PieceType.ANT,
            piece.Color.BLACK,
            0,
            -2, 0)
        self.black_ant_1 = piece.Piece(
            piece.PieceType.ANT,
            piece.Color.BLACK,
            1,
            -1, 2)

        self.starting_pieces = (
            self.white_spider_0,
            self.white_bee_0,
            self.white_ant_0,
            self.white_ant_1,
            self.black_beetle_0,
            self.black_bee_0,
            self.black_ant_0,
            self.black_ant_1)

        for starting_piece in self.starting_pieces:
            self.game_board.force_place(starting_piece)

    def test_equal_empty(self):
        first = gameboard.GameBoard()
        second = gameboard.GameBoard()
        self.assertEqual(first, second)

    def test_equal(self):
        self.assertEqual(self.game_board, self.game_board)

    def test_not_equal(self):
        empty_board = gameboard.GameBoard()
        self.assertNotEqual(empty_board, self.game_board)

    def test_get_pieces(self):
        for color in (None, piece.Color.BLACK, piece.Color.WHITE):
            pieces = set(self.game_board.get_pieces(color))
            placed_pieces = set(self.game_board.get_placed_pieces(color))
            unplaced_pieces = set(self.game_board.get_unplaced_pieces(color))

            # "Greater" here is for the set operator overloading for
            # proper superset.
            with self.subTest(msg="Placed Pieces", color=color):
                self.assertGreater(pieces, placed_pieces)
            with self.subTest(msg="Unplaced Pieces", color=color):
                self.assertGreater(pieces, unplaced_pieces)

    def test_get_placed_pieces(self):
        placed_pieces = self.game_board.get_placed_pieces()
        for piece in self.starting_pieces:
            with self.subTest(str(piece)):
                self.assertIn(piece, placed_pieces)

    def test_get_unplaced_pieces(self):
        unplaced_pieces = self.game_board.get_unplaced_pieces()
        for piece in self.starting_pieces:
            with self.subTest(str(piece)):
                self.assertNotIn(piece, unplaced_pieces)

    def test_piece_stacking(self):
        beetle_on_top_of_hive = piece.Piece(
            piece.PieceType.BEETLE,
            piece.Color.WHITE,
            0,
            -1, 0)

        self.game_board.force_place(beetle_on_top_of_hive)
        self.assertIs(beetle_on_top_of_hive,
                      self.game_board.get_cell(
                          beetle_on_top_of_hive.q, beetle_on_top_of_hive.r))

        # The bottom piece is still registered on the board.
        self.assertIn(self.black_beetle_0,
                      self.game_board.get_placed_pieces())

    def test_piece_unstacking(self):
        beetle_on_top_of_hive = piece.Piece(
            piece.PieceType.BEETLE,
            piece.Color.WHITE,
            0,
            -1, 0)
        beetle_off_of_hive = piece.Piece(
            piece.PieceType.BEETLE,
            piece.Color.WHITE,
            0,
            -1, -1)

        self.game_board.force_place(beetle_on_top_of_hive)
        self.game_board.force_place(beetle_off_of_hive)

        self.assertIs(beetle_off_of_hive, self.game_board.get_cell(
            beetle_off_of_hive.q, beetle_off_of_hive.r))
        self.assertIs(beetle_off_of_hive, self.game_board.get_cell(
            beetle_off_of_hive.q, beetle_off_of_hive.r))

    def test_place_floating(self):
        floating_piece = piece.Piece(
            piece.PieceType.BEETLE,
            piece.Color.WHITE,
            0,
            0, -2)

        with self.assertRaises(ValueError):
            self.game_board.place(floating_piece)

    def test_invalid_move(self):
        """No valid move exists from the starting configuration to perform
        this move."""
        invalid_placement = piece.Piece(
            piece.PieceType.BEE,
            piece.Color.WHITE,
            0,
            1, 1)

        with self.assertRaises(ValueError):
            self.game_board.place(invalid_placement)

    def test_get_moves(self):
        available_moves = self.game_board.get_moves()

        for starting_piece in self.starting_pieces:
            with self.subTest(starting_piece):
                self.assertEqual(
                    list(starting_piece.get_moves(self.game_board)),
                    list(available_moves[starting_piece]))

    def test_json_conversion(self):
        json_object = self.game_board.to_json_object()
        end_game_board = gameboard.GameBoard(json_object=json_object)
        self.assertEqual(self.game_board, end_game_board)
        self.assertIsNot(self.game_board, end_game_board)
