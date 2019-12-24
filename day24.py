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

def read_eris1(text):
    eris = set()
    for y, line in enumerate(text.splitlines()):
        for x, ch in enumerate(line):
            if ch == '#':
                eris.add((x, y))
    return eris

def adjacent1(x, y):
    yield x - 1, y
    yield x, y - 1
    yield x + 1, y
    yield x, y + 1

def neighbors1(eris, x, y):
    return sum(int(cell in eris) for cell in adjacent1(x, y))

def all_cells1(eris):
    return itertools.product(range(MAXX), range(MAXY))

def next_eris1(e1):
    e2 = set()
    for x, y in all_cells1(e1):
        ncount = neighbors1(e1, x, y)
        if (x, y) in e1:
            alive = ncount == 1
        else:
            alive = ncount in (1, 2)
        if alive:
            e2.add((x, y))
    return e2

def iter_eris1(eris):
    while True:
        yield eris
        eris = next_eris1(eris)


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

def test_next_eris1():
    for before, after in zip(TEST_STATES, TEST_STATES[1:]):
        ebefore = read_eris1(before)
        eafter = read_eris1(after)
        assert next_eris1(ebefore) == eafter

def test_iter_eris1():
    gold = map(read_eris1, TEST_STATES)
    sut = iter_eris1(read_eris1(TEST_STATES[0]))
    assert all(e1 == e2 for e1, e2 in zip(sut, gold))


def first_repeated1(eris):
    eriss = set()
    for estate in iter_eris1(eris):
        etuple = tuple(sorted(estate))
        if etuple in eriss:
            return estate
        eriss.add(etuple)

def biodiversity1(eris):
    biodiv = 0
    for p2, (y, x) in enumerate(all_cells1(eris)):
        if (x, y) in eris:
            biodiv += 2 ** p2
    return biodiv

def test_first_repeated():
    eris = first_repeated1(read_eris1(TEST_STATES[0]))
    assert biodiversity1(eris) == 2129920

if __name__ == "__main__":
    biodiv = biodiversity1(first_repeated1(read_eris1(INPUT)))
    print(f"Part 1: biodiversity of the first repeated state is {biodiv}")

# Part 1 was easy, so Part 2 is a mind-bender :)

def read_eris2(text):
    eris = set()
    for y, line in enumerate(text.splitlines()):
        for x, ch in enumerate(line):
            if ch == '#':
                eris.add((x, y, 0))
    return eris

def adjacent2(x, y, level):
    # Cell to the west
    if x == 0:
        xw = [1]
        yw = [2]
        lw = level - 1
    elif (x, y) == (3, 2):
        xw = [4]
        yw = range(5)
        lw = level + 1
    else:
        xw = [x - 1]
        yw = [y]
        lw = level
    yield from itertools.product(xw, yw, [lw])

    # Cell to the east
    if x == 4:
        xe = [3]
        ye = [2]
        le = level - 1
    elif (x, y) == (1, 2):
        xe = [0]
        ye = range(5)
        le = level + 1
    else:
        xe = [x + 1]
        ye = [y]
        le = level
    yield from itertools.product(xe, ye, [le])

    # Cell to the north
    if y == 0:
        xn = [2]
        yn = [1]
        ln = level - 1
    elif (x, y) == (2, 3):
        xn = range(5)
        yn = [4]
        ln = level + 1
    else:
        xn = [x]
        yn = [y - 1]
        ln = level
    yield from itertools.product(xn, yn, [ln])

    # Cell to the south
    if y == 4:
        xs = [2]
        ys = [3]
        ls = level - 1
    elif (x, y) == (2, 1):
        xs = range(5)
        ys = [0]
        ls = level + 1
    else:
        xs = [x]
        ys = [y + 1]
        ls = level
    yield from itertools.product(xs, ys, [ls])

def all_cells_for_level(level):
    for x, y in itertools.product(range(MAXX), range(MAXY)):
        if (x, y) != (2, 2):
            yield x, y, level

def level_range(eris):
    minl = min(level for x, y, level in eris)
    maxl = max(level for x, y, level in eris)
    return minl, maxl

def neighbors2(eris, cell):
    return sum(int(cell in eris) for cell in adjacent2(*cell))

def all_cells2(eris):
    minl, maxl = level_range(eris)
    for level in range(minl - 1, maxl + 2):
        yield from all_cells_for_level(level)

def next_eris2(e1):
    e2 = set()
    for cell in all_cells2(e1):
        ncount = neighbors2(e1, cell)
        if cell in e1:
            alive = ncount == 1
        else:
            alive = ncount in (1, 2)
        if alive:
            e2.add(cell)
    return e2

def iter_eris2(eris):
    while True:
        yield eris
        eris = next_eris2(eris)

def eris_after2(start, minutes):
    eris = read_eris2(start)
    eris = next(itertools.islice(iter_eris2(eris), minutes, None))
    return eris

def test_eris2():
    assert len(eris_after2(TEST_STATES[0], 10)) == 99

if __name__ == "__main__":
    eris = eris_after2(INPUT, 200)
    print(f"Part 2: after 200 minutes, there are {len(eris)} bugs")

# There's a lot of duplication here.  The two parts could be folded together
# using a generalization of cell structure and adjacency calculation.

# Here we go:

class Eris:
    # Abstract methods that vary by part 1/2

    def read_cell(self, x, y):
        """Produce a cell from position x, y in a text form."""

    def adjacent(self, *cell):
        """Yield all the cells adjacent to this one."""

    def all_cells(self):
        """Yield all the cells in the eris, for polling."""

    # Common code

    def read_eris(self, text):
        eris = set()
        for y, line in enumerate(text.splitlines()):
            for x, ch in enumerate(line):
                if ch == '#':
                    eris.add(self.read_cell(x, y))
        return eris

    def neighbors(self, eris, cell):
        return sum(int(cell in eris) for cell in self.adjacent(*cell))

    def next_eris(self, e1):
        e2 = set()
        for cell in self.all_cells(e1):
            ncount = self.neighbors(e1, cell)
            if cell in e1:
                alive = ncount == 1
            else:
                alive = ncount in (1, 2)
            if alive:
                e2.add(cell)
        return e2

    def iter_eris(self, eris):
        while True:
            yield eris
            eris = self.next_eris(eris)

    def first_repeated(self, eris):
        eriss = set()
        for estate in self.iter_eris(eris):
            etuple = tuple(sorted(estate))
            if etuple in eriss:
                return estate
            eriss.add(etuple)

class Eris1(Eris):
    def read_cell(self, x, y):
        return (x, y)

    def adjacent(self, x, y):
        yield x - 1, y
        yield x, y - 1
        yield x + 1, y
        yield x, y + 1

    def all_cells(self, eris):
        return itertools.product(range(MAXX), range(MAXY))

    def biodiversity(self, eris):
        biodiv = 0
        for p2, (y, x) in enumerate(self.all_cells(eris)):
            if (x, y) in eris:
                biodiv += 2 ** p2
        return biodiv

class Eris2(Eris):
    def read_cell(self, x, y):
        return (x, y, 0)

    def adjacent(self, x, y, level):
        # Cell to the west
        if x == 0:
            xw = [1]
            yw = [2]
            lw = level - 1
        elif (x, y) == (3, 2):
            xw = [4]
            yw = range(5)
            lw = level + 1
        else:
            xw = [x - 1]
            yw = [y]
            lw = level
        yield from itertools.product(xw, yw, [lw])

        # Cell to the east
        if x == 4:
            xe = [3]
            ye = [2]
            le = level - 1
        elif (x, y) == (1, 2):
            xe = [0]
            ye = range(5)
            le = level + 1
        else:
            xe = [x + 1]
            ye = [y]
            le = level
        yield from itertools.product(xe, ye, [le])

        # Cell to the north
        if y == 0:
            xn = [2]
            yn = [1]
            ln = level - 1
        elif (x, y) == (2, 3):
            xn = range(5)
            yn = [4]
            ln = level + 1
        else:
            xn = [x]
            yn = [y - 1]
            ln = level
        yield from itertools.product(xn, yn, [ln])

        # Cell to the south
        if y == 4:
            xs = [2]
            ys = [3]
            ls = level - 1
        elif (x, y) == (2, 1):
            xs = range(5)
            ys = [0]
            ls = level + 1
        else:
            xs = [x]
            ys = [y + 1]
            ls = level
        yield from itertools.product(xs, ys, [ls])

    def all_cells(self, eris):
        minl = min(level for x, y, level in eris)
        maxl = max(level for x, y, level in eris)
        for level in range(minl - 1, maxl + 2):
            for x, y in itertools.product(range(MAXX), range(MAXY)):
                if (x, y) != (2, 2):
                    yield x, y, level


if __name__ == "__main__":
    eris1 = Eris1()
    biodiv = eris1.biodiversity(eris1.first_repeated(eris1.read_eris(INPUT)))
    print(f"Part 1: biodiversity of the first repeated state is {biodiv}")

    eris2 = Eris2()
    eris = eris2.read_eris(INPUT)
    eris = next(itertools.islice(eris2.iter_eris(eris), 200, None))
    print(f"Part 2: after 200 minutes, there are {len(eris)} bugs")
