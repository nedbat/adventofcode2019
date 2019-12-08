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

def flatten_layers(image):
    wide = len(image[0][0])
    tall = len(image[0])
    flat = ["2" * wide for _ in range(tall)]

    for layer in reversed(image):
        next_flat = []
        for frow, lrow in zip(flat, layer):
            next_row = "".join(f if l == "2" else l for f, l in zip(frow, lrow))
            next_flat.append(next_row)
        flat = next_flat

    return flat

def test_flatten_layers():
    image = read_layers("0222112222120000", 2, 2)
    flat = flatten_layers(image)
    assert flat == ["01", "10"]

def part2():
    image = the_image()
    flat = flatten_layers(image)
    print(f"Part 2:")
    art = "#. "
    for row in flat:
        print("".join("#. "[int(d)] for d in row))

if __name__ == "__main__":
    part2()
