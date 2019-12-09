# https://adventofcode.com/2019/day/7

import itertools

import pytest

from intcode import CagedIntCode, IntCode, program_from_file

class OneOutputIntCode(CagedIntCode):
    def run_to_output(self):
        while not self.outputs and self.step():
            pass
        return self.outputs[0]


# The tests from day 5
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
def test_one_output(mem, inputs, outputs):
    cpu = OneOutputIntCode(mem, inputs)
    assert cpu.run_to_output() == outputs[0]


def run_amplifiers(mem, phase_settings):
    signal = 0
    for phase_setting in phase_settings:
        cpu = OneOutputIntCode(mem, [phase_setting, signal])
        signal = cpu.run_to_output()
    return signal

def max_thruster(mem):
    """Returns the thruster value and the settings that produced it."""
    return max(
        (run_amplifiers(mem, settings), settings)
        for settings in itertools.permutations(range(5))
    )

@pytest.mark.parametrize("mem, output, settings", [
    ([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], 43210, (4,3,2,1,0)),
    ([3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0], 54321, (0,1,2,3,4)),
    ([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], 65210, (1,0,4,3,2)),
])
def test_max_thruster(mem, output, settings):
    thruster, tsettings = max_thruster(mem)
    assert thruster == output
    assert tsettings == settings

def the_program():
    return program_from_file("day07_input.txt")


def part1():
    thruster, settings = max_thruster(the_program())
    print(f"Part 1: the max thruster signal is {thruster}")

if __name__ == "__main__":
    part1()


class NeedInput(Exception):
    pass

class ChainableIntCode(IntCode):
    def __init__(self, mem, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        super().__init__(mem, input_fn=self.feed_input, output_fn=self.outputs.append)

    def feed_input(self):
        if self.inputs:
            return self.inputs.pop(0)
        else:
            self.ip -= 1
            raise NeedInput()

    def run_until_blocked(self):
        while True:
            try:
                if not self.step():
                    return False
            except NeedInput:
                return True

def cycle_pairs(seq):
    return zip(seq, seq[1:] + seq[:1])

def test_cycle_pairs():
    assert list(cycle_pairs([1,2,3,4])) == [(1,2), (2,3), (3,4), (4,1)]

def run_looped_amplifiers(mem, phase_settings):
    signal_buffers = [[setting] for setting in phase_settings]
    signal_buffers[0].append(0)

    cpus = [ChainableIntCode(mem, ins, outs) for ins, outs in cycle_pairs(signal_buffers)]
    while True:
        any_halted = False
        for cpu in cpus:
            if not cpu.run_until_blocked():
                any_halted = True
        if any_halted:
            return signal_buffers[0][-1]

def looped_thruster_values(mem):
    for settings in itertools.permutations(range(5, 10)):
        yield run_looped_amplifiers(mem, settings), settings

def max_looped_thruster(mem):
    return max(looped_thruster_values(mem))

@pytest.mark.parametrize("mem, output, settings", [
    ([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], 139629729, (9,8,7,6,5)),
    ([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], 18216, (9,7,8,5,6)),
])
def test_max_looped_thruster(mem, output, settings):
    thruster, tsettings = max_looped_thruster(mem)
    assert thruster == output
    assert tsettings == settings

def part2():
    thruster, settings = max_looped_thruster(the_program())
    print(f"Part 2: the max thruster signal is {thruster}")
    
if __name__ == "__main__":
    part2()
