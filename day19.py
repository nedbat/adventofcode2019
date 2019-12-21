# https://adventofcode.com/2019/day/19

import itertools

from intcode import IntCode, program_from_file

class BeamScan:
    program = program_from_file("day19_input.txt")

    def __init__(self, x, y):
        self.inputs = iter([x, y])
        self.cpu = IntCode(self.program, lambda: next(self.inputs), self.output_fn)
        self.affected = 0

    def output_fn(self, val):
        self.affected = val

def probe(x, y):
    scanner = BeamScan(x, y)
    scanner.cpu.run()
    return scanner.affected

def scan(ux, uy):
    points = 0
    for y, x in itertools.product(range(uy), range(ux)):
        yes = probe(x, y)
        print(".#"[yes], end=('\n' if x == ux-1 else ''))
        points += yes
    return points

if __name__ == '__main__':
    print(f"Part 1: {scan(50, 50)} are affected")
