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

    def __init__(self, json_object=None):
        super().__init__()

        self._placed_pieces = set()
        self._unplaced_pieces = set()

        if not json_object:
            self._init_empty()
        else:
            self._init_from_json_object(json_object)

    def _init_empty(self):
        for color in piece.Color:
            for piece_type, piece_count in self._piece_type_counts.items():
                if piece_count > 0:
                    self._unplaced_pieces.add(
                        piece.Piece(piece_type, color, 0))

    def _init_from_json_object(self, json_object):
        assert json_object

        for json_piece_object in json_object["pieces"]:
            board_piece = piece.Piece(json_object=json_piece_object)
            if board_piece.is_placed():
                self._placed_pieces.add(board_piece)
            else:
                self._unplaced_pieces.add(board_piece)

    def __eq__(self, other):
        if self._unplaced_pieces != other._unplaced_pieces:
            return False
        if self._placed_pieces != other._placed_pieces:
            return False
        return True

    def place(self, new_piece):
        local_instance = self._get_piece(new_piece)
        assert local_instance

        available_moves = local_instance.get_moves(self)
        if self.get_cell(new_piece.q, new_piece.r) not in available_moves:
            raise ValueError("Piece does not represent a valid move:" +
                             str(local_instance) + " to " + str(new_piece))

        self.force_place(new_piece)

    def force_place(self, new_piece):
        """Like place, but doesn't verify game mechanics.
        Storage consistency assumptions are validated however."""

        local_instance = self._get_piece(new_piece)
        self._validate_placement(new_piece, local_instance)
        self._remove_replaced_piece(local_instance)
        self._register_new_piece(new_piece)

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

    def _validate_placement(self, new_piece, local_instance):
        # Make sure this new_piece is valid to place.
        if local_instance is new_piece:
            raise ValueError(
                "Unable to place new_piece already on game board:" +
                str(new_piece))

        if not local_instance:
            raise ValueError(
                "Piece not available for placement:" + str(new_piece))

        if math.isnan(new_piece.q) or math.isnan(new_piece.r):
            raise ValueError("Piece does not have coordinates specified:" +
                             str(new_piece))

    def _remove_replaced_piece(self, replaced_piece):
        self._remove_unplaced(replaced_piece)
        self._remove_placed(replaced_piece)

    def _remove_unplaced(self, unplaced_piece):
        if unplaced_piece not in self._unplaced_pieces:
            return

        next_unplaced_piece = piece.Piece(
            unplaced_piece.piece_type,
            unplaced_piece.color,
            unplaced_piece.piece_number + 1)

        max_piece_count = self._piece_type_counts[unplaced_piece.piece_type]
        if next_unplaced_piece.piece_number < max_piece_count:
            self._unplaced_pieces.add(next_unplaced_piece)
        self._unplaced_pieces.remove(unplaced_piece)

    def _remove_placed(self, placed_piece):
        if placed_piece not in self._placed_pieces:
            return

        self._placed_pieces.remove(placed_piece)
        self.unregister_cell(placed_piece)

        if placed_piece.above:
            self.register_cell(placed_piece.above)

    def _register_new_piece(self, new_piece):
        bottom_piece = self.get_cell(new_piece.q, new_piece.r)
        if piece.Piece.is_piece(bottom_piece):
            self.unregister_cell(bottom_piece)
            new_piece.above = bottom_piece

        self.register_cell(new_piece)
        self._placed_pieces.add(new_piece)

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

    def get_moves(self):
        moves = dict()

        for piece in self._placed_pieces | self._unplaced_pieces:
            moves[piece] = piece.get_moves(self)

        return moves

    def to_json_object(self):
        pieces = [x.to_json_object() for x in self.get_pieces()]
        return {"pieces": pieces}
