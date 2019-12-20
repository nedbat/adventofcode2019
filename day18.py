# https://adventofcode.com/2019/day/18

import string

import pytest

from astar import State, search


TESTS = [
"""\
#########
#b.A.@.a#
#########
""",

"""\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""",

"""\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""",

"""\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
""",

"""\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
""",

]

class Vault:
    def __init__(self):
        # Walkable points
        self.cells = {}     # map coords to . or letter
        self.keys = {}      # map letter to coordinates
        self.entrance = None

    @classmethod
    def from_lines(cls, lines):
        vault = cls()
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == '#':
                    continue
                vault.cells[x, y] = ch
                if ch in string.ascii_lowercase:
                    vault.keys[ch] = (x, y)
                if ch == '@':
                    vault.entrance = (x, y)
        return vault

def neighbors(pos):
    x, y = pos
    yield (x - 1, y)
    yield (x, y - 1)
    yield (x + 1, y)
    yield (x, y + 1)

def distance_guess(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


class SearchState(State):
    def __init__(self, vault, keys="", pos=None):
        self.vault = vault
        self.keys = keys
        self.pos = pos or vault.entrance

    def __repr__(self):
        return f"<{self.summary()}>"

    def __hash__(self):
        return hash((self.keys, self.pos))

    def __eq__(self, other):
        return self.keys == other.keys and self.pos == other.pos

    def is_goal(self):
        return len(self.keys) == len(self.vault.keys)

    def next_states(self, cost):
        for npos in neighbors(self.pos):
            nch = self.vault.cells.get(npos)
            if nch is None:
                continue
            if nch in string.ascii_uppercase:
                if nch.lower() not in self.keys:
                    continue
            nkeys = self.keys
            if nch in self.vault.keys and nch not in nkeys:
                nkeys = "".join(sorted(nkeys + nch))
            yield SearchState(self.vault, nkeys, npos), cost + 1

    def guess_completion_cost(self):
        more = []
        num_keys = 0
        for key, kpos in self.vault.keys.items():
            if key not in self.keys:
                more.append(distance_guess(self.pos, kpos))
                num_keys += 1
        return max(more, default=0) + num_keys

    def summary(self):
        return f"At {self.pos}, has {self.keys!r}"


def shortest_path(lines, log=None):
    vault = Vault.from_lines(lines)
    walked = search(SearchState(vault), log=log)
    return walked

@pytest.mark.parametrize("lines, walked", [
    (TESTS[0], 8),
    (TESTS[1], 86),
    (TESTS[2], 132),
    (TESTS[3], 136),
    (TESTS[4], 81),
])
def test_shortest_path(lines, walked):
    assert shortest_path(lines.splitlines()) == walked


if __name__ == "__main__":
    with open("day18_input.txt") as f:
        shortest = shortest_path(f, log=1)
    print(f"Part 1: the shortest path is {shortest}")
