# https://adventofcode.com/2019/day/4

import pytest

# Brute force

def is_ok_password(num):
    strnum = str(num)
    has_double = any(a == b for a, b in zip(strnum, strnum[1:]))
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

def is_ok_password2(num):
    strnum = str(num)
    strnum_padded = "X" + strnum + "X"
    has_good_double = any(x != a == b != y for x, a, b, y in zip(strnum_padded, strnum_padded[1:], strnum_padded[2:], strnum_padded[3:]))
    monotonic = all(a <= b for a, b in zip(strnum, strnum[1:]))
    return has_good_double and monotonic

@pytest.mark.parametrize("num, ok", [
    (112233, True),
    (123444, False),
    (123789, False),
    (111122, True),
])
def test_is_ok_password2(num, ok):
    assert is_ok_password2(num) == ok

def part2():
    count = sum(int(is_ok_password2(num)) for num in range(367479, 893698))
    print(f"Part 2: there are {count} different passwords")

if __name__ == "__main__":
    part2()
