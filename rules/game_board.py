from rules.hexgrid import HexGrid
from rules.piece import Piece
import math
import collections


class GameBoard(HexGrid):

    _piece_creature_counts = {
        Piece.Creature.BEE: 1,
        Piece.Creature.SPIDER: 2,
        Piece.Creature.BEETLE: 2,
        Piece.Creature.GRASSHOPPER: 3,
        Piece.Creature.ANT: 3
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
        for color in Piece.Color:
            for creature, piece_count in self._piece_creature_counts.items():
                for piece_number in range(piece_count):
                    self._unplaced_pieces.add(
                        Piece(creature, color, piece_number))
        self.player_turn = Piece.Color.WHITE

    def _init_from_json_object(self, json_object):
        for json_piece_object in json_object["pieces"]:
            board_piece = Piece(json_object=json_piece_object)
            if board_piece.is_placed():
                self._register_new_piece(board_piece)
            else:
                self._unplaced_pieces.add(board_piece)
        self.player_turn = Piece.Color[json_object["player_turn"]]

    def __eq__(self, other):
        if self._unplaced_pieces != other._unplaced_pieces:
            return False
        if self._placed_pieces != other._placed_pieces:
            return False
        return True

    def place(self, new_piece):
        local_instance = self._get_piece(new_piece)
        assert local_instance
        assert new_piece.color == self.player_turn

        available_moves = local_instance.get_moves(self)
        if self.get_cell(new_piece.q, new_piece.r) not in available_moves:
            raise ValueError("Piece does not represent a valid move:" +
                             str(local_instance) + " to " + str(new_piece))

        self.force_place(new_piece)
        self.player_turn = new_piece.opposite_color()

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
                    piece.creature == unplaced_piece.creature and
                    piece.piece_number == unplaced_piece.piece_number):
                return unplaced_piece

        for placed_piece in self._placed_pieces:
            if (piece.color == placed_piece.color and
                    piece.creature == placed_piece.creature and
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

        next_unplaced_piece = Piece(
            unplaced_piece.creature,
            unplaced_piece.color,
            unplaced_piece.piece_number + 1)

        max_piece_count = self._piece_creature_counts[unplaced_piece.creature]
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
        if Piece.is_piece(bottom_piece):
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
        piece_moves = collections.defaultdict(list)

        for placed_piece in self.get_placed_pieces(self.player_turn):
            moves = placed_piece.get_moves(self)
            if moves:
                piece_moves[placed_piece] = moves

        # Remove later numbers of the same unplaced piece.
        unplaced_types = collections.defaultdict(
            lambda: collections.defaultdict(list))
        for unplaced_piece in self.get_unplaced_pieces(self.player_turn):
            unplaced_types[unplaced_piece.color][unplaced_piece.creature].append(
                unplaced_piece)

        for piece_dict in unplaced_types.values():
            for creature_list in piece_dict.values():
                creature_list.sort(key=lambda x: x.piece_number)
                unplaced_piece = creature_list[0]
                piece_moves[unplaced_piece] = unplaced_piece.get_moves(self)

        return piece_moves

    def to_json_object(self):
        pieces = [x.to_json_object() for x in self.get_pieces()]
        return {
            "pieces": pieces,
            "player_turn": self.player_turn.name
        }
