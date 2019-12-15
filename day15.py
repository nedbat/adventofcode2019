# https://adventofcode.com/2019/day/15

import time

import attr
import blessings
import pytest

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

@attr.s(auto_attribs=True, frozen=True)
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

DIRNAMES = {
    Direction(0, -1): 'N',
    Direction(0, 1): 'S',
    Direction(-1, 0): 'W',
    Direction(1, 0): 'E',
}

def move_string(moves):
    return ''.join(DIRNAMES[m] for m in moves)

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
        print("-" * 60)

def common_head_len(seq1, seq2):
    """How long is the common head of seq1 and seq2?"""
    i = -1
    for i, (e1, e2) in enumerate(zip(seq1, seq2)):
        if e1 != e2:
            return i
    return i + 1

@pytest.mark.parametrize("seq1, seq2, head_len", [
    ("", "", 0),
    ("ABC", "ABC", 3),
    ("ABC", "ABCDEF", 3),
    ("ABC", "ABD", 2),
])
def test_common_head_len(seq1, seq2, head_len):
    assert common_head_len(seq1, seq2) == head_len


class Done(Exception):
    pass

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
        self.moves_to_point = {Point(0, 0): []}
        self.points_to_explore = [Point(0, 0)]
        self.state = 'pick_a_point'
        self.blind_moves = []
        self.explore_moves = []
        self.explore_back = None

    def input_fn(self):
        #print(f"input with state {self.state}")
        self.dir = getattr(self, self.state + '_input')()
        #print(f"moving {self.dir}")
        return MOVEMENT[self.dir]

    def output_fn(self, val):
        if val == 0:
            next_pos = self.pos
        else:
            next_pos = self.pos.move(self.dir)
        #print(f"output with state {self.state}, pos = {self.pos}, next_pos = {next_pos}")
        getattr(self, self.state + '_output')(val, next_pos)
        self.pos = next_pos
        print("-" * 80)
        self.draw()
        time.sleep(.001)

    def pick_a_point_input(self):
        #print(f"picking point")
        if not self.points_to_explore:
            raise Done()
        pt = self.points_to_explore.pop()
        moves = self.moves_from_to(self.pos, pt)
        if moves:
            self.blind_move(moves)
            return self.blind_move_input()
        else:
            self.explore()
            return self.explore_input()

    def moves_from_to(self, pt1, pt2):
        """Return the moves to get from self.pos to pt."""
        to_here = self.moves_to_point[pt1]
        to_there = self.moves_to_point[pt2]
        common_len = common_head_len(to_here, to_there)
        backup = list(reversed([d.back() for d in to_here[common_len:]]))
        return backup + to_there[common_len:]

    def blind_move(self, moves):
        self.blind_moves = list(reversed(moves))
        self.state = 'blind_move'

    def blind_move_input(self):
        #print(f"blind moving with moves {move_string(self.blind_moves)}")
        return self.blind_moves.pop()

    def blind_move_output(self, val, next_pos):
        assert val != 0
        if not self.blind_moves:
            self.explore()

    def explore(self):
        self.explore_moves = list(MOVEMENT)
        self.state = 'explore'

    def explore_input(self):
        #print(f"exploring with moves {move_string(self.explore_moves)}")
        if self.explore_moves:
            return self.explore_moves.pop()
        else:
            state = 'pick_a_point'
            return self.pick_a_point_input()

    def explore_output(self, val, next_pos):
        if val == 0:
            # Hit a wall
            self.tank[self.pos.move(self.dir).tuple()] = 1
        else:
            # Moved one step
            if next_pos not in self.moves_to_point:
                moves = list(self.moves_to_point[self.pos]) + [self.dir]
                self.moves_to_point[next_pos] = moves
                self.points_to_explore.append(next_pos)
                self.tank[next_pos.tuple()] = 0
                if val == 2:
                    # this is the goal
                    self.oxygen_pos = next_pos
            self.explore_undo(self.dir)

    def explore_undo(self, dir):
        self.explore_back = dir.back()
        self.state = 'explore_undo'

    def explore_undo_input(self):
        #print(f"undoing explore")
        return self.explore_back

    def explore_undo_output(self, val, next_pos):
        assert val != 0
        self.state = 'explore'

    def draw_fn(self, x, y):
        if self.oxygen_pos is not None and (x, y) == self.oxygen_pos.tuple():
            return '@'
        if (x, y) == self.pos.tuple():
            return 'D'
        if (x, y) == (0, 0):
            return 'o'
        if Point(x, y) in self.points_to_explore:
            return '?'
        if Point(x, y) in self.moves_to_point:
            return '·'

    def draw(self):
        self.tank.draw(' █', self.draw_fn)

    def run(self):
        with term.fullscreen():
            with term.hidden_cursor():
                try:
                    self.cpu.run()
                except Done:
                    pass

if __name__ == "__main__":
    robot = Robot()
    robot.run()
    robot.draw()
    num_moves = len(robot.moves_to_point[robot.oxygen_pos])
    print(f"Part 1: it takes {num_moves} steps to get to the oxygen")

    farthest = max(len(robot.moves_from_to(robot.oxygen_pos, pt)) for pt in robot.moves_to_point)
    print(f"Part 2: it will take {farthest} minutes to fill with oxygen")
