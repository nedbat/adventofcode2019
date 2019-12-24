import collections
import string

import pytest

TEST1 = """\
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""

TEST2 = """\
                   A
                   A
  #################.#############
  #.#...#...................#.#.#
  #.#.#.###.###.###.#########.#.#
  #.#.#.......#...#.....#.#.#...#
  #.#########.###.#####.#.#.###.#
  #.............#.#.....#.......#
  ###.###########.###.#####.#.#.#
  #.....#        A   C    #.#.#.#
  #######        S   P    #####.#
  #.#...#                 #......VT
  #.#.#.#                 #.#####
  #...#.#               YN....#.#
  #.###.#                 #####.#
DI....#.#                 #.....#
  #####.#                 #.###.#
ZZ......#               QG....#..AS
  ###.###                 #######
JO..#.#.#                 #.....#
  #.#.#.#                 ###.#.#
  #...#..DI             BU....#..LF
  #####.#                 #.#####
YN......#               VT..#....QG
  #.###.#                 #.###.#
  #.#...#                 #.....#
  ###.###    J L     J    #.#.###
  #.....#    O F     P    #.#...#
  #.###.#####.#.#####.#####.###.#
  #...#.#.#...#.....#.....#.#...#
  #.#####.###.###.#.#.#########.#
  #...#.#.....#...#.#.#.#.....#.#
  #.###.#####.###.###.#.#.#######
  #.#.........#...#.............#
  #########.###.###.#############
           B   J   C
           U   P   P
"""

def letter(ch):
    return ch in string.ascii_uppercase

def adjacent(x, y):
    yield x - 1, y
    yield x, y - 1
    yield x + 1, y
    yield x, y + 1

class Maze:
    def __init__(self, text):
        self.dots = {}
        letters = {}
        for y, line in enumerate(text.splitlines()):
            for x, ch in enumerate(line):
                if ch == '#':
                    continue
                if ch == '.':
                    self.dots[x, y] = ch
                else:
                    letters[x, y] = ch

        self.labels = collections.defaultdict(list)
        for (x, y), ch in self.dots.items():
            label = None
            w = letters.get((x - 1, y))
            n = letters.get((x, y - 1))
            e = letters.get((x + 1, y))
            s = letters.get((x, y + 1))
            if w:
                ww = letters.get((x - 2, y))
                label = ww + w
            elif n:
                nn = letters.get((x, y - 2))
                label = nn + n
            elif e:
                ee = letters.get((x + 2, y))
                label = e + ee
            elif s:
                ss = letters.get((x, y + 2))
                label = s + ss
            if label:
                self.labels[label].append((x, y))

        self.jumps = {}
        for pair in self.labels.values():
            if len(pair) == 2:
                self.jumps[pair[0]] = pair[1]
                self.jumps[pair[1]] = pair[0]

    def neighbors(self, xy):
        for nxy in adjacent(*xy):
            if nxy in self.dots:
                yield nxy
        if xy in self.jumps:
            yield self.jumps[xy]


def shortest_traverse(maze):
    start = maze.labels['AA'][0]
    end = maze.labels['ZZ'][0]
    edge = set([start])
    came_from = {start: None}
    while end not in came_from:
        next_edge = set()
        for pt in edge:
            for npt in maze.neighbors(pt):
                if npt not in came_from:
                    next_edge.add(npt)
                    came_from[npt] = pt
        edge = next_edge
    
    steps = 0
    pt = end
    while pt is not None:
        pt = came_from[pt]
        steps += 1

    return steps - 1

@pytest.mark.parametrize("maze, steps", [
    (TEST1, 23),
    (TEST2, 58),
])
def test_shortest_traverse(maze, steps):
    actual = shortest_traverse(Maze(maze))
    assert actual == steps

if __name__ == "__main__":
    with open("day20_input.txt") as f:
        maze = Maze(f.read())
    steps = shortest_traverse(maze)
    print(f"Part 1: {steps} steps")
