#!/usr/bin/env python3

import gameboard
import unittest
import piece


class FullGameBoardTestCase(unittest.TestCase):

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
            self.game_board.place(starting_piece)

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
