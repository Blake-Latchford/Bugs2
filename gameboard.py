#!/usr/bin/env python3

import hexgrid
import piece
import math


class GameBoard(hexgrid.HexGrid):

    _piece_type_counts = {
        piece.PieceType.BEE: 1,
        piece.PieceType.SPIDER: 2,
        piece.PieceType.BEETLE: 2,
        piece.PieceType.GRASSHOPPER: 3,
        piece.PieceType.ANT: 3
    }

    def __init__(self):
        super().__init__()

        self._placed_pieces = set()
        self._unplaced_pieces = set()

        for color in piece.Color:
            for piece_type, piece_count in self._piece_type_counts.items():
                for piece_number in range(piece_count):
                    self._unplaced_pieces.add(
                        piece.Piece(piece_type, color, piece_number))

    def place(self, piece):
        local_instance = self._get_piece(piece)

        if not local_instance:
            raise ValueError("Piece not available for placement:" + str(piece))

        if math.isnan(piece.q) or math.isnan(piece.r):
            raise ValueError("Piece does not have coordinates specified:" +
                             str(piece))

        if local_instance in self._unplaced_pieces:
            self._unplaced_pieces.remove(local_instance)

        if local_instance in self._placed_pieces:
            self._placed_pieces.remove(local_instance)

        self.register_cell(piece)
        self._placed_pieces.add(piece)

    def _get_piece(self, piece):
        """Get a piece based on its color, type and number."""
        for unplaced_piece in self._unplaced_pieces:
            if (piece.color == unplaced_piece.color and
                    piece.piece_type == unplaced_piece.piece_type and
                    piece.piece_number == unplaced_piece.piece_number):
                return unplaced_piece

        for placed_piece in self._placed_pieces:
            if (piece.color == placed_piece.color and
                    piece.piece_type == placed_piece.piece_type and
                    piece.piece_number == placed_piece.piece_number):
                return placed_piece

        return None

    def get_pieces(self, color=None):
        pieces = set(self.get_placed_pieces(color))
        pieces.update(self.get_unplaced_pieces(color))
        return pieces

    def get_placed_pieces(self, color=None):
        if color is None:
            return self._placed_pieces
        return (x for x in self._placed_pieces if x.color == color)

    def get_unplaced_pieces(self, color=None):
        if color is None:
            return self._unplaced_pieces
        return (x for x in self._unplaced_pieces if x.color == color)
