# https://adventofcode.com/2019/day/9

import pytest

from intcode import produces, program_from_file

if __name__ == "__main__":
    output = produces(program_from_file("day09_input.txt"), [1])
    if len(output) > 1:
        print(f"Incorrect functioning: {output}")
    else:
        print(f"Part 1: the BOOST keycode is {output[0]}")

    output = produces(program_from_file("day09_input.txt"), [2])
    print(f"Part 2: the coordinates of the distress signal are {output[0]}")
