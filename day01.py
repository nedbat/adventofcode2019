# https://adventofcode.com/2019/day/1

import pytest

def fuel_for_module(mass):
    return mass // 3 - 2

@pytest.mark.parametrize("mass, fuel", [
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583),
])
def test_fuel_for_module(mass, fuel):
    assert fuel_for_module(mass) == fuel

if __name__ == "__main__":
    with open("day01_input.txt") as f:
        modules = list(map(int, f))

    all_fuel = sum(map(fuel_for_module, modules))

    print(f"Part 1: the sum of the fuel requirements is {all_fuel}")
