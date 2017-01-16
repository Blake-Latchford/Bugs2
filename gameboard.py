#!/usr/bin/env python3

import hexgrid


class GameBoard(hexgrid.HexGrid):

    def __init__(self):
        super().__init__()

    def get_placed_pieces(self, color=None):
        if color is None:
            return self._populated_cells.values()
        return (x for x in self._populated_cells.values() if x.color == color)