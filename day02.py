# https://adventofcode.com/2019/day/2

import pytest


def next_state(mem, pos):
    op = mem[pos]
    if op in [1, 2]:
        a = mem[mem[pos+1]]
        b = mem[mem[pos+2]]
        if op == 1:
            c = a + b
        elif op == 2:
            c = a * b
        mem2 = list(mem)
        mem2[mem[pos+3]] = c
        return mem2, pos+4
    elif op == 99:
        return mem, None
    else:
        raise Exception(f"Unknown opcode {op}")

def final_state(mem):
    pos = 0
    while True:
        mem, pos = next_state(mem, pos)
        if pos is None:
            return mem

@pytest.mark.parametrize("first, last", [
    ([1,9,10,3,2,3,11,0,99,30,40,50], [3500,9,10,70, 2,3,11,0, 99, 30,40,50]),
    ([1,0,0,0,99], [2,0,0,0,99]),
    ([2,3,0,3,99], [2,3,0,6,99]),
    ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
    ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]),

])
def test_final_state(first, last):
    assert final_state(first) == last


INPUT = [
    1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,13,27,1,10,27,31,2,31,13,35,1,10,35,39,2,9,39,43,2,43,9,47,1,6,47,51,1,10,51,55,2,55,13,59,1,59,10,63,2,63,13,67,2,67,9,71,1,6,71,75,2,75,9,79,1,79,5,83,2,83,13,87,1,9,87,91,1,13,91,95,1,2,95,99,1,99,6,0,99,2,14,0,0
]

def part1():
    mem = list(INPUT)
    mem[1] = 12
    mem[2] = 2
    final = final_state(mem)
    print(f"Part 1: position 0 has {final[0]}")

if __name__ == "__main__":
    part1()
