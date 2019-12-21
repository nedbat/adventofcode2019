# https://adventofcode.com/2019/day/21

from intcode import IntCode, program_from_file

class AsciiComputer:
    def __init__(self, program, input):
        self.cpu = IntCode(program, self.input_fn, self.output_fn)
        self.input = []
        self.store_input(input)
    
    def store_input(self, text):
        self.input = list(reversed(text))

    def input_fn(self):
        if not self.input:
            self.store_input(input("") + "\n")
        return ord(self.input.pop())

    def output_fn(self, val):
        if 0 <= val < 128:
            print(chr(val), end='', flush=True)
        else:
            print(f"Numeric output: {val}")

    def run(self):
        self.cpu.run()

def this_computer(input):
    return AsciiComputer(program_from_file("day21_input.txt"), input)

if __name__ == "__main__":
    # Jump if ((not A) and D), or (D and not C)
    this_computer("""\
NOT C J
AND D J
NOT A T
AND D T
OR T J
WALK
""").run()
