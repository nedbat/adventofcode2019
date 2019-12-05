# https://adventofcode.com/2019/day/5

from enum import Enum

import pytest


class Op(Enum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    STOP = 99

class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1

class IntCode:
    def __init__(self, mem, input_fn=None, output_fn=print):
        self.ip = 0
        self.mem = list(mem)
        self.input_fn = input_fn
        self.output_fn = output_fn

    def next_instruction(self):
        inst = self.mem[self.ip]
        self.ip += 1
        return inst

    def get_parameter_value(self):
        mode = Mode(self.modes % 10)
        self.modes //= 10
        ivalue = self.next_instruction()
        if mode == Mode.POSITION:
            return self.mem[ivalue]
        elif mode == Mode.IMMEDIATE:
            return ivalue
        else:
            raise Exception(f"Unknown mode: {mode}")

    def set_at_parameter(self, value):
        self.mem[self.next_instruction()] = value

    def step(self):
        """Run the next instruction, return True if we should keep going."""
        instruction = self.next_instruction()
        op = Op(instruction % 100)
        self.modes = instruction // 100
        if op == Op.ADD:
            result = self.get_parameter_value() + self.get_parameter_value()
            self.set_at_parameter(result)
        elif op == Op.MUL:
            result = self.get_parameter_value() * self.get_parameter_value()
            self.set_at_parameter(result)
        elif op == Op.INPUT:
            self.set_at_parameter(self.input_fn())
        elif op == Op.OUTPUT:
            self.output_fn(self.get_parameter_value())
        elif op == Op.STOP:
            return False
        else:
            raise Exception(f"Unknown op: {instruction}")
        return True

    def run(self):
        while self.step():
            pass


# The tests from day 2.
@pytest.mark.parametrize("first, last", [
    ([1,9,10,3,2,3,11,0,99,30,40,50], [3500,9,10,70, 2,3,11,0, 99, 30,40,50]),
    ([1,0,0,0,99], [2,0,0,0,99]),
    ([2,3,0,3,99], [2,3,0,6,99]),
    ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
    ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]),
])
def test_from_day2(first, last):
    cpu = IntCode(first)
    cpu.run()
    assert cpu.mem == last

@pytest.mark.parametrize("first, last", [
    ([1002,4,3,4,33], [1002, 4, 3, 4, 99]),
])
def test_final_state(first, last):
    cpu = IntCode(first)
    cpu.run()
    assert cpu.mem == last


def the_program():
    with open("day05_input.txt") as f:
        return [int(v) for v in f.read().split(",")]


def part1():
    cpu = IntCode(the_program(), input_fn=lambda: 1)
    cpu.run()

if __name__ == "__main__":
    part1()
