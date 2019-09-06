import unittest
from unittest.mock import patch
import rules.gameboard as gameboard
import console_client.console_client as console_client


@patch("builtins.input")
class ConsoleClientTestCase(unittest.TestCase):

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
