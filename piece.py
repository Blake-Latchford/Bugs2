#!/usr/bin/env python3

from enum import Enum, unique
import hexcell
import math


class Piece(hexcell.HexCell):

    @unique
    class PieceType(Enum):
        BEE = 0
        SPIDER = 1
        BEETLE = 2
        GRASSHOPPER = 3
        ANT = 4
        # MOSQUITO = 5
        # LADYBUG = 6
        # PILLBUG = 7

    @unique
    class Color(Enum):
        WHITE = 0
        BLACK = 1

    def __init__(self, piece_type, color, piece_number,
                 q=math.nan,
                 r=math.nan):
        super().__init__(q, r)
        self.piece_type = piece_type
        self.color = color
        self.piece_number = piece_number

    def __eq__(self, other):
        if not super().__eq__(other):
            return False

        if self.piece_type != other.piece_type:
            return False

        if self.color != other.color:
            return False

        if self.piece_number != other.piece_number:
            return False

        return True

    def __hash__(self):
        return hash((super().__hash__(),
                     self.piece_type,
                     self.color,
                     self.piece_number))

    def get_moves(self, game_board):
        if not self.can_move(game_board):
            return []

        piece_moves = {
            self.PieceType.BEE: self.get_moves_BEE,
            self.PieceType.SPIDER: self.get_moves_SPIDER,
            self.PieceType.BEETLE: self.get_moves_BEETLE,
            self.PieceType.GRASSHOPPER: self.get_moves_GRASSHOPPER,
            self.PieceType.ANT: self.get_moves_ANT
        }
        return piece_moves[self.piece_type](game_board)

    def can_move(self, game_board):
        partitions = [[x] for x in self._get_piece_neighbors(self, game_board)]
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
        space_neighbors = self._get_space_neighbors(self, game_board)
        movable_neighbors = (
            neighbor for neighbor in space_neighbors
            if self._freedom_to_move(self, neighbor, game_board))
        return movable_neighbors

    def get_moves_SPIDER(self, game_board):
        raise NotImplementedError

    def get_moves_BEETLE(self, game_board):
        raise NotImplementedError

    def get_moves_GRASSHOPPER(self, game_board):
        raise NotImplementedError

    def get_moves_ANT(self, game_board):
        raise NotImplementedError

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

        return (self._is_piece(clockwise_neighbor) !=
                self._is_piece(counterclockwise_neighbor))

    def _get_piece_neighbors(self, hex_cell, game_board):
        return {x for x in hex_cell.get_neighbors(game_board)
                if Piece._is_piece(x)}

    def _get_space_neighbors(self, hex_cell, game_board):
        return {x for x in hex_cell.get_neighbors(game_board)
                if Piece._is_space(x)}

    @classmethod
    def _is_piece(cls, hex_cell):
        return hasattr(hex_cell, "get_moves")

    @classmethod
    def _is_space(cls, hex_cell):
        return not cls._is_piece(hex_cell)
