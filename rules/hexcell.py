from enum import Enum, unique
import math


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
    """A single cell in a hexagonal grid.

    Attributes:
        q, r, s - The coordinates of the hex.
    """

    _direction_coord_change = {
        Direction.Q_POS: (+1, +0, -1),
        Direction.R_POS: (+0, +1, -1),
        Direction.S_POS: (+1, -1, +0),
        Direction.Q_NEG: (-1, +0, +1),
        Direction.R_NEG: (+0, -1, +1),
        Direction.S_NEG: (-1, +1, +0)
    }

    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.s = -q - r

    def __eq__(self, other):
        return self.has_same_coordinates(other)

    def has_same_coordinates(self, other):
        """Same as __eq__, but accessible for derived classes."""

        for member_name in ("q", "r", "s"):
            if not self._are_equal_or_nan(
                    getattr(self, member_name),
                    getattr(other, member_name)):
                return False
        return True

    def _are_equal_or_nan(self, first, second):
        if math.isnan(first) and math.isnan(second):
            return True
        return first == second

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    def __str__(self):
        return "(" + str(self.q) + "," + str(self.r) + "," + str(self.s) + ")"

    def __repr__(self):
        return str(self)

    def __sub__(self, other):
        return HexCell(
            self.q - other.q,
            self.r - other.r
        )

    def __add__(self, other):
        return HexCell(
            self.q + other.q,
            self.r + other.r
        )

    def rotate_clockwise_about_origin(self):
        return HexCell(-self.s, -self.q)

    def rotate_counterclockwise_about_origin(self):
        return HexCell(-self.r, -self.s)

    def get_neighbors(self, hex_grid):
        """Get the cells adjacent to hex_cell in hex_grid in Direction order."""

        return (self.get_neighbor(hex_grid, direction)
                for direction in Direction)

    def get_neighbor(self, hex_grid, direction):
        """Get the HexCell adjacent to hex_cell in the specified direction."""

        coord_change = self._direction_coord_change[direction]

        q = self.q + coord_change[0]
        r = self.r + coord_change[1]
        s = self.s + coord_change[2]

        assert q + r + s == 0

        return hex_grid.get_cell(q, r)

    def get_offset_coords(self):
        col = self.q + (self.r - (self.r & 1)) // 2
        row = self.r

        return (col, row)

    @staticmethod
    def from_offset_cords(offset_cords):
        col, row = offset_cords

        q = col - (row - (row & 1)) // 2
        r = row
        return HexCell(q, r)
