import unittest
from unittest.mock import patch
import rules.gameboard as gameboard
import console_client.console_client as console_client


@patch("builtins.input")
class ConsoleClientTestCase(unittest.TestCase):

    def setUp(self):
        self.gameboard = gameboard.GameBoard()
        self.console_client = console_client.ConsoleClient(self.gameboard)

    def test_first_moves(self, input_magic_mock):
        for i in range(len(self.gameboard.get_moves())):
            with self.subTest(i):
                self.gameboard = gameboard.GameBoard()
                self.console_client = console_client.ConsoleClient(
                    self.gameboard)

                selections = [str(x) for x in (i, 0, 0)]
                input_magic_mock.reset_mock()
                input_magic_mock.side_effect = selections

                self.console_client.move()
                self.console_client.move()

                self.assertEqual(
                    input_magic_mock.call_count,
                    len(selections))
