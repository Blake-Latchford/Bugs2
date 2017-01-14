#!/usr/bin/env python3

from enum import Enum, unique

@unique
class Direction(Enum):
    """The six cardinal directions on a hexigonal grid
    Named as <axis>_<sign>, so Q_POS is in the positive direction
    on the q axis.
    """
    Q_POS = 0
    R_POS = 1
    S_POS = 2
    Q_NEG = 3
    R_NEG = 4
    S_NEG = 5

class HexCell:

    direction_coord_change = {
        Direction.Q_POS : (+1, -1,  0),
        Direction.R_POS : (+1,  0, -1),
        Direction.S_POS : ( 0, +1, -1),
        Direction.Q_NEG : (-1, +1,  0),
        Direction.R_NEG : (-1,  0, +1),
        Direction.S_NEG : ( 0, -1, +1)
    }

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
        neighbors = []
        for direction in Direction:
            neighbors.append(self.get_neighbor(direction))
        return neighbors

    def get_neighbor(self, direction):
        coord_change = HexCell.direction_coord_change[direction]

        q = self.q + coord_change[0]
        r = self.r + coord_change[1]
        s = self.s + coord_change[2]

        assert q + r + s == 0

        neighbor = self.hex_grid.get_cell(q, r)
        if not neighbor:
            neighbor = HexCell(self.hex_grid, q, r)
        
        return neighbor


    def breadth_first_search(self, max_distance, filter_function=None):
        search_results = []
        previous_distance_result = [self]
        
        for result_index in range(max_distance):
            current_distance_result = []

            for hex_cell in previous_distance_result:
                if filter_function and filter_function(hex_cell):
                    current_distance_result.append(hex_cell)

            search_results.append(current_distance_result)
            previous_distance_result = current_distance_result;

        return search_results

    def distance(self, other):
        return (abs(self.q - other.q) + abs(self.r - other.r) + abs(self.s - other.s)) / 2

class HexGrid:
    def __init__(self):
        pass

    def get_cell(self, q, r):
        pass
