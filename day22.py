# https://adventofcode.com/2019/day/22

import re

import pytest

# Part 1: actually perform the operations. Very unlikely this will work for
# part 2... :)

def make_program(shuffle_process, reverse=False):
    code = []
    code.append("def doit(fixed, arg):")
    lines = shuffle_process.splitlines()
    if reverse:
        lines = lines[::-1]
    for line in lines:
        line = line.strip()
        if not line:
            continue
        op, amt = re.search(r"^(.*[a-z]) ?(-?\d*)$", line).groups()
        op = op.replace(" ", "_")
        amt = int(amt or "0")
        code.append(f"  arg = {op}({amt}, fixed, arg)")
    code.append("  return arg")
    return "\n".join(code) + "\n"

def deal_into_new_stack(_, __, deck):
    return deck[::-1]

def cut(amt, _, deck):
    return deck[amt:] + deck[:amt]

def deal_with_increment(amt, _, deck):
    new_deck = [None] * len(deck)
    new_i = 0
    for card in deck:
        new_deck[new_i] = card
        new_i += amt
        new_i %= len(deck)
    return new_deck

def run_process(process, fixed, arg):
    prog = make_program(process)
    globs = {
        'deal_into_new_stack': deal_into_new_stack,
        'cut': cut,
        'deal_with_increment': deal_with_increment,
    }
    exec(prog, globs, globs)
    arg = globs['doit'](fixed, arg)
    return arg

TEST_DATA = [
    ("deal into new stack\n", [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]),
    ("cut 3\n", [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]),
    ("cut -2\n", [8, 9, 0, 1, 2, 3, 4, 5, 6, 7]),
    ("cut -4\n", [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]),
    ("deal with increment 3\n", [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]),
    ("deal with increment 7\n", [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]),
    ("deal with increment 9\n", [0, 9, 8, 7, 6, 5, 4, 3, 2, 1]),
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
    assert run_process(process, None, list(range(10))) == result

if __name__ == "__main__":
    deck = list(range(10007))
    with open("day22_input.txt") as f:
        process = f.read()
    deck = run_process(process, None, deck)
    i2019 = deck.index(2019)
    print(f"Part 1: 2019 is at {i2019}")


# Part 2: closed-form tracking of what card is at a particular index.

def deal_into_new_stack2(_, deck_len, index):
    return deck_len - 1 - index

def cut2(amt, deck_len, index):
    return (index + amt) % deck_len

def modular_inverse(a, m):
    m0 = m
    y = 0
    x = 1

    if m == 1:
        return 0

    while a > 1:
        # q is quotient
        q = a // m

        t = m

        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y

        # Update x and y
        y = x - q * y
        x = t

    # Make x positive
    if x < 0:
        x += m0

    return x

def deal_with_increment2(amt, deck_len, index):
    return modular_inverse(amt, deck_len) * index % deck_len

def run_process2(process, fixed, arg):
    prog = make_program(process, reverse=True)
    globs = {
        'deal_into_new_stack': deal_into_new_stack2,
        'cut': cut2,
        'deal_with_increment': deal_with_increment2,
    }
    exec(prog, globs, globs)
    arg = globs['doit'](fixed, arg)
    return arg

@pytest.mark.parametrize("process, result", TEST_DATA)
def test_run_process2(process, result):
    for index in range(10):
        assert run_process2(process, 10, index) == result[index]

def part2(process, deck_size, iterations, index):
    seen = set()
    while True:
        next = run_process2(process, deck_size, index)
        delta = index - next
        index = next
        if delta < 0:
            delta += deck_size
        if delta in seen:
            print(len(seen))
            break
        seen.add(delta)
        if len(seen) % 10000 == 0:
            print(len(seen))
    return (index + (orig - index) * iterations) % deck_size

if __name__ == "__main__":
    with open("day22_input.txt") as f:
        process = f.read()
    answer = part2(process, 119_315717_514047, 101_741582_076661, 2020)
    print(f"Part 2: card {answer} is at position 2020")
