# https://adventofcode.com/2019/day/24

import itertools

INPUT = """\
####.
.###.
.#..#
##.##
###..
"""

MAXX = MAXY = 5

def adjacent(x, y):
    yield x - 1, y
    yield x, y - 1
    yield x + 1, y
    yield x, y + 1

def neighbors(eris, x, y):
    return sum(int((nx, ny) in eris) for nx, ny in adjacent(x, y))

def read_eris(text):
    eris = set()
    for y, line in enumerate(text.splitlines()):
        for x, ch in enumerate(line):
            if ch == '#':
                eris.add((x, y))
    return eris

def next_eris(e1):
    e2 = set()
    for x, y in itertools.product(range(MAXX), range(MAXY)):
        ncount = neighbors(e1, x, y)
        if (x, y) in e1:
            alive = ncount == 1
        else:
            alive = ncount in (1, 2)
        if alive:
            e2.add((x, y))
    return e2

def iter_eris(eris):
    while True:
        yield eris
        eris = next_eris(eris)


TEST_STATES = [
# Initial state:
"""\
....#
#..#.
#..##
..#..
#....
""",

# After 1 minute:
"""\
#..#.
####.
###.#
##.##
.##..
""",

# After 2 minutes:
"""\
#####
....#
....#
...#.
#.###
""",

# After 3 minutes:
"""\
#....
####.
...##
#.##.
.##.#
""",

# After 4 minutes:
"""\
####.
....#
##..#
.....
##...
""",
]

def test_next_eris():
    for before, after in zip(TEST_STATES, TEST_STATES[1:]):
        ebefore = read_eris(before)
        eafter = read_eris(after)
        assert next_eris(ebefore) == eafter

def test_iter_eris():
    gold = map(read_eris, TEST_STATES)
    sut = iter_eris(read_eris(TEST_STATES[0]))
    assert all(e1 == e2 for e1, e2 in zip(sut, gold))


def first_repeated(eris):
    eriss = set()
    for estate in iter_eris(eris):
        etuple = tuple(sorted(estate))
        if etuple in eriss:
            return estate
        eriss.add(etuple)

def biodiversity(eris):
    biodiv = 0
    for p2, (y, x) in enumerate(itertools.product(range(MAXX), range(MAXY))):
        if (x, y) in eris:
            biodiv += 2 ** p2
    return biodiv

def test_first_repeated():
    eris = first_repeated(read_eris(TEST_STATES[0]))
    assert biodiversity(eris) == 2129920

if __name__ == "__main__":
    biodiv = biodiversity(first_repeated(read_eris(INPUT)))
    print(f"Part 1: biodiversity of the first repeated state is {biodiv}")
