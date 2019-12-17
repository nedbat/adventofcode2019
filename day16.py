# https://adventofcode.com/2019/day/16

import itertools

import pytest


def base_pattern(n):
    while True:
        for val in [0, 1, 0, -1]:
            yield from [val] * n

def repeating_pattern(n):
    return itertools.islice(base_pattern(n), 1, None)

def test_repeating_pattern():
    assert list(itertools.islice(repeating_pattern(3), 10)) == [0, 0, 1, 1, 1, 0, 0, 0, -1, -1]


def fft_one_out(signal, i):
    total = 0
    for s, m in zip(signal, repeating_pattern(i)):
        if m == 0:
            continue
        s = int(s)
        total += s * m
    return str(total)[-1]

def fft(signal):
    return "".join(fft_one_out(signal, i+1) for i in range(len(signal)))

def test_fft():
    assert fft("12345678") == "48226158"

def fftn(signal, n):
    for _ in range(n):
        signal = fft(signal)
    return signal

@pytest.mark.parametrize("signal, output", [
    ('80871224585914546619083218645595', '24176176'),
    ('19617804207202209144916044189917', '73745418'),
    ('69317163492948606335995924319873', '52432133'),
])
def test_fft_100(signal, output):
    assert fftn(signal, 100)[:8] == output

INPUT = '59782619540402316074783022180346847593683757122943307667976220344797950034514416918778776585040527955353805734321825495534399127207245390950629733658814914072657145711801385002282630494752854444244301169223921275844497892361271504096167480707096198155369207586705067956112600088460634830206233130995298022405587358756907593027694240400890003211841796487770173357003673931768403098808243977129249867076581200289745279553289300165042557391962340424462139799923966162395369050372874851854914571896058891964384077773019120993386024960845623120768409036628948085303152029722788889436708810209513982988162590896085150414396795104755977641352501522955134675'

if __name__ == '__main__':
    digit8 = fftn(INPUT, 100)[:8]
    print(f"Part 1: first eight in the final output list are {digit8}")
