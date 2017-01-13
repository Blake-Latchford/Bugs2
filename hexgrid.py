#!/usr/bin/env python3

from enum import Enum, unique

@unique
class Direction(Enum):
    """The six cardinal directions on a hexigonal grid
    Named as <axis>_<sign>, so Q_POS is in the positive direction
    on the q axis.
    """
    Q_POS = 1
    R_POS = 2
    S_POS = 3
    Q_NEG = 4
    R_NEG = 5
    S_NEG = 6

    def next_clockwise(self):
        direction_list = list(Direction)
        self_index = direction_list.index(self)
        return direction_list[(self_index + 1) % len(direction_list)]

    def next_counterclockwise(self):
        direction_list = list(Direction)
        self_index = direction_list.index(self)
        return direction_list[self_index - 1]

class HexCell:
    def __init__(self, hex_grid, q, r):
        self.hex_grid = hex_grid
        self.q = q
        self.r = r
        self.s = -q - r

    def __eq__(self, other):
        return self.has_same_coordinates(other)

    def has_same_coordinates(self, other):
        return (self.q == other.q and
                self.r == other.r and
                self.s == other.s)

    def get_neighbors(self):
        pass

    def get_neighbor(self, direction):
        pass

    def breadth_first_search(self, max_distance, filter_function=None):
        pass

    def distance(self, other):
        pass

class HexGrid:
    def __init__(self):
        pass
