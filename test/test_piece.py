import unittest
import gameboard
import hexcell
import piece
import math


class PieceTestCase(unittest.TestCase):

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

    def test_one_hive_rule(self):
        self.assertFalse(
            self.white_ant_0.get_moves(self.game_board))

    def test_freedom_to_move_rule(self):
        pocket = hexcell.HexCell(-1, 1)
        self.assertNotIn(pocket,
                         self.white_ant_1.get_moves(self.game_board))

    def test_place_piece(self):
        new_piece = piece.Piece(
            piece.PieceType.ANT,
            piece.Color.BLACK,
            2)

        calculated_moves = new_piece.get_moves(self.game_board)
        expected_move_coords = (
            (-1, -1),
            (-1, 3),
            (-2, 3),
            (-2, -2),
            (-3, 2)
        )

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def test_bee(self):
        calculated_moves = self.black_bee_0.get_moves(self.game_board)
        expected_move_coords = (
            (-3, 1),
            (-1, 1))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def test_spider(self):
        white_spider_1 = piece.Piece(
            piece.PieceType.SPIDER,
            piece.Color.WHITE,
            1,
            2, -1)

        calculated_moves = white_spider_1.get_moves(self.game_board)
        expected_move_coords = (
            (0, 2),
            (0, -1))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def test_beetle(self):
        black_beetle_1 = piece.Piece(
            piece.PieceType.BEETLE,
            piece.Color.BLACK,
            1,
            -1, -1)

        calculated_moves = black_beetle_1.get_moves(self.game_board)
        expected_move_coords = (
            (-2, -1),
            (-2, 0),
            (-1, 0),
            (0, -1))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def test_grasshopper(self):
        white_grasshopper_0 = piece.Piece(
            piece.PieceType.GRASSHOPPER,
            piece.Color.WHITE,
            0,
            -1, -1)
        calculated_moves = white_grasshopper_0.get_moves(self.game_board)

        expected_move_coords = (
            (-1, 1),
            (-3, 1))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def test_ant(self):
        calculated_moves = self.white_ant_1.get_moves(self.game_board)

        expected_move_coords = (
            (-3, -1),
            (-2, -1),
            (-1, -1),
            (0, -1),
            (1, -2),
            (2, -1),
            (2, -1),
            (1, 0),
            (1, 1),
            (0, 2),
            (-1, 3),
            (-2, 3),
            (-2, 2),
            (-3, 2))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def assert_move_coords(self, calculated_moves, expected_move_coords):
        expected_moves = [hexcell.HexCell(q, r)
                          for q, r in expected_move_coords]

        missing_moves = []
        for expected_move in expected_moves:
            matched_calculated_move = next(
                (x for x in calculated_moves
                 if not x.has_same_coordinates(expected_move)),
                None)

            if not matched_calculated_move:
                missing_moves.append(expected_move)

        extra_moves = []
        for calculated_move in calculated_moves:
            matched_expected_move = next(
                (x for x in expected_moves
                 if not x.has_same_coordinates(calculated_move)),
                None)

            if not matched_expected_move:
                extra_moves.append(calculated_move)

        with self.subTest("Missing moves"):
            self.assertFalse(missing_moves)
        with self.subTest("Extra moves"):
            self.assertFalse(extra_moves)

    def test_place_in_empty_gameboard(self):
        empty_gameboard = gameboard.GameBoard()
        new_piece = piece.Piece(
            piece.PieceType.SPIDER,
            piece.Color.WHITE,
            0)
        self.assertTrue(new_piece.get_moves(empty_gameboard))


class PieceProtobufTestCase(unittest.TestCase):

    def test_conversion(self):
        for piece_type in piece.PieceType:
            for color in piece.Color:
                for piece_num in range(4):
                    for q, r in ((0, 0), (-4, 63), (math.nan, math.nan)):
                        starting_piece = piece.Piece(
                            piece_type, color, piece_num, q, r)
                        with self.subTest(starting_piece):
                            protobuf = starting_piece.to_protobuf()
                            end_piece = piece.Piece.from_protobuf(protobuf)
                            self.assertEqual(starting_piece, end_piece)
                            self.assertIsNot(starting_piece, end_piece)
