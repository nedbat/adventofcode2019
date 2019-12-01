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

def fuel_for_modules(modules):
    return sum(map(fuel_for_module, modules))

if __name__ == "__main__":
    with open("day01_input.txt") as f:
        modules = list(map(int, f))

    all_fuel = fuel_for_modules(modules)

    print(f"Part 1: the sum of the fuel requirements is {all_fuel}")


def fuel_for_module_and_fuel(mass):
    total = 0
    fuel = fuel_for_module(mass)
    while fuel > 0:
        total += fuel
        fuel = fuel_for_module(fuel)
    return total

@pytest.mark.parametrize("mass, fuel", [
    (14, 2),
    (1969, 966),
    (100756, 50346),
])
def test_fuel_for_modules_and_fuel(mass, fuel):
    assert fuel_for_module_and_fuel(mass) == fuel

def fuel_for_modules_and_fuel(modules):
    return sum(map(fuel_for_module_and_fuel, modules))

if __name__ == "__main__":
    total_fuel = fuel_for_modules_and_fuel(modules)
    print(f"Part 2: the sum of the fuel requirements including the fuel is {total_fuel}")
