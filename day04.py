# https://adventofcode.com/2019/day/4

import re

import pytest

# Brute force

def is_ok_password(num):
    strnum = str(num)
    has_double = bool(re.search(r"(.)\1", strnum))
    monotonic = all(a <= b for a, b in zip(strnum, strnum[1:]))
    return has_double and monotonic

@pytest.mark.parametrize("num, ok", [
    (111111, True),
    (223450, False),
    (123789, False),
])
def test_is_ok_password(num, ok):
    assert is_ok_password(num) == ok


def part1():
    count = sum(int(is_ok_password(num)) for num in range(367479, 893698))
    print(f"Part 1: there are {count} different passwords")

if __name__ == "__main__":
    part1()
