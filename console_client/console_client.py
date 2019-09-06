import collections
import rules.piece as piece
import rules.gameboard as gameboard


class ConsoleClient:

    # TODO these are needed to print the board.
    _piece_color_dict = {
        "w": piece.Color.WHITE,
        "b": piece.Color.BLACK
    }

    _piece_type_dict = {
        "B": piece.PieceType.BEE,
        "s": piece.PieceType.SPIDER,
        "b": piece.PieceType.BEETLE,
        "g": piece.PieceType.GRASSHOPPER,
        "a": piece.PieceType.ANT
    }

    def __init__(self, gameboard):
        self.gameboard = gameboard

    def get_move(self):
        piece_moves = collections.OrderedDict(self.gameboard.get_moves())

        if not piece_moves:
            return None

        while True:
            for i, source_piece in enumerate(piece_moves.keys()):
                print(str(i) + ") " + str(source_piece))

            source_piece_index = int(input("Select source piece number:"))
            source_piece, valid_moves = \
                list(piece_moves.items())[source_piece_index]
            valid_moves = list(valid_moves)

            if len(valid_moves) > 1:
                for i, move in enumerate(valid_moves):
                    print(str(i) + ") " + str(move))
                dest_index = int(input("Select destination number:"))
            else:
                dest_index = 0
            dest = valid_moves[dest_index]

            return piece.Piece(
                piece_type=source_piece.piece_type,
                color=source_piece.color,
                piece_number=source_piece.piece_number,
                q=dest.q,
                r=dest.r)

if __name__ == '__main__':
    client = ConsoleClient(gameboard.GameBoard())
    while client.move():
        pass
    print("Server Terminated.")
