# https://adventofcode.com/2019/day/6

import collections

TEST = """\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
""".splitlines()

def build_orbits(lines):
    orbits = {}
    for line in lines:
        around, orbit = line.strip().split(")")
        orbits[orbit] = around
    return orbits

def direct_and_indirect(orbits, node):
    around = orbits.get(node)
    if around is not None:
        return 1 + direct_and_indirect(orbits, around)
    return 0

def total_orbits(lines):
    orbits = build_orbits(lines)
    return sum(direct_and_indirect(orbits, node) for node in orbits)

def test_total_orbits():
    assert total_orbits(TEST) == 42

def part1():
    with open("day06_input.txt") as f:
        total = total_orbits(f)
    print(f"Part 1: the total direct and indirect orbits are {total}")

if __name__ == "__main__":
    part1()

TEST2 = TEST + """\
K)YOU
I)SAN
""".splitlines()

def path_to_node(orbits, node):
    around = orbits.get(node)
    if around is not None:
        getting_here = path_to_node(orbits, around)
    else:
        getting_here = set()
    return getting_here | {node}

def transfers(orbits, n1, n2):
    p1 = path_to_node(orbits, n1)
    p2 = path_to_node(orbits, n2)
    return len(p1) + len(p2) - 2 * len(p1 & p2) - 2

def tranfers_me_to_santa(lines):
    orbits = build_orbits(lines)
    return transfers(orbits, "YOU", "SAN")

def test_transfers():
    assert tranfers_me_to_santa(TEST2) == 4

def part2():
    with open("day06_input.txt") as f:
        transfers = tranfers_me_to_santa(f)
    print(f"Part 2: orbital transfers required is {transfers}")

if __name__ == "__main__":
    part2()
