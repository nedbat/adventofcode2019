# https://adventofcode.com/2019/day/15

import random
import time

import attr
import blessings

from intcode import IntCode, program_from_file

@attr.s(auto_attribs=True, frozen=True)
class Direction:
    dx: int = 1
    dy: int = 0

    def left(self):
        return self.__class__(self.dy, -self.dx)

    def right(self):
        return self.__class__(-self.dy, self.dx)
    
    def back(self):
        return self.__class__(-self.dx, -self.dy)

@attr.s(auto_attribs=True)
class Point:
    x: int = 0
    y: int = 0

    def move(self, direction):
        return self.__class__(self.x + direction.dx, self.y + direction.dy)

    def tuple(self):
        return self.x, self.y

MOVEMENT = {
    Direction(0, -1): 1,
    Direction(0, 1): 2,
    Direction(-1, 0): 3,
    Direction(1, 0): 4,
}

term = blessings.Terminal()

class Field:
    def __init__(self):
        self.cells = {}
    
    def __getitem__(self, coords):
        return self.cells.get(coords, 0)

    def __setitem__(self, coords, val):
        self.cells[coords] = val

    def draw(self, cell_chars='.#', draw_fn=None):
        if draw_fn is None:
            draw_fn = lambda: None
        lx = min(x for x, y in self.cells)
        ux = max(x for x, y in self.cells)
        ly = min(y for x, y in self.cells)
        uy = max(y for x, y in self.cells)

        print(term.clear())
        print(term.move(0, 0))
        for y in range(ly, uy + 1):
            for x in range(lx, ux + 1):
                ch = draw_fn(x, y) or cell_chars[self[x, y]]
                print(ch, end='')
            print()

class Robot:
    def __init__(self):
        program = program_from_file("day15_input.txt")
        self.cpu = IntCode(program, self.input_fn, self.output_fn)
        self.oxygen_pos = None
        self.pos = Point(0, 0)
        self.dir = Direction(0, -1)
        self.tank = Field()
        self.tank[0, 0] = 0
        self.moves = []
        self.moves_to_point = {(0, 0): []}

    def input_fn(self):
        # Not smart, but it gets the job done.
        self.dir = random.choice(list(MOVEMENT))
        cmd = MOVEMENT[self.dir]
        return cmd

    def output_fn(self, val):
        if val == 0:
            # Hit a wall
            self.tank[self.pos.move(self.dir).tuple()] = 1
        else:
            # Moved one step
            new_pos = self.pos.move(self.dir)
            if new_pos.tuple() not in self.moves_to_point:
                moves = list(self.moves_to_point[self.pos.tuple()]) + [self.dir]
                self.moves_to_point[new_pos.tuple()] = moves
            self.pos = new_pos
            self.tank[self.pos.tuple()] = 0
            if val == 2:
                # and this is the goal
                self.oxygen_pos = self.pos
        # print("-" * 80)
        # self.draw()
        # time.sleep(.001)

    def draw_fn(self, x, y):
        if self.oxygen_pos is not None and (x, y) == self.oxygen_pos.tuple():
            return '@'
        if (x, y) == self.pos.tuple():
            return 'D'
        if (x, y) == (0, 0):
            return 'o'
        if (x, y) in self.moves_to_point:
            return '.'

    def draw(self):
        self.tank.draw(' #', self.draw_fn)

    def run(self):
        with term.fullscreen():
            with term.hidden_cursor():
                while self.oxygen_pos is None and self.cpu.step():
                    pass

if __name__ == "__main__":
    robot = Robot()
    robot.run()
    robot.draw()
    num_moves = len(robot.moves_to_point[robot.oxygen_pos.tuple()])
    print(f"Part 1: it takes {num_moves} to get to the oxygen")
