#!/usr/bin/env python3


from enum import Enum, unique
from hexcell import HexCell


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


class HexGrid:
    """A grid of HexCells.
    Registered cells are preserved. As this represents the entire infinite hex
    plane, any cell can be gotten. However, only registered cells are guaranteed
    to be identical on future calls.
    """

    _direction_coord_change = {
        Direction.Q_POS: (+1, -1,  0),
        Direction.R_POS: (+1,  0, -1),
        Direction.S_POS: (0, +1, -1),
        Direction.Q_NEG: (-1, +1,  0),
        Direction.R_NEG: (-1,  0, +1),
        Direction.S_NEG: (0, -1, +1)
    }

    def __init__(self):
        self._populated_cells = {}

    def get_cell(self, q, r):
        """Get the cell at the specified coordinates. If no cell is registered
        at that location, create a temporary new cell."""

        coords = (q, r)
        if coords in self._populated_cells:
            return self._populated_cells[coords]
        return HexCell(q, r)

    def register_cell(self, hex_cell):
        """Register a hex cell to be retained in the grid."""
        assert (hex_cell.q, hex_cell.r) not in self._populated_cells

        self._populated_cells[(hex_cell.q, hex_cell.r)] = hex_cell

    def reset(self):
        self._populated_cells = {}

    def get_neighbors(self, hex_cell):
        """Get the set of cells adjacent to hex_cell"""
        neighbors = []
        for direction in Direction:
            neighbors.append(self.get_neighbor(hex_cell, direction))
        return neighbors

    def get_neighbor(self, hex_cell, direction):
        """Get the HexCell adjacent to hex_cell in the specified direction."""

        coord_change = self._direction_coord_change[direction]

        q = hex_cell.q + coord_change[0]
        r = hex_cell.r + coord_change[1]
        s = hex_cell.s + coord_change[2]

        assert q + r + s == 0

        return self.get_cell(q, r)

    def breadth_first_search(self, start, max_distance, filter_function=None):
        """Do a breadth first search from start and going max_distance
        hexes away.

        Arguments:
            start - HexCell at which to start the search.
            max_distance - Maximum Manhattan distance to search.
            filter_function - If specified, then can be used to prevent hexes
                from being accepted in a search. Expected signature is:
                filter_function(hex_cell, distance) -> bool
                If the return value is true, hex_cell is added to the results.
                distance is the Manhattan distance from start.
        """
        search_results = []
        previous_distance_result = [start]
        visited = set([start])

        for search_results_index in range(max_distance):
            distance = search_results_index + 1
            current_distance_result = []

            for hex_cell in previous_distance_result:
                for neighbor in self.get_neighbors(hex_cell):
                    if (neighbor not in visited and
                            (not filter_function or filter_function(neighbor, distance))):
                        current_distance_result.append(neighbor)
                        visited.add(neighbor)

            search_results.append(current_distance_result)
            previous_distance_result = current_distance_result

        return search_results
