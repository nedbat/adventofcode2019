# https://adventofcode.com/2019/day/22

import re

import pytest

# Part 1: actually perform the operations. Very unlikely this will work for
# part 2... :)

def make_program(shuffle_process):
    code = []
    code.append("def doit(*args):")
    for line in shuffle_process.splitlines():
        line = line.strip()
        if not line:
            continue
        op, amt = re.search(r"^(.*[a-z]) ?(-?\d*)$", line).groups()
        op = op.replace(" ", "_")
        amt = int(amt or "0")
        code.append(f"  args = {op}({amt}, *args)")
    code.append("  return args")
    return "\n".join(code) + "\n"

def deal_into_new_stack(_, deck):
    return (deck[::-1],)

def cut(amt, deck):
    return ((deck[amt:] + deck[:amt]),)

def deal_with_increment(amt, deck):
    new_deck = [None] * len(deck)
    new_i = 0
    for card in deck:
        new_deck[new_i] = card
        new_i += amt
        new_i %= len(deck)
    return (new_deck,)

def run_process(process, *args):
    prog = make_program(process)
    globs = {
        'deal_into_new_stack': deal_into_new_stack,
        'cut': cut,
        'deal_with_increment': deal_with_increment,
    }
    exec(prog, globs, globs)
    args = globs['doit'](*args)
    return args

TEST_DATA = [
    ("deal into new stack\n", [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]),
    ("cut 3\n", [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]),
    ("cut -4\n", [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]),
    ("deal with increment 3\n", [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]),
    ("""\
        deal with increment 7
        deal into new stack
        deal into new stack
        """,
        [0, 3, 6, 9, 2, 5, 8, 1, 4, 7],
    ),
    ("""\
        cut 6
        deal with increment 7
        deal into new stack
        """,
        [3, 0, 7, 4, 1, 8, 5, 2, 9, 6],
    ),
    ("""\
        deal with increment 7
        deal with increment 9
        cut -2
        """,
        [6, 3, 0, 7, 4, 1, 8, 5, 2, 9],
    ),
    ("""\
        deal into new stack
        cut -2
        deal with increment 7
        cut 8
        cut -4
        deal with increment 7
        cut 3
        deal with increment 9
        deal with increment 3
        cut -1
        """,
        [9, 2, 5, 8, 1, 4, 7, 0, 3, 6],
    ),
]

@pytest.mark.parametrize("process, result", TEST_DATA)
def test_run_process(process, result):
    assert run_process(process, list(range(10))) == (result,)

if __name__ == "__main__":
    deck = list(range(10007))
    with open("day22_input.txt") as f:
        process = f.read()
    (deck,) = run_process(process, deck)
    i2019 = deck.index(2019)
    print(f"Part 1: 2019 is at {i2019}")

# Part 2: closed-form tracking of where a card ends up.


