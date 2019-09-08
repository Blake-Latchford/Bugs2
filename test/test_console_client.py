import unittest
from unittest.mock import patch
import rules.gameboard as gameboard
import rules.piece as piece
import console_client.console_client as console_client


@patch("builtins.input")
class ConsoleClientInputTestCase(unittest.TestCase):

    def test_first_moves(self, input_magic_mock):
        for i in range(len(gameboard.GameBoard().get_moves())):
            with self.subTest(i):
                new_gameboard = gameboard.GameBoard()
                new_console_client = console_client.ConsoleClient(
                    new_gameboard)

                selections = [str(x) for x in (i, 0, 0)]
                input_magic_mock.reset_mock()
                input_magic_mock.side_effect = selections

                result = new_console_client.get_move()
                self.assertTrue(result)
                new_gameboard.place(result)

                result = new_console_client.get_move()
                self.assertTrue(result)
                new_gameboard.place(result)

                self.assertEqual(
                    input_magic_mock.call_count,
                    len(selections))


class ConsoleClinetGameStateTestCase(unittest.TestCase):

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

        self.console_clinet = console_client.ConsoleClient(self.game_board)
        self.game_state = self.console_clinet.game_state_as_string()

    def test_contains_placed_pieces(self):
        placed_pieces = self.game_board.get_placed_pieces(
            self.game_board.player_turn)
        for placed_piece in placed_pieces:
            with self.subTest(placed_piece):
                placed_piece_string = self.console_clinet.piece_to_string(
                    placed_piece)
                self.assertIn(placed_piece_string, self.game_state)

    def test_contains_unplaced_pieces(self):
        unplaced_pieces = self.game_board.get_unplaced_pieces(
            self.game_board.player_turn)
        for unplaced_piece in unplaced_pieces:
            with self.subTest(unplaced_piece):
                unplaced_piece_string = self.console_clinet.piece_to_string(
                    unplaced_piece)
                self.assertIn(unplaced_piece_string, self.game_state)

    def test_player_turn(self):
        self.assertIn(
            str(self.game_board.player_turn.name),
            self.game_state)

    def test_piece_to_string(self):
        for piece_type, piece_type_string in self.console_clinet._piece_type_dict.items():
            for piece_color, piece_color_string in self.console_clinet._piece_color_dict.items():
                test_piece = piece.Piece(piece_type, piece_color, 0)
                with self.subTest(test_piece):
                    test_piece_string = self.console_clinet.piece_to_string(
                        test_piece)
                    self.assertIn(piece_type_string,
                                  test_piece_string)
                    self.assertIn(piece_color_string,
                                  test_piece_string)
                    self.assertIn(str(test_piece.piece_number),
                                  test_piece_string)

    def test_emtpy_piece_to_string(self):
        """Fail if throws"""
        self.console_clinet.piece_to_string(None)
