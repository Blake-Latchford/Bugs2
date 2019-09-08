import unittest
from rules.gameboard import GameBoard
from rules.hexcell import HexCell
from rules.piece import Piece
import math


class PieceMovementTestCase(unittest.TestCase):

    def setUp(self):
        self.game_board = GameBoard()

        # Setup to test various move options.
        # Layout is as follows, with white spider 0 (ws0) at 0,0.
        # bB0 is black bee zero, and bb0 is black beetle zero.
        #
        #               wB0
        # wa1 ba0 bb0 ws0
        #       bB0     wa0
        #             ba1

        self.white_spider_0 = Piece(
            Piece.Creature.SPIDER,
            Piece.Color.WHITE,
            0,
            0, 0)
        self.white_bee_0 = Piece(
            Piece.Creature.BEE,
            Piece.Color.WHITE,
            0,
            1, -1)
        self.white_ant_0 = Piece(
            Piece.Creature.ANT,
            Piece.Color.WHITE,
            0,
            0, 1)
        self.white_ant_1 = Piece(
            Piece.Creature.ANT,
            Piece.Color.WHITE,
            1,
            -3, 0)

        self.black_beetle_0 = Piece(
            Piece.Creature.BEETLE,
            Piece.Color.BLACK,
            0,
            -1, 0)
        self.black_bee_0 = Piece(
            Piece.Creature.BEE,
            Piece.Color.BLACK,
            0,
            -2, 1)
        self.black_ant_0 = Piece(
            Piece.Creature.ANT,
            Piece.Color.BLACK,
            0,
            -2, 0)
        self.black_ant_1 = Piece(
            Piece.Creature.ANT,
            Piece.Color.BLACK,
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
        pocket = HexCell(-1, 1)
        self.assertNotIn(pocket,
                         self.white_ant_1.get_moves(self.game_board))

    def test_place_wrong_player(self):
        new_piece = Piece(
            Piece.Creature.ANT,
            Piece.Color.BLACK,
            2)
        self.assertFalse(new_piece.get_moves(self.game_board))

    def test_move_wrong_player(self):
        self.assertFalse(self.black_ant_1.get_moves(self.game_board))

    def test_place_piece(self):
        self.game_board.player_turn = Piece.Color.BLACK
        new_piece = Piece(
            Piece.Creature.ANT,
            Piece.Color.BLACK,
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
        self.game_board.player_turn = Piece.Color.BLACK
        calculated_moves = self.black_bee_0.get_moves(self.game_board)
        expected_move_coords = (
            (-3, 1),
            (-1, 1))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def test_spider(self):
        white_spider_1 = Piece(
            Piece.Creature.SPIDER,
            Piece.Color.WHITE,
            1,
            2, -1)

        calculated_moves = white_spider_1.get_moves(self.game_board)
        expected_move_coords = (
            (0, 2),
            (0, -1))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def test_beetle(self):
        self.game_board.player_turn = Piece.Color.BLACK
        black_beetle_1 = Piece(
            Piece.Creature.BEETLE,
            Piece.Color.BLACK,
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
        white_grasshopper_0 = Piece(
            Piece.Creature.GRASSHOPPER,
            Piece.Color.WHITE,
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
        expected_moves = [HexCell(q, r)
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


class PieceIndependentTestCase(unittest.TestCase):

    def test_place_in_empty_gameboard(self):
        empty_gameboard = GameBoard()
        new_piece = Piece(
            Piece.Creature.SPIDER,
            Piece.Color.WHITE,
            0)
        self.assertTrue(new_piece.get_moves(empty_gameboard))

    def test_place_second_move(self):
        test_gameboard = GameBoard()
        test_gameboard.place(
            Piece(
                Piece.Creature.SPIDER,
                Piece.Color.WHITE,
                0, 0, 0))
        new_piece = Piece(
            Piece.Creature.SPIDER,
            Piece.Color.BLACK,
            0)
        self.assertTrue(new_piece.get_moves(test_gameboard))

    def test_is_not_placed(self):
        new_piece = Piece(
            Piece.Creature.SPIDER,
            Piece.Color.WHITE,
            0)
        self.assertFalse(new_piece.is_placed())

    def test_is_placed(self):
        new_piece = Piece(
            Piece.Creature.SPIDER,
            Piece.Color.WHITE,
            0,
            0, 0)
        self.assertTrue(new_piece.is_placed())

    def test_json_conversion(self):
        for piece_type in Piece.Creature:
            for color in Piece.Color:
                for piece_num in range(4):
                    for q, r in ((0, 0), (-4, 63), (math.nan, math.nan)):
                        starting_piece = Piece(
                            piece_type, color, piece_num, q, r)
                        with self.subTest(starting_piece):
                            json_object = starting_piece.to_json_object()
                            end_piece = Piece(json_object=json_object)
                            self.assertEqual(starting_piece, end_piece)
                            self.assertIsNot(starting_piece, end_piece)

    def test_get_moved_absolute_on_to_board(self):
        old_piece = Piece(
            Piece.Creature.SPIDER,
            Piece.Color.WHITE,
            0)
        new_piece = old_piece.get_moved_absolute(0, 0)

        self.assertTrue(math.isnan(old_piece.q))
        self.assertTrue(math.isnan(old_piece.r))

        self.assertEqual(new_piece.q, 0)
        self.assertEqual(new_piece.r, 0)

    def test_get_moved_absolute(self):
        old_piece = Piece(
            Piece.Creature.SPIDER,
            Piece.Color.WHITE,
            0,
            0, 0)
        new_piece = old_piece.get_moved_absolute(15, -6)

        self.assertEqual(old_piece.q, 0)
        self.assertEqual(old_piece.r, 0)

        self.assertEqual(new_piece.q, 15)
        self.assertEqual(new_piece.r, -6)
