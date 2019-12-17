# https://adventofcode.com/2019/day/17

from intcode import IntCode, program_from_file


class Camera:
    def __init__(self):
        program = program_from_file("day17_input.txt")
        self.cpu = IntCode(program, None, self.output_fn)
        self.x = self.y = 0
        self.chars = {}

    def output_fn(self, val):
        ch = chr(val)
        if ch == '#':
            self.chars[self.x, self.y] = '#'
        if ch == '\n':
            self.x = 0
            self.y += 1
        else:
            self.x += 1
        print(ch, end='')

    def intersections(self):
        for (x, y), ch in self.chars.items():
            if ch == '#':
                if (
                    self.chars.get((x-1, y)) == '#' and
                    self.chars.get((x+1, y)) == '#' and
                    self.chars.get((x, y-1)) == '#' and
                    self.chars.get((x, y+1)) == '#'
                ):
                    yield x, y


if __name__ == "__main__":
    cam = Camera()
    cam.cpu.run()
    all_params = sum(x * y for x, y in cam.intersections())
    print(f"Part 1: the alignment parameters sum to {all_params}")
