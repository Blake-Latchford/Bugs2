from enum import IntEnum, unique
from . import hexcell
import math
import functools


@functools.total_ordering
class Piece(hexcell.HexCell):

    @unique
    class Creature(IntEnum):
        BEE = 0
        SPIDER = 1
        BEETLE = 2
        GRASSHOPPER = 3
        ANT = 4
        # MOSQUITO = 5
        # LADYBUG = 6
        # PILLBUG = 7

    @unique
    class Color(IntEnum):
        WHITE = 0
        BLACK = 1

    def __init__(self, creature=None,
                 color=None,
                 piece_number=None,
                 q=math.nan,
                 r=math.nan,
                 json_object=None):
        """If json_object is specified, assume it is a hash of the other
        parameters. The enums are stored as strings."""

        if json_object:
            super().__init__(json_object["q"], json_object["r"])
            self.creature = self.Creature[json_object["creature"]]
            self.color = self.Color[json_object["color"]]
            self.piece_number = json_object["piece_number"]
        else:
            super().__init__(q, r)
            self.creature = creature
            self.color = color
            self.piece_number = piece_number
            self.above = None

    def __lt__(self, other):
        attribute_names = [
            "color",
            "creature",
            "piece_number",
        ]

        for attribute_name in attribute_names:
            self_attribute = int(getattr(self, attribute_name))
            other_attribute = int(getattr(other, attribute_name))
            if self_attribute < other_attribute:
                return True
            elif self_attribute > other_attribute:
                return False

        return False

    def __eq__(self, other):
        if not super().__eq__(other):
            return False

        if self.creature != other.creature:
            return False

        if self.color != other.color:
            return False

        if self.piece_number != other.piece_number:
            return False

        return True

    def __hash__(self):
        return hash((super().__hash__(),
                     self.creature,
                     self.color,
                     self.piece_number))

    def __str__(self):
        str_members = [
            self.color.name,
            self.creature.name,
            self.piece_number]
        return " ".join([str(x) for x in str_members])

    def __repr__(self):
        str_members = [
            self.color.name,
            self.creature.name,
            self.piece_number,
            super().__str__()]

        return " ".join([str(x) for x in str_members])

    # TODO why does everything take game_board?
    def get_moves(self, game_board):
        if math.nan in (self.q, self.r, self.s):
            return self._get_placements(game_board)

        if not self.can_move(game_board):
            return []

        method_name = "get_moves_" + self.creature.name
        return getattr(self, method_name)(game_board)

    def _get_placements(self, game_board):
        open_neighbors = set()
        non_enemy_adjacent_open_neighbors = set()

        if game_board.player_turn != self.color:
            return False

        if not list(game_board.get_placed_pieces(self.color)):
            oppisite_pieces = list(game_board.get_placed_pieces(
                self.opposite_color()))
            if not oppisite_pieces:
                return {game_board.get_cell(0, 0)}

            assert len(oppisite_pieces) == 1
            return oppisite_pieces[0].get_neighbors(game_board)

        for piece in game_board.get_placed_pieces(self.color):
            for open_neighbor in piece._get_space_neighbors(piece, game_board):
                open_neighbors.add(open_neighbor)

        for open_neighbor in open_neighbors:
            for neighbor_adjacent in open_neighbor.get_neighbors(game_board):
                try:
                    if neighbor_adjacent.color != self.color:
                        break
                except AttributeError:
                    continue
            else:
                non_enemy_adjacent_open_neighbors.add(open_neighbor)

        return non_enemy_adjacent_open_neighbors

    def can_move(self, game_board):
        if game_board.player_turn != self.color:
            return False

        partitions = [[x] for x in self._get_piece_neighbors(self, game_board)]

        if not partitions:  # Only one piece on the board.
            return False

        first_partition = partitions[0]
        first_partition.insert(0, self)
        search_index = 1

        while len(partitions) > 1 and search_index < len(first_partition):
            search_hex = first_partition[search_index]
            neighbors = self._get_piece_neighbors(search_hex, game_board)
            external_neighbors = (x for x in neighbors
                                  if x not in first_partition)

            for neighbor in external_neighbors:
                adjacent_partition = None
                for other_partition in partitions[1:]:
                    if neighbor in other_partition:
                        adjacent_partition = other_partition
                        break

                if adjacent_partition:
                    first_partition += adjacent_partition
                    partitions.remove(adjacent_partition)
                else:
                    first_partition.append(neighbor)

            search_index += 1

        return len(partitions) == 1

    def get_moves_BEE(self, game_board):
        return self._get_freedom_to_move_neighbors(self, game_board)

    def get_moves_SPIDER(self, game_board):
        visited = {self}
        previous_search_results = {self}

        for _ in range(3):
            next_search_results = set()
            for previous_search_result in previous_search_results:
                free_neighbors = self._get_freedom_to_move_neighbors(
                    previous_search_result, game_board)
                for neighbor in free_neighbors:
                    if neighbor not in visited:
                        next_search_results.add(neighbor)
                        visited.add(neighbor)
            previous_search_results = next_search_results

        return previous_search_results

    def get_moves_BEETLE(self, game_board):
        moves = set(self._get_freedom_to_move_neighbors(self, game_board))
        moves.union(self._get_piece_neighbors(self, game_board))

        return moves

    def get_moves_GRASSHOPPER(self, game_board):
        viable_landing_locations = set()
        for direction in hexcell.Direction:
            next_landing_location = self
            while self.is_piece(next_landing_location):
                next_landing_location = next_landing_location.get_neighbor(
                    game_board, direction)

            if self is not next_landing_location:
                viable_landing_locations.add(next_landing_location)

        return viable_landing_locations

    def get_moves_ANT(self, game_board):
        visited = set()
        unvisited = [self]

        while unvisited:
            next_unvisited = unvisited.pop()
            visited.add(next_unvisited)
            free_neighbors = self._get_freedom_to_move_neighbors(
                next_unvisited, game_board)
            for neighbor in (x for x in free_neighbors if x not in visited):
                unvisited.append(neighbor)

        visited.remove(self)
        return visited

    def _get_piece_neighbors(self, hex_cell, game_board):
        return {x for x in hex_cell.get_neighbors(game_board)
                if Piece.is_piece(x)}

    def _get_space_neighbors(self, hex_cell, game_board):
        return {x for x in hex_cell.get_neighbors(game_board)
                if Piece._is_space(x)}

    def _get_freedom_to_move_neighbors(self, hex_cell, game_board):
        space_neighbors = self._get_space_neighbors(hex_cell, game_board)
        movable_neighbors = (
            neighbor for neighbor in space_neighbors
            if self._freedom_to_move(hex_cell, neighbor, game_board))
        return movable_neighbors

    def _freedom_to_move(self, start, end, game_board):
        diff = end - start

        clockwise_neighbor_hex = (
            diff.rotate_clockwise_about_origin() + start)
        counterclockwise_neighbor_hex = (
            diff.rotate_counterclockwise_about_origin() + start)

        clockwise_neighbor = game_board.get_cell(
            clockwise_neighbor_hex.q,
            clockwise_neighbor_hex.r)
        counterclockwise_neighbor = game_board.get_cell(
            counterclockwise_neighbor_hex.q,
            counterclockwise_neighbor_hex.r)

        clockwise_blocked = (
            self.is_piece(clockwise_neighbor) and
            clockwise_neighbor is not self)
        counterclockwise_blocked = (
            self.is_piece(counterclockwise_neighbor) and
            counterclockwise_neighbor is not self)

        return (clockwise_blocked != counterclockwise_blocked)

    def is_placed(self):
        if math.isnan(self.q) or math.isnan(self.r) or math.isnan(self.s):
            return False
        return True

    def get_moved_absolute(self, q, r):
        return Piece(
            self.creature,
            self.color,
            self.piece_number,
            q, r)

    @classmethod
    def is_piece(cls, hex_cell):
        return hasattr(hex_cell, "get_moves")

    @classmethod
    def _is_space(cls, hex_cell):
        return not cls.is_piece(hex_cell)

    def opposite_color(self):
        if self.color == self.Color.WHITE:
            return self.Color.BLACK
        return self.Color.WHITE

    def to_json_object(self):
        json_object = dict()
        json_object["creature"] = self.creature.name
        json_object["color"] = self.color.name
        json_object["piece_number"] = self.piece_number
        json_object["q"] = self.q
        json_object["r"] = self.r

        return json_object
