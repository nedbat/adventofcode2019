# https://adventofcode.com/2019/day/5

from enum import Enum

import pytest


class Op(Enum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
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
            raise Exception(f"Unimplemented mode: {mode.name}")

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
        elif op == Op.JUMP_IF_TRUE:
            val = self.get_parameter_value()
            where = self.get_parameter_value()
            if val != 0:
                self.ip = where
        elif op == Op.JUMP_IF_FALSE:
            val = self.get_parameter_value()
            where = self.get_parameter_value()
            if val == 0:
                self.ip = where
        elif op == Op.EQUALS:
            result = int(self.get_parameter_value() == self.get_parameter_value())
            self.set_at_parameter(result)
        elif op == Op.LESS_THAN:
            result = int(self.get_parameter_value() < self.get_parameter_value())
            self.set_at_parameter(result)
        elif op == Op.STOP:
            return False
        else:
            raise Exception(f"Unimplemented op: {op.name}")
        return True

    def run(self):
        while self.step():
            pass


def final_state(first):
    cpu = IntCode(first)
    cpu.run()
    return cpu.mem

# The tests from day 2.
@pytest.mark.parametrize("first, last", [
    ([1,9,10,3,2,3,11,0,99,30,40,50], [3500,9,10,70, 2,3,11,0, 99, 30,40,50]),
    ([1,0,0,0,99], [2,0,0,0,99]),
    ([2,3,0,3,99], [2,3,0,6,99]),
    ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
    ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]),
])
def test_from_day2(first, last):
    assert final_state(first) == last

@pytest.mark.parametrize("first, last", [
    ([1002,4,3,4,33], [1002, 4, 3, 4, 99]),
])
def test_final_state(first, last):
    assert final_state(first) == last


def the_program():
    with open("day05_input.txt") as f:
        return [int(v) for v in f.read().split(",")]


def part1():
    cpu = IntCode(the_program(), input_fn=lambda: 1)
    cpu.run()

if __name__ == "__main__":
    part1()


class CagedIntCode(IntCode):
    def __init__(self, mem, inputs):
        self.inputs = list(reversed(inputs))
        self.outputs = []
        super().__init__(mem, input_fn=self.inputs.pop, output_fn=self.outputs.append)

def produces(mem, inputs):
    cpu = CagedIntCode(mem, inputs)
    cpu.run()
    return cpu.outputs

@pytest.mark.parametrize("mem, inputs, outputs", [
    # Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
    ([3,9,8,9,10,9,4,9,99,-1,8], [8], [1]),
    ([3,9,8,9,10,9,4,9,99,-1,8], [7], [0]),
    ([3,9,8,9,10,9,4,9,99,-1,8], [77], [0]),
    # Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
    ([3,9,7,9,10,9,4,9,99,-1,8], [7], [1]),
    ([3,9,7,9,10,9,4,9,99,-1,8], [9], [0]),
    # Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
    ([3,3,1108,-1,8,3,4,3,99], [8], [1]),
    ([3,3,1108,-1,8,3,4,3,99], [77], [0]),
    # Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
    ([3,3,1107,-1,8,3,4,3,99], [7], [1]),
    ([3,3,1107,-1,8,3,4,3,99], [9], [0]),
    # output 0 if the input was zero or 1 if the input was non-zero (position mode)
    ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [0], [0]),
    ([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [17], [1]),
    # output 0 if the input was zero or 1 if the input was non-zero (immediate mode)
    ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0], [0]),
    ([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [17], [1]),
    # larger example
    ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [7], [999]),
    ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [8], [1000]),
    ([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [9], [1001]),
])
def test_produces(mem, inputs, outputs):
    assert produces(mem, inputs) == outputs



def part2():
    cpu = CagedIntCode(the_program(), inputs=[5])
    cpu.run()
    print(f"Part 2: the diagnostic code for system id 5 is {cpu.outputs[0]}")

if __name__ == "__main__":
    part2()
