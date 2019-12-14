# https://adventofcode.com/2019/day/14

import collections

import pytest


TEST1 = """\
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

TEST2 = """\
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""

TEST3 = """\
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""

TEST4 = """\
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""

TEST5 = """\
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""

def num_thing(s):
    num, thing = s.strip().split()
    return int(num), thing

def parse_reactions(lines):
    if isinstance(lines, str):
        lines = lines.splitlines()
    reactions = {}
    for line in lines:
        ins, out = line.split("=>")
        num_out, thing_out = num_thing(out)
        in_pairs = [num_thing(s) for s in ins.split(",")]
        reactions[thing_out] = (num_out, in_pairs)
    return reactions

def test_parse_reactions():
    assert parse_reactions(TEST1) == {
        'A': (10, [(10, 'ORE')]),
        'B': (1, [(1, 'ORE')]),
        'C': (1, [(7, 'A'), (1, 'B')]),
        'D': (1, [(7, 'A'), (1, 'C')]),
        'E': (1, [(7, 'A'), (1, 'D')]),
        'FUEL': (1, [(7, 'A'), (1, 'E')]),
    }

def make_one_fuel(reactions, have=()):
    need = collections.defaultdict(int)
    extra = collections.defaultdict(int)
    extra.update(have)

    need['FUEL'] = 1

    while True:
        if 'ORE' in need and len(need) == 1:
            break
        for thing, amount in list(need.items()):
            if thing not in reactions:
                continue
            total = extra[thing]
            amount_to_make = amount - extra[thing]
            if amount_to_make > 0:
                react_amt, react_in = reactions[thing]
                num_reactions = (amount_to_make - 1) // react_amt + 1
                for in_amt, in_thing in react_in:
                    need[in_thing] += in_amt * num_reactions
                total += react_amt * num_reactions
            extra[thing] = total - amount
            need[thing] -= amount
        for thing, amount in list(need.items()):
            if amount == 0:
                del need[thing]
    return need['ORE'], tuple(sorted(extra.items()))

def ore_needed(reactions):
    return make_one_fuel(reactions)[0]

@pytest.mark.parametrize("reactions, ore", [
    (TEST1, 31),
    (TEST2, 165),
    (TEST3, 13312),
    (TEST4, 180697),
    (TEST5, 2210736),
])
def test_ore_needed(reactions, ore):
    assert ore_needed(parse_reactions(reactions)) == ore

if __name__ == "__main__":
    with open("day14_input.txt") as f:
        ore = ore_needed(parse_reactions(f))
    print(f"Part 1: need {ore} ore")

def find_cycle(reactions):
    """Returns head_fuel, head_ore, cycle_fuel, cycle_ore """
    # maps have-states to fuel number
    ores = []
    total_fuel = 0
    have = ()
    while True:
        ore, have = make_one_fuel(reactions, have)
        total_fuel += 1
        ores.append(ore)
        if all(x == 0 for _, x in have):
            return total_fuel, ores
        
def total_fuel(reactions, ore_on_hand):
    cycle_info = find_cycle(reactions)
    cycle_fuel, ores = cycle_info
    cycle_ore = sum(ores)
    cycles = ore_on_hand // cycle_ore
    ore_left = ore_on_hand - cycles * cycle_ore
    total_fuel = cycles * cycle_fuel
    for ore in ores:
        if ore > ore_left:
            break
        ore_left -= ore
        total_fuel += 1
    return total_fuel

@pytest.mark.parametrize("reactions, fuel", [
    (TEST1, 34482758620),
    (TEST2, 6323777403),
    (TEST3, 82892753),
    (TEST4, 5586022),
    (TEST5, 460664),
])
def test_total_fuel(reactions, fuel):
    assert total_fuel(parse_reactions(reactions), 1_000_000_000_000) == fuel

if __name__ == "__main__":
    with open("day14_input.txt") as f:
        reactions = parse_reactions(f)
    fuel = total_fuel(reactions, 1_000_000_000_000)
    print(f"Part 2: with 1 trillion ore, we can make {fuel} fuel")
