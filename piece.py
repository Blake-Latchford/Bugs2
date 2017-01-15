#!/usr/bin/env python3

from enum import Enum
import hexcell


class Piece(hexcell.HexCell):

    PieceType = Enum((
        "BEE",
        "SPIDER",
        "BEETLE",
        "GRASSHOPPER",
        "ANT",
        "MOSQUITO",
        "LADYBUG",
        "PILLBUG"
    ))

    def __init__(self, piece_type, q, r):
        super().__init__(q, r)
        self.piece_type = piece_type
