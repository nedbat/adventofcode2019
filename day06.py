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
