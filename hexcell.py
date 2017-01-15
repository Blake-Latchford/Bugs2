#!/usr/bin/env python3


class HexCell:
    """A single cell in a hexagonal grid.
    
    Attributes:
        q, r, s - The coordinates of the hex.
    """

    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.s = -q - r

    def __eq__(self, other):
        return self.has_same_coordinates(other)

    def has_same_coordinates(self, other):
        return (self.q == other.q and
                self.r == other.r and
                self.s == other.s)
    
    def __hash__(self):
        return hash((self.q, self.r, self.s))
    
    def __str__(self):
        return "(" + str(self.q) + "," + str(self.r) + "," + str(self.s) + ")"

    def __repr__(self):
        return str(self)

    def distance(self, other):
        return (abs(self.q - other.q) + abs(self.r - other.r) + abs(self.s - other.s)) / 2
