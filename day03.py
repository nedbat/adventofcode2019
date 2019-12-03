# https://adventofcode.com/2019/day/3

import pytest

def parse_wire(wire_spec):
    """Parse a wire, yielding ((dx,dy), distance)."""
    directions = {'R': (1, 0), 'U': (0, 1), 'L': (-1, 0), 'D': (0, -1)}
    for move in wire_spec.split(","):
        direction = move[0]
        distance = int(move[1:])
        yield directions[direction], distance


def points_on_wire(wire_spec):
    """Yield the (x,y) points a wire touches.

    `wire_spec` is a string like "R8,U5,L5,D3".

    """
    x, y = 0, 0
    for (dx, dy), distance in parse_wire(wire_spec):
        for _ in range(distance):
            x += dx; y += dy
            yield x, y

def wire_intersections(spec1, spec2):
    return set(points_on_wire(spec1)) & set(points_on_wire(spec2))


def distance_to_closest_intersection(spec1, spec2):
    intersections = wire_intersections(spec1, spec2)
    distance = min(abs(x) + abs(y) for x, y in intersections)
    return distance

@pytest.mark.parametrize("spec1, spec2, distance", [
    ("R8,U5,L5,D3", "U7,R6,D4,L4", 6),
    ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159),
    ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135),
])
def test_distance_to_closest_intersection(spec1, spec2, distance):
    assert distance_to_closest_intersection(spec1, spec2) == distance


def specs_from_file(fname):
    with open(fname) as f:
        text = f.read()
    return text.splitlines()

def part1():
    distance = distance_to_closest_intersection(*specs_from_file("day03_input.txt"))
    print(f"Part 1: distance to closest intersection is {distance}")

if __name__ == "__main__":
    part1()
