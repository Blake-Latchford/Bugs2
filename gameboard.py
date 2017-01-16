#!/usr/bin/env python3

import hexgrid


class GameBoard(hexgrid.HexGrid):

    def __init__(self):
        super().__init__()

    def get_placed_pieces(self):
        return self._populated_cells.values()
