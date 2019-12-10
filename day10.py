# https://adventofcode.com/2019/day/10

from math import gcd
import itertools
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
    d = gcd(dx, dy)
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

def test_spot_ratings():
    belt = Belt.read(TEST0)
    ratings = set(spot_ratings(belt))
    assert ratings == {(1, 0, 7), (4, 0, 7), (0, 2, 6), (1, 2, 7), (2, 2, 7), (3, 2, 7), (4, 2, 5), (4, 3, 7), (3, 4, 8), (4, 4, 7)}

def best_spot(belt):
    return max(spot_ratings(belt), key=lambda x_y_vis: x_y_vis[2])

@pytest.mark.parametrize("belt_text, x, y, vis", [
    (TEST0, 3, 4, 8),
    (TEST1, 5, 8, 33),
    (TEST2, 1, 2, 35),
    (TEST3, 6, 3, 41),
    (TEST4, 11, 13, 210),
])
def test_best_spot(belt_text, x, y, vis):
    belt = Belt.read(belt_text)
    print(sorted(belt))
    assert best_spot(belt) == (x, y, vis)

def the_belt():
    with open("day10_input.txt") as f:
        return Belt.read(f.read())

def part1():
    x, y, vis = best_spot(the_belt())
    print(f"Part 1: the best spot is {x, y} with {vis} asteroids visible")

if __name__ == "__main__":
    part1()
