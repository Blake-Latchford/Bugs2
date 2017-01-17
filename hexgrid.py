#!/usr/bin/env python3


from hexcell import HexCell


class HexGrid:
    """A grid of HexCells.
    Registered cells are preserved. As this represents the entire infinite hex
    plane, any cell can be gotten. However, only registered cells are guaranteed
    to be identical on future calls.
    """

    def __init__(self):
        self._registered_cells = {}

    def get_cell(self, q, r):
        """Get the cell at the specified coordinates. If no cell is registered
        at that location, create a temporary new cell."""

        coords = (q, r)
        if coords in self._registered_cells:
            return self._registered_cells[coords]
        return HexCell(q, r)

    def register_cell(self, hex_cell):
        """Register a hex cell to be retained in the grid."""
        assert (hex_cell.q, hex_cell.r) not in self._registered_cells

        self._registered_cells[(hex_cell.q, hex_cell.r)] = hex_cell

    def reset(self):
        self._registered_cells = {}

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
                for neighbor in hex_cell.get_neighbors(self):
                    if (neighbor not in visited and
                            (not filter_function or filter_function(neighbor, distance))):
                        current_distance_result.append(neighbor)
                        visited.add(neighbor)

            search_results.append(current_distance_result)
            previous_distance_result = current_distance_result

        return search_results
