# https://adventofcode.com/2019/day/13

import time

import blessings

from intcode import IntCode, program_from_file

class ArcadeCabinet:
    title = "Intcode Arcade Cabinet.  Score: "
    title_y = 1
    start_y = 2
    pause = 0.005

    def __init__(self, mem0=None):
        program = program_from_file("day13_input.txt")
        if mem0 is not None:
            program[0] = mem0
        self.intcode = IntCode(program, self.input_fn, self.output_fn)
        self.outs = []
        self.tiles = {}
        self.term = None
        self.score = 0
        self.ball_x = 0
        self.paddle_x = 0

    def input_fn(self):
        if self.pause:
            time.sleep(self.pause)
        if self.ball_x < self.paddle_x:
            return -1
        elif self.ball_x > self.paddle_x:
            return 1
        else:
            return 0

    def output_fn(self, val):
        self.outs.append(val)
        if len(self.outs) == 3:
            x, y, val = self.outs
            if (x, y) == (-1, 0):
                self.set_score(val)
            else:
                self.draw_tile(x, y, val)
                if val == 3:
                    self.paddle_x = x
                elif val == 4:
                    self.ball_x = x
            self.outs = []

    def set_score(self, score):
        self.score = score
        with self.term.location(len(self.title), self.title_y):
            print(f"{self.score:8d}")

    def draw_tile(self, x, y, tile):
        self.tiles[x, y] = tile
        with self.term.location(x, y + self.start_y):
            print(" |#_o"[tile])

    def num_blocks(self):
        return sum(int(tile == 2) for tile in self.tiles.values())

    def run(self):
        print("\n"*60)
        self.term = blessings.Terminal()
        with self.term.hidden_cursor():
            with self.term.location(0, self.title_y):
                print(self.title)
            while self.intcode.step():
                pass

    
if __name__ == "__main__":
    cab = ArcadeCabinet()
    cab.run()
    part_1 = cab.num_blocks()

    cab = ArcadeCabinet(2)
    cab.run()
    part_2 = cab.score

    print(f"Part 1: there are {part_1} block tiles")
    print(f"Part 2: final score is {part_2}")
