# https://adventofcode.com/2019/day/10

import collections
import itertools
import math
import string
import typing

import attr
import pytest

TEST0 = """\
.#..#
.....
#####
....#
...##
"""

TEST1 = """\
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""

TEST2 = """\
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""

TEST3 = """\
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""

TEST4 = """\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

@attr.s
class Belt:
    width: int = 0
    height: int = 0
    asteroids: typing.Set[typing.Tuple[int, int]] = set()

    @classmethod
    def read(cls, text):
        belt = cls()
        belt.asteroids = set()
        x = y = 0
        for c in text:
            if c == '#':
                belt.asteroids.add((x, y))
                x += 1
            elif c == '.':
                x += 1
            elif c == '\n':
                x = 0
                y += 1
        belt.width = max(x for x, y in belt.asteroids) + 1
        belt.height = max(y for x, y in belt.asteroids) + 1
        return belt

    def __iter__(self):
        return iter(self.asteroids)

def radiating_out(cx, cy, width, height):
    max_radius = max([cx, cy, width-cx, height-cy])
    for r in range(1, max_radius+1):
        for d in range(-r, r):
            yield cx + d, cy - r
            yield cx + r, cy + d
            yield cx - d, cy + r
            yield cx - r, cy - d

def in_rect(x, y, width, height):
    return 0 <= x < width and 0 <= y < height

def only_in_rect(seq, width, height):
    """Of the points in `seq`, which are in the width x height field?"""
    for x, y in seq:
        if in_rect(x, y, width, height):
            yield x, y

def radiating(cx, cy, width, height):
    """Produce all the points raditaing from cx, cy, in ring distance order."""
    yield from only_in_rect(radiating_out(cx, cy, width, height), width, height)

def ring_distance(x1, y1, x2, y2):
    """x2, y2 is at what ring distance from x1, y1?"""
    return max([abs(x1 - x2), abs(y1 - y2)])

@pytest.mark.parametrize("w, h, cx, cy", 
    [(wh, wh, cx, cy) for wh in [4, 5] for cx in range(wh) for cy in range(wh)]
)
def test_radiating(w, h, cx, cy):
    points = list(radiating(cx, cy, w, h))
    # We touched every point except where we started:
    assert len(set(points)) == w * h - 1
    # Nearer points come before farther points:
    distances = [ring_distance(cx, cy, x, y) for x, y in points]
    assert sorted(distances) == distances

def multiples(cx, cy, dx, dy, start_mult, width, height):
    for mult in itertools.count(start_mult+1):
        x = cx + mult * dx
        y = cy + mult * dy
        if in_rect(x, y, width, height):
            yield x, y
        else:
            break

def step_size(dx, dy):
    d = math.gcd(dx, dy)
    return dx // d, dy // d, d

def visible(belt, x, y):
    """Which asteroids are visible in belt from x, y?"""
    asts = set(belt)
    asts.remove((x, y))
    debug = dict.fromkeys(belt, '#')
    markers = iter(string.ascii_uppercase)
    for ax, ay in radiating(x, y, belt.width, belt.height):
        if (ax, ay) not in asts:
            continue
        # ax, ay is visible. Take out any asteroids it blocks
        marker = next(markers, 'Z')
        debug[ax, ay] = marker
        dx, dy, start_mult = step_size(ax - x, ay - y)
        for axd, ayd in multiples(x, y, dx, dy, start_mult, belt.width, belt.height):
            if (axd, ayd) in asts:
                asts.remove((axd, ayd))
                debug[axd, ayd] = marker.lower()
    # print(f"\nConsidering {x, y}")
    # print_debug(debug)
    return asts

def print_debug(debug):
    width = max(x for x, y in debug) + 1
    height = max(y for x, y in debug) + 1
    for y in range(height):
        for x in range(width):
            print(debug.get((x, y), "."), end="")
        print()
    print("-" * width)

def spot_ratings(belt):
    for x, y in belt:
        vis = visible(belt, x, y)
        yield x, y, len(vis)

TEST0_RATINGS = {(1, 0, 7), (4, 0, 7), (0, 2, 6), (1, 2, 7), (2, 2, 7), (3, 2, 7), (4, 2, 5), (4, 3, 7), (3, 4, 8), (4, 4, 7)}

def test_spot_ratings():
    belt = Belt.read(TEST0)
    ratings = set(spot_ratings(belt))
    assert ratings == TEST0_RATINGS

def best_spot(belt):
    return max(spot_ratings(belt), key=lambda x_y_vis: x_y_vis[2])

BEST_SPOT_TESTS = [
    (TEST0, 3, 4, 8),
    (TEST1, 5, 8, 33),
    (TEST2, 1, 2, 35),
    (TEST3, 6, 3, 41),
    (TEST4, 11, 13, 210),
]
@pytest.mark.parametrize("belt_text, x, y, vis", BEST_SPOT_TESTS)
def test_best_spot(belt_text, x, y, vis):
    belt = Belt.read(belt_text)
    assert best_spot(belt) == (x, y, vis)

def the_belt():
    with open("day10_input.txt") as f:
        return Belt.read(f.read())

def part1():
    x, y, vis = best_spot(the_belt())
    print(f"Part 1: the best spot is {x, y} with {vis} asteroids visible")

if __name__ == "__main__":
    part1()


# Part 2 makes clear that I should have been using trig all along.

def radians_to_delta(dx, dy):
    a = math.atan2(dx, -dy)
    if a < 0:
        a += 2 * math.pi
    return a

def distance_to_delta(dx, dy):
    """Not exact distance, just sorts the same for the same angle."""
    return dx * dx

def test_radians_to_delta():
    angles = [radians_to_delta(dx, dy) for dx, dy in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]]
    assert sorted(angles) == angles

def asteroid_polars(belt, cx, cy):
    """Report on asteroids in polar coordinates from cx, cy"""
    for ax, ay in belt:
        if (ax, ay) == (cx, cy):
            continue
        dx, dy = ax - cx, ay - cy
        yield ax, ay, radians_to_delta(dx, dy), distance_to_delta(dx, dy)

def visible_trig(belt, x, y):
    polars = list(asteroid_polars(belt, x, y))
    angles = set(a for ax, ay, a, d in polars)
    return len(angles)

def spot_ratings_trig(belt):
    for x, y in belt:
        vis = visible_trig(belt, x, y)
        yield x, y, vis

def best_spot_trig(belt):
    return max(spot_ratings_trig(belt), key=lambda x_y_vis: x_y_vis[2])

@pytest.mark.parametrize("belt_text, x, y, vis", BEST_SPOT_TESTS)
def test_best_spot_trig(belt_text, x, y, vis):
    belt = Belt.read(belt_text)
    assert best_spot_trig(belt) == (x, y, vis)

def asteroid_vaporization_order(belt, x, y):
    polars = list(asteroid_polars(belt, x, y))
    by_angle = collections.defaultdict(list)
    for ax, ay, ang, dist in polars:
        by_angle[ang].append((dist, ax, ay))
    for angle, asteroids in by_angle.items():
        by_angle[angle] = sorted(asteroids)
    angles = sorted(by_angle)
    while True:
        any_found = False
        for angle in angles:
            asteroids = by_angle[angle]
            if asteroids:
                dist, ax, ay = asteroids.pop()
                yield ax, ay
                any_found = True
        if not any_found:
            break

def test_asteroid_vaporization_order():
    belt = Belt.read(TEST4)
    bx, by, vis = best_spot_trig(belt)
    assert vis == 210
    order = list(asteroid_vaporization_order(belt, bx, by))
    print(order)
    assert order[0] == (11, 12)
    assert order[199] == (8, 2)

def part2():
    belt = the_belt()
    x, y, vis = best_spot_trig(belt)
    assert vis == 282
    order = list(asteroid_vaporization_order(belt, x, y))
    th200 = order[199]
    print(f"Part 2: the 200th asteroid vaporized is at {th200}")

if __name__ == "__main__":
    part2()
