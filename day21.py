# https://adventofcode.com/2019/day/21

from intcode import IntCode, program_from_file

class AsciiComputer:
    def __init__(self, program, label, input):
        self.cpu = IntCode(program, self.input_fn, self.output_fn)
        self.label = label
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
            print(f"{self.label}: hull damage is: {val}")

    def run(self):
        print(f"--- {self.label} ---------")
        self.cpu.run()

def this_computer(label, input):
    return AsciiComputer(program_from_file("day21_input.txt"), label, input)

if __name__ == "__main__":
    # Jump if ((not A) and D), or (D and not C)
    this_computer("Part 1", """\
NOT C J
AND D J
NOT A T
AND D T
OR T J
WALK
""").run()

    seen_patterns = [
        "##=##.=..#=###=##",
        "=###=.#.=..#=.##=",
        "##=##.=.#.=#..=##",
        #   ABCDEFGHI
    ]
    this_computer("Part 2", 
# Jump if (D) and (E or H) and not (A and B and C and D)
"""\
OR H J
OR E J
AND D J
OR A T
AND B T
AND C T
AND D T
NOT T T
AND T J
RUN
"""
).run()
