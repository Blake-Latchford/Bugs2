import collections
from rules.piece import Piece
from rules.game_board import GameBoard


class ConsoleClient:

    # TODO these are needed to print the board.
    _piece_color_dict = {
        Piece.Color.WHITE: "w",
        Piece.Color.BLACK: "b"
    }

    _piece_creature_dict = {
        Piece.Creature.BEE: "B",
        Piece.Creature.SPIDER: "s",
        Piece.Creature.BEETLE: "b",
        Piece.Creature.GRASSHOPPER: "g",
        Piece.Creature.ANT: "a",
    }

    def __init__(self, game_board):
        self.game_board = game_board

    def get_move(self):
        unsorted_piece_moves = self.game_board.get_moves()
        sorted_keys = sorted(unsorted_piece_moves.keys())

        piece_moves = collections.OrderedDict()
        for sorted_key in sorted_keys:
            piece_moves[sorted_key] = unsorted_piece_moves[sorted_key]

        if not piece_moves:
            return None

        print("\n" * 100)

        while True:
            print("")
            print(self.game_state_as_string())
            for i, piece in enumerate(piece_moves.keys()):
                print(str(i) + ") " + str(piece))

            piece_index = int(input("Select source piece number:"))
            piece, valid_moves = \
                list(piece_moves.items())[piece_index]
            valid_moves = list(valid_moves)

            if len(valid_moves) > 1:
                for i, move in enumerate(valid_moves):
                    print(str(i) + ") " + str(move))
                dest_index = int(input("Select destination number:"))
            else:
                dest_index = 0
            dest = valid_moves[dest_index]

            return Piece(
                creature=piece.creature,
                color=piece.color,
                piece_number=piece.piece_number,
                q=dest.q,
                r=dest.r)

    def game_state_as_string(self):
        result = "Current player: " + \
            str(self.game_board.player_turn.name) + "\n"

        pieces_by_offset_coords = self._get_pieces_by_offset_coords()
        max_x, min_x, max_y, min_y = self._get_max_offset_coords(
            pieces_by_offset_coords.keys())

        for y in range(min_y, max_y + 1):
            # Offset odd rows.
            if y % 2 == 1:
                result += "  "

            for x in range(min_x, max_x + 1):
                coord = (x, y)
                if coord in pieces_by_offset_coords:
                    p = pieces_by_offset_coords[(x, y)]
                else:
                    p = None
                result += self.piece_to_string(p)
                result += " "

            result += "\n"

        return result

    def _get_pieces_by_offset_coords(self):
        pices_by_offset_coords = collections.defaultdict()
        for placed_piece in self.game_board.get_placed_pieces():
            offset_coords = placed_piece.get_offset_coords()
            pices_by_offset_coords[offset_coords] = placed_piece
        return pices_by_offset_coords

    @staticmethod
    def _get_max_offset_coords(offset_coords):
        if not offset_coords:
            return 0, 0, 0, 0

        max_x = max(coord[0] for coord in offset_coords)
        min_x = min(coord[0] for coord in offset_coords)
        max_y = max(coord[1] for coord in offset_coords)
        min_y = min(coord[1] for coord in offset_coords)

        return max_x, min_x, max_y, min_y

    @classmethod
    def piece_to_string(cls, piece):
        if piece:
            return (cls._piece_color_dict[piece.color] +
                    cls._piece_creature_dict[piece.creature] +
                    str(piece.piece_number))

        return "   "

if __name__ == '__main__':
    client = ConsoleClient(GameBoard())
    while True:
        move = client.get_move()
        if not move:
            break
        client.game_board.place(move)
    print("Server Terminated.")
