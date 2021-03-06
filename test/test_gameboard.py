import unittest
from rules.game_board import GameBoard
from rules.piece import Piece


class GameBoardTestCase(unittest.TestCase):

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

    def test_equal_empty(self):
        first = GameBoard()
        second = GameBoard()
        self.assertEqual(first, second)

    def test_equal(self):
        self.assertEqual(self.game_board, self.game_board)

    def test_not_equal(self):
        empty_board = GameBoard()
        self.assertNotEqual(empty_board, self.game_board)

    def test_get_pieces(self):
        for color in (None, Piece.Color.BLACK, Piece.Color.WHITE):
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
        for starting_piece in self.starting_pieces:
            with self.subTest(str(starting_piece)):
                self.assertNotIn(starting_piece, unplaced_pieces)

    def test_piece_stacking(self):
        beetle_on_top_of_hive = Piece(
            Piece.Creature.BEETLE,
            Piece.Color.WHITE,
            0,
            -1, 0)

        self.game_board.force_place(beetle_on_top_of_hive)
        self.assertIs(beetle_on_top_of_hive,
                      self.game_board.get_cell(
                          beetle_on_top_of_hive.q, beetle_on_top_of_hive.r))

        # The bottom piece is still registered on the board.
        self.assertIn(self.black_beetle_0,
                      self.game_board.get_placed_pieces())

        self.game_board.force_place(Piece(
            Piece.Creature.BEETLE,
            Piece.Color.WHITE,
            0,
            0, -1
        ))

        self.assertIs(self.black_beetle_0,
                      self.game_board.get_cell(
                          self.black_beetle_0.q, self.black_beetle_0.r))

    def test_piece_unstacking(self):
        beetle_on_top_of_hive = Piece(
            Piece.Creature.BEETLE,
            Piece.Color.WHITE,
            0,
            -1, 0)
        beetle_off_of_hive = Piece(
            Piece.Creature.BEETLE,
            Piece.Color.WHITE,
            0,
            -1, -1)

        self.game_board.force_place(beetle_on_top_of_hive)
        self.game_board.force_place(beetle_off_of_hive)

        self.assertIs(beetle_off_of_hive, self.game_board.get_cell(
            beetle_off_of_hive.q, beetle_off_of_hive.r))
        self.assertIs(beetle_off_of_hive, self.game_board.get_cell(
            beetle_off_of_hive.q, beetle_off_of_hive.r))

    def test_place_floating(self):
        floating_piece = Piece(
            Piece.Creature.BEETLE,
            Piece.Color.WHITE,
            0,
            0, -2)

        with self.assertRaises(ValueError):
            self.game_board.place(floating_piece)

    def test_invalid_move(self):
        """No valid move exists from the starting configuration to perform
        this move."""
        invalid_placement = Piece(
            Piece.Creature.BEE,
            Piece.Color.WHITE,
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

        self.assertNotIn(
            self.game_board._get_piece(Piece(
                Piece.Creature.GRASSHOPPER,
                Piece.Color.WHITE,
                2
            )),
            available_moves.keys()
        )

    def test_json_conversion(self):
        json_object = self.game_board.to_json_object()
        end_game_board = GameBoard(json_object=json_object)

        # More granular assertions than below - provide more info on failure.
        self.assertFalse(
            end_game_board._placed_pieces - self.game_board._placed_pieces)
        self.assertFalse(
            self.game_board._placed_pieces - end_game_board._placed_pieces)

        self.assertFalse(
            end_game_board._unplaced_pieces - self.game_board._unplaced_pieces)
        self.assertFalse(
            self.game_board._unplaced_pieces - end_game_board._unplaced_pieces)

        self.assertEqual(self.game_board, end_game_board)
        self.assertIsNot(self.game_board, end_game_board)

    def test_fourth_move_bee(self):
        self.game_board._remove_placed(self.white_bee_0)
        self.game_board._remove_placed(self.black_bee_0)

        piece_moves = self.game_board.get_moves()
        self.assertEqual(len(piece_moves), 1, piece_moves)

        for piece in piece_moves.keys():
            self.assertEqual(piece.creature, Piece.Creature.BEE)

    def test_move_before_bee(self):
        self.game_board._remove_placed(self.white_bee_0)
        self.game_board._remove_placed(self.black_bee_0)
        self.game_board._remove_placed(self.black_ant_1)
        self.game_board._remove_placed(self.white_ant_1)

        piece_moves = self.game_board.get_moves()
        self.assertNotIn(self.white_ant_0, piece_moves.keys())
        self.assertNotIn(self.white_spider_0, piece_moves.keys())
        self.assertIn(self.white_bee_0, piece_moves.keys())

    def test_bee_is_unplaced(self):
        self.assertFalse(
            self.game_board.bee_is_unplaced(self.game_board.player_turn))

        self.game_board._remove_placed(self.white_bee_0)
        self.assertTrue(
            self.game_board.bee_is_unplaced(
                Piece.Color.WHITE))
