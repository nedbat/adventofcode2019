# https://adventofcode.com/2019/day/19

import itertools
import sys

import pytest

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


def binary_search_last_true(lo, hi, fn):
    """Perform a binary search.

    Returns the value lo <= x <= hi where fn(x) is True and fn(x+1) is False.
    """
    assert fn(lo)
    assert not fn(hi)
    
    while hi - lo > 1:
        mid = (lo + hi) // 2
        mid_true = fn(mid)
        if mid_true:
            lo = mid
        else:
            hi = mid
    return lo

def binary_search_first_true(lo, hi, fn):
    """
    Return x such that lo <= x <= hi, and fn(x-1) is False and fn(x) is True.
    """
    return binary_search_last_true(lo, hi, lambda x: not fn(x)) + 1

@pytest.mark.parametrize("lo, hi, result", [
    (1, 10, 2),
    (1, 10, 9),
    (1, 10, 5),
])
def test_binary_search(lo, hi, result):
    assert binary_search_last_true(lo, hi, lambda x: x <= result) == result
    

MAX = 10000

def find_beam_start_in_row(rownum):
    for x in range(MAX):
        if probe(x, rownum):
            return x

def square_fits(x, y, sqsize):
    """Does a square of size sqsize fit with its lower-left at x, y?"""
    return probe(x, y) and probe(x + sqsize - 1, y - sqsize + 1)

def square_fits_on_row(rownum, sqsize):
    # Find the first on cell in this row
    first_on = find_beam_start_in_row(rownum)
    # Does the square fit here?
    return square_fits(first_on, rownum, sqsize)

def find_fit(sqsize):
    # binary search for a row where the square fits
    row = binary_search_first_true(sqsize, MAX, lambda val: square_fits_on_row(val, sqsize))
    return row

if __name__ == '__main__':
    row = find_fit(100)
    firstx = find_beam_start_in_row(row)
    answer = firstx * 10000 + (row - 99)
    print(f"Part 2: answer is {answer}")
