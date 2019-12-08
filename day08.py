# https://adventofcode.com/2019/day/8

def read_layers(digits, wide, tall):
    layers = []
    perlayer = wide * tall
    for start_layer in range(0, len(digits), perlayer):
        layer = []
        for start_row in range(0, perlayer, wide):
            start = start_layer + start_row
            layer.append(digits[start: start + wide])
        layers.append(layer)
    return layers

def test_read_layers():
    assert read_layers("123456789012", 3, 2) == [["123", "456"], ["789", "012"]]

def digits_in_layer(layer, digit):
    return sum(row.count(digit) for row in layer)

def the_image():
    with open("day08_input.txt") as f:
        return read_layers(f.read().strip(), 25, 6)

def part1():
    image = the_image()
    fewest_zeros = min(image, key=lambda l: digits_in_layer(l, "0"))
    ones_time_twos = digits_in_layer(fewest_zeros, "1") * digits_in_layer(fewest_zeros, "2")
    print(f"Part 1: ones times twos is {ones_time_twos}")

if __name__ == "__main__":
    part1()
