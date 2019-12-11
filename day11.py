# https://adventofcode.com/2019/day/11

import itertools

import attr

from intcode import IntCode, program_from_file

@attr.s(auto_attribs=True)
class Direction:
    dx: int = 1
    dy: int = 0

    def left(self):
        return self.__class__(self.dy, -self.dx)

    def right(self):
        return self.__class__(-self.dy, self.dx)

@attr.s(auto_attribs=True)
class Point:
    x: int = 0
    y: int = 0

    def move(self, direction):
        return self.__class__(self.x + direction.dx, self.y + direction.dy)

    def tuple(self):
        return self.x, self.y

class Hull:
    def __init__(self):
        self.panels = {}
    
    def __getitem__(self, coords):
        return self.panels.get(coords, 0)

    def __setitem__(self, coords, val):
        self.panels[coords] = val


class Robot:
    def __init__(self, program, hull):
        self.intcode = IntCode(program, self.input_fn, self.output_fn)
        self.hull = hull
        self.pos = Point(0, 0)
        self.dir = Direction(0, -1)
        self.actions = itertools.cycle([self.paint, self.move])

    def input_fn(self):
        return self.hull[self.pos.tuple()]

    def output_fn(self, val):
        next(self.actions)(val)

    def paint(self, val):
        self.hull[self.pos.tuple()] = val

    def move(self, val):
        if val == 0:
            self.dir = self.dir.left()
        else:
            self.dir = self.dir.right()
        self.pos = self.pos.move(self.dir)

    def run(self):
        self.intcode.run()


def part1():
    the_program = program_from_file("day11_input.txt")
    hull = Hull()
    robot = Robot(the_program, hull)
    robot.run()
    print(f"Part 1: {len(hull.panels)} were painted")

if __name__ == "__main__":
    part1()
