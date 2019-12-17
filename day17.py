# https://adventofcode.com/2019/day/17

from intcode import IntCode, program_from_file


class Camera:
    def __init__(self, mem0=None, inputs=''):
        self.inputs = iter(inputs)
        program = program_from_file("day17_input.txt")
        if mem0 is not None:
            program[0] = mem0
        self.cpu = IntCode(program, self.input_fn, self.output_fn)
        self.x = self.y = 0
        self.chars = {}
        self.dust = None

    def input_fn(self):
        return ord(next(self.inputs))

    def output_fn(self, val):
        if val > 128:
            self.dust = val
        else:
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

    # Manually determined the instructions to provide.
    cam = Camera(mem0=2, inputs="""\
A,B,A,C,B,C,A,C,B,C
L,8,R,10,L,10
R,10,L,8,L,8,L,10
L,4,L,6,L,8,L,8
n
""")
    cam.cpu.run()
    print(f"Part 2: total dust is {cam.dust}")
