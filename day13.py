# https://adventofcode.com/2019/day/13

from intcode import IntCode, program_from_file

class ArcadeCabinet:
    def __init__(self):
        program = program_from_file("day13_input.txt")
        self.intcode = IntCode(program, self.input_fn, self.output_fn)
        self.outs = []
        self.tiles = {}

    def input_fn(self):
        raise Exception("Don't know what input to provide!")

    def output_fn(self, val):
        self.outs.append(val)
        if len(self.outs) == 3:
            self.draw_tile(*self.outs)
            self.outs = []

    def draw_tile(self, x, y, tile):
        self.tiles[x, y] = tile

    def run(self):
        self.intcode.run()


if __name__ == "__main__":
    cab = ArcadeCabinet()
    cab.run()
    num_blocks = sum(int(tile == 2) for tile in cab.tiles.values())
    print(f"Part 1: there are {num_blocks} block tiles")
