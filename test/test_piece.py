#!/usr/bin/env python3

import unittest
import gameboard
import hexcell
import piece


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
            piece.Piece.PieceType.SPIDER,
            piece.Piece.Color.WHITE,
            0,
            0, 0)
        self.white_bee_0 = piece.Piece(
            piece.Piece.PieceType.BEE,
            piece.Piece.Color.WHITE,
            0,
            1, -1)
        self.white_ant_0 = piece.Piece(
            piece.Piece.PieceType.ANT,
            piece.Piece.Color.WHITE,
            0,
            0, 1)
        self.white_ant_1 = piece.Piece(
            piece.Piece.PieceType.ANT,
            piece.Piece.Color.WHITE,
            1,
            -3, 0)

        self.black_beetle_0 = piece.Piece(
            piece.Piece.PieceType.BEETLE,
            piece.Piece.Color.BLACK,
            0,
            -1, 0)
        self.black_bee_0 = piece.Piece(
            piece.Piece.PieceType.BEE,
            piece.Piece.Color.BLACK,
            0,
            -2, 1)
        self.black_ant_0 = piece.Piece(
            piece.Piece.PieceType.ANT,
            piece.Piece.Color.BLACK,
            0,
            -2, 0)
        self.black_ant_1 = piece.Piece(
            piece.Piece.PieceType.ANT,
            piece.Piece.Color.BLACK,
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
            self.game_board.register_cell(starting_piece)

    def test_one_hive_rule(self):
        self.assertFalse(
            self.white_ant_0.get_moves(self.game_board))

    def test_freedom_to_move_rule(self):
        pocket = hexcell.HexCell(-1, 1)
        self.assertNotIn(pocket,
                         self.white_ant_1.get_moves(self.game_board))

    def test_bee(self):
        calculated_moves = self.black_bee_0.get_moves(self.game_board)
        expected_move_coords = (
            (-3, 1),
            (-1, 1))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def test_spider(self):
        white_spider_1 = piece.Piece(
            piece.Piece.PieceType.SPIDER,
            piece.Piece.Color.WHITE,
            1,
            2, -1)

        calculated_moves = white_spider_1.get_moves(self.game_board)
        expected_move_coords = (
            (0, 2),
            (0, -1))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def test_beetle(self):
        black_beetle_1 = piece.Piece(
            piece.Piece.PieceType.BEETLE,
            piece.Piece.Color.BLACK,
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
            piece.Piece.PieceType.GRASSHOPPER,
            piece.Piece.Color.WHITE,
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
            (-3, 2),
            (-3, 1),
            (-4, 1),
            (-5, 1))

        self.assert_move_coords(calculated_moves, expected_move_coords)

    def assert_move_coords(self, calculated_moves, expected_move_coords):
        expected_move_hexes = [hexcell.HexCell(q, r)
                               for q, r in expected_move_coords]

        missing_moves = []
        for expected_move_hex in expected_move_hexes:
            matching_calculated_moves = [
                x for x in calculated_moves
                if x.has_same_coordinates(expected_move_hex)]

            # This should never happen. Doesn't make sense.
            self.assertLess(len(matching_calculated_moves), 2)

            if not matching_calculated_moves:
                missing_moves.append(expected_move_hex)

        extra_moves = []
        for calculated_move_hex in calculated_moves:
            matching_expected_moves = [
                x for x in calculated_moves
                if x.has_same_coordinates(matching_expected_moves)]

            # This should never happen. Doesn't make sense.
            self.assertLess(len(matching_expected_moves), 2)

            if not matching_expected_moves:
                missing_moves.append(expected_move_hex)

        extra_moves = calculated_moves_set - expected_move_hexes_set

        self.assertFalse(missing_moves, "Missed moves.")
        self.assertFalse(extra_moves, "Extra moves.")
