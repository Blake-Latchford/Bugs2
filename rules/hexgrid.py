from . import hexcell


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
        return hexcell.HexCell(q, r)

    def register_cell(self, hex_cell):
        """Register a hex cell to be retained in the grid."""
        assert (hex_cell.q, hex_cell.r) not in self._registered_cells

        self._registered_cells[(hex_cell.q, hex_cell.r)] = hex_cell

    def unregister_cell(self, hex_cell):
        assert self._registered_cells[(hex_cell.q, hex_cell.r)] is hex_cell

        self._registered_cells.pop((hex_cell.q, hex_cell.r), None)

    def reset(self):
        self._registered_cells = {}

    def __repr__(self):
        return repr(self._registered_cells)
