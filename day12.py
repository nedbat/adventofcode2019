# https://adventofcode.com/2019/day/12

import itertools


class Xyz:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"<x={self.x}, y={self.y}, z={self.z}>"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        return Xyz(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Xyz(self.x - other.x, self.y - other.y, self.z - other.z)

    def sign(self):
        return Xyz(sign(self.x), sign(self.y), sign(self.z))

    def abs(self):
        return abs(self.x) + abs(self.y) + abs(self.z)


Xyz0 = Xyz(0, 0, 0)

def test_xyz():
    assert repr(Xyz(1,2,3) + Xyz(10,20,30)) == "<x=11, y=22, z=33>"
    assert repr(Xyz(1,2,3) - Xyz(10,20,30)) == "<x=-9, y=-18, z=-27>"


class Moon:
    def __init__(self, pos, vel=Xyz0):
        self.pos = pos
        self.vel = vel

    def __repr__(self):
        return f"Moon(pos={self.pos}, vel={self.vel})"

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel

    def energy(self):
        return self.pos.abs() * self.vel.abs()


def sign(val):
    if val < 0:
        return -1
    elif val > 0:
        return 1
    else:
        return 0


TEST1 = [
    Moon(Xyz(x=-1, y=0, z=2)),
    Moon(Xyz(x=2, y=-10, z=-7)),
    Moon(Xyz(x=4, y=-8, z=8)),
    Moon(Xyz(x=3, y=5, z=-1)),
]

TEST2 = [
    Moon(Xyz(x=-8, y=-10, z=0)),
    Moon(Xyz(x=5, y=5, z=10)),
    Moon(Xyz(x=2, y=-7, z=3)),
    Moon(Xyz(x=9, y=-8, z=-3)),
]

def simulate(moons):
    while True:
        yield moons
        gravity = [sum([(o.pos - m.pos).sign() for o in moons], Xyz0) for m in moons]
        vels = [m.vel + g for m, g in zip(moons, gravity)]
        moons = [Moon(m.pos + v, v) for m, v in zip(moons, vels)]

def total_energy(moons):
    return sum(m.energy() for m in moons)

def test_simulate():
    steps = simulate(TEST1)
    for i in range(11):
        moons = next(steps)
        print(i, moons)
    assert moons == [
        Moon(pos=Xyz(x= 2, y= 1, z=-3), vel=Xyz(x=-3, y=-2, z= 1)),
        Moon(pos=Xyz(x= 1, y=-8, z= 0), vel=Xyz(x=-1, y= 1, z= 3)),
        Moon(pos=Xyz(x= 3, y=-6, z= 1), vel=Xyz(x= 3, y= 2, z=-3)),
        Moon(pos=Xyz(x= 2, y= 0, z= 4), vel=Xyz(x= 1, y=-1, z=-1)),
    ]
    assert total_energy(moons) == 179

def after_steps(moons, steps):
    return next(itertools.islice(simulate(moons), steps, steps+1))

def test_simulate2():
    assert total_energy(after_steps(TEST2, 100)) == 1940

INPUT = [
    Moon(Xyz(x=-3, y=15, z=-11)),
    Moon(Xyz(x=3, y=13, z=-19)),
    Moon(Xyz(x=-13, y=18, z=-2)),
    Moon(Xyz(x=6, y=0, z=-1)),
]

if __name__ == "__main__":
    energy = total_energy(after_steps(INPUT, 1000))
    print(f"Part 1: total energy after 1000 steps is {energy}")


