# https://adventofcode.com/2019/day/5

from intcode import IntCode, CagedIntCode, program_from_file


def the_program():
    return program_from_file("day05_input.txt")

def part1():
    cpu = IntCode(the_program(), input_fn=lambda: 1)
    cpu.run()

if __name__ == "__main__":
    part1()


def part2():
    cpu = CagedIntCode(the_program(), inputs=[5])
    cpu.run()
    print(f"Part 2: the diagnostic code for system id 5 is {cpu.outputs[0]}")

if __name__ == "__main__":
    part2()
