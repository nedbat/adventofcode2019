# https://adventofcode.com/2019/day/18

import string
import sys
import textwrap

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

class Node:
    def __init__(self):
        # The letter of this node's key, if any.
        self.key = None
        # The letter of this node's door (lower-cased) if any.
        self.door = None
        # Is this an entrance?
        self.entrance = False
        # Edges away from the node: a dict with other-node coords as keys, and
        # length of edge as value.
        self.edges = {}

class Vault:
    def __init__(self):
        # Walkable points
        self.cells = {}     # map coords to . or letter
        self.keys = {}      # map letter to coordinates
        self.entrances = []
        self.graph = None

    @classmethod
    def from_lines(cls, lines):
        vault = cls()
        for y, line in enumerate(lines):
            for x, ch in enumerate(line.strip()):
                if ch == '#':
                    continue
                vault.cells[x, y] = ch
                if ch in string.ascii_lowercase:
                    vault.keys[ch] = (x, y)
                if ch == '@':
                    vault.entrances.append((x, y))
        vault.graph = graph_for_vault(vault)
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

def graph_for_vault(vault):
    graph = {}

    # Make nodes for every walkable cell in the vault.
    for pos, ch in vault.cells.items():
        graph[pos] = node = Node()
        if ch in string.ascii_lowercase:
            node.key = ch
        elif ch in string.ascii_uppercase:
            node.door = ch.lower()

    # Entrances are special
    for ex, ey in vault.entrances:
        graph[ex, ey].entrance = True

    # Now connect up the nodes by edges.
    for pos in vault.cells:
        node = graph[pos]
        for npos in neighbors(pos):
            nch = vault.cells.get(npos)
            if nch is not None:
                node.edges[npos] = 1

    # Reduce the graph by removing dead-ends and uninteresting 
    # nodes connecting only two other nodes.
    while True:
        prev_nodes = len(graph)
        for pos, node in list(graph.items()):
            if node.key or node.door or node.entrance:
                # Never remove a special node.
                continue
            if len(node.edges) == 1:
                # A dead end, drop it
                opos, _ = node.edges.popitem()
                del graph[opos].edges[pos]
                del graph[pos]
            elif len(node.edges) == 2:
                (opos1, len1), (opos2, len2) = node.edges.items()
                node1 = graph[opos1]
                assert node1.edges[pos] == len1
                del node1.edges[pos]
                node1.edges[opos2] = len1 + len2
                node2 = graph[opos2]
                assert node2.edges[pos] == len2
                del node2.edges[pos]
                node2.edges[opos1] = len1 + len2
                del graph[pos]
        if len(graph) == prev_nodes:
            # Nothing changed, we're done.
            break

    return graph

def print_vault(vault):
    minx = min(x for x, y in vault.cells)
    maxx = max(x for x, y in vault.cells)
    miny = min(y for x, y in vault.cells)
    maxy = max(y for x, y in vault.cells)
    for y in range(miny - 1, maxy + 2):
        for x in range(minx - 1, maxx + 2):
            ch = vault.cells.get((x, y), '#')
            if ch == '.':
                ch = '.' if (x, y) in vault.graph else ' '
            node = vault.graph.get((x, y))
            if node and node.entrance:
                ch = '@'
            print(ch, end="")
        print()

class SearchState(State):
    def __init__(self, vault, keys="", pos=None):
        self.vault = vault
        self.keys = keys
        self.pos = pos or vault.entrances[0]

    def __repr__(self):
        return f"<{self.summary()}>"

    def __hash__(self):
        return hash((self.keys, self.pos))

    def __eq__(self, other):
        return self.keys == other.keys and self.pos == other.pos

    def is_goal(self):
        return len(self.keys) == len(self.vault.keys)

    def next_states(self, cost):
        for npos, edgelen in self.vault.graph[self.pos].edges.items():
            nbor = self.vault.graph[npos]
            if nbor.door:
                if nbor.door not in self.keys:
                    continue
            nkeys = self.keys
            if nbor.key and nbor.key not in nkeys:
                nkeys = "".join(sorted(nkeys + nbor.key))
            yield SearchState(self.vault, nkeys, npos), cost + edgelen

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


if __name__ == "__main__" and "1" in sys.argv:
    with open("day18_input.txt") as f:
        shortest = shortest_path(f)
    print(f"Part 1: the shortest path is {shortest}")


class MultiVault(Vault):
    @classmethod
    def from_lines(cls, lines):
        vault = super().from_lines(lines)
        vault.create_entrances()
        return vault

    def create_entrances(self):
        ex, ey = self.entrances[0]
        del self.cells[ex, ey]
        del self.cells[ex - 1, ey]
        del self.cells[ex, ey - 1]
        del self.cells[ex + 1, ey]
        del self.cells[ex, ey + 1]
        self.entrances = (
            (ex - 1, ey - 1),
            (ex + 1, ey - 1),
            (ex - 1, ey + 1),
            (ex + 1, ey + 1),
        )


class MultiSearchState(State):
    def __init__(self, vault, keys="", poss=None):
        self.vault = vault
        self.keys = keys
        self.poss = poss or vault.entrances

    def __repr__(self):
        return f"<{self.summary()}>"

    def __hash__(self):
        return hash((self.keys, self.poss))

    def __eq__(self, other):
        return self.keys == other.keys and self.poss == other.poss

    def is_goal(self):
        return len(self.keys) == len(self.vault.keys)

    def next_states(self, cost):
        for ipos, pos in enumerate(self.poss):
            for npos, edgelen in self.vault.graph[pos].edges.items():
                nbor = self.vault.graph[npos]
                if nbor.door:
                    if nbor.door not in self.keys:
                        continue
                nkeys = self.keys
                if nbor.key and nbor.key not in nkeys:
                    nkeys = "".join(sorted(nkeys + nbor.key))
                nposs = tuple(npos if ii == ipos else pos for ii, pos in enumerate(self.poss))
                yield MultiSearchState(self.vault, nkeys, nposs), cost + edgelen

    def same_quadrant(self, pos1, pos2):
        """Are pos1 and pos2 in the same quadrant?"""
        x1, y1 = pos1
        x2, y2 = pos2
        xe, ye = self.vault.entrances[0]
        return (
            (x1 <= xe) == (x2 <= xe) and
            (y1 <= ye) == (y2 <= ye)
        )

    def guess_completion_cost(self):
        mores = [[] for _ in self.poss]
        num_keys = 0
        for key, kpos in self.vault.keys.items():
            #print(f"Considering key {key!r} at {kpos}")
            if key not in self.keys:
                # Find the robot in the same quadrant as this key.
                for pos, more in zip(self.poss, mores):
                    if self.same_quadrant(pos, kpos):
                        #print(f"Robot {pos} can get it in {distance_guess(pos, kpos)} steps")
                        more.append(distance_guess(pos, kpos))
                num_keys += 1
        #print(f"mores = {mores}")
        guess = sum(max(more, default=0) for more in mores) + num_keys
        #print(f"guess = {guess}")
        return guess

    def summary(self):
        return f"At {self.poss}, has {self.keys!r}"


def test_multi():
    vault = MultiVault.from_lines(textwrap.dedent("""\
        #######
        #a.#Cd#
        ##...##
        ##.@.##
        ##...##
        #cB#Ab#
        #######
        """).splitlines())
    walked = search(MultiSearchState(vault), log=1)
    assert walked == 8

def test_multi2():
    vault = MultiVault.from_lines(textwrap.dedent("""\
        #############
        #g#f.D#..h#l#
        #F###e#E###.#
        #dCba...BcIJ#
        #####.@.#####
        #nK.L...G...#
        #M###N#H###.#
        #o#m..#i#jk.#
        #############
        """).splitlines())
    walked = search(MultiSearchState(vault), log=1)
    assert walked == 72


if __name__ == "__main__" and "2" in sys.argv:
    with open("day18_input.txt") as f:
        vault = MultiVault.from_lines(f)
    walked = search(MultiSearchState(vault), log=10)
    print(f"Part 2: the shortest path is {walked}")

if 0:
    with open("day18_input.txt") as f:
        vault = Vault.from_lines(f)
    print_vault(vault)

