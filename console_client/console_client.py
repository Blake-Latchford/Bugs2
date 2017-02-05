import sys
import asyncio
import piece
import gameboard
import hexcell

import concurrent.futures


class ConsoleClient:

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

    def __init__(self, gameboard, queue=None, loop=None):
        self.gameboard = gameboard

        if queue is None:
            queue = asyncio.Queue()
        self.queue = queue

        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

        self.loop.create_task(self.task_get_move())
        self.loop.create_task(self.consumer())

    async def task_get_move(self):
        while True:
            try:
                print("Select Piece To Move:")
                source_piece_string = await self._get_input()
                source_piece = self._parse_piece(source_piece_string)

                print("Select Destination:")
                relative_location_string = await self._get_input()
                destination = self._parse_relative_location(
                    relative_location_string)

                place_piece_json_object = json_object = \
                    source_piece.to_json_object()
                place_piece_json_object["q"], place_piece_json_object["r"] = \
                    destination
                destination_piece = piece.Piece(place_piece_json_object)

                await self.queue.put(destination_piece)
            except Exception as e:
                print("Invalid move specified:")
                print(e)

    async def _get_input(self):
        thread_executor = concurrent.futures.ThreadPoolExecutor()
        line = await self.loop.run_in_executor(
            thread_executor,
            sys.stdin.readline)
        return line

    def _parse_piece(self, piece_string):
        piece_color = self._piece_color_dict[piece_string[0].lower()]
        piece_type = self._piece_type_dict[piece_string[1].lower()]
        piece_number = int(piece_string[2:])
        return piece.Piece(
            color=piece_color,
            piece_type=piece_type,
            piece_number=piece_number)

    def _parse_relative_location(self, relative_location_string):
        dir_chars = ("-", "/", "\\")
        direction = None
        origin_piece = None

        if relative_location_string.startswith(dir_chars):
            conversion_dict = {
                "/": hexcell.Direction.Q_NEG,
                "-": hexcell.Direction.R_NEG,
                "\\": hexcell.Direction.S_NEG
            }
            direction = conversion_dict[relative_location_string[0]]
            origin_piece = self._parse_piece(relative_location_string[1:])
        elif relative_location_string.endswith(dir_chars):
            conversion_dict = {
                "/": hexcell.Direction.Q_POS,
                "-": hexcell.Direction.R_POS,
                "\\": hexcell.Direction.S_POS
            }
            direction = conversion_dict[relative_location_string[-1]]
            origin_piece = self._parse_piece(relative_location_string[:-1])

        if not direction or not origin_piece:
            raise RuntimeError(
                "Invalid relative destination:" + relative_location_string)

        specified_hexcell = origin_piece.get_neighbor(
            self.gameboard, direction)

        return (specified_hexcell.q, specified_hexcell.r)

if __name__ == '__main__':
    server = ConsoleClient(gameboard.GameBoard())
    asyncio.get_event_loop().run_forever()
    print("Server Terminated.")
