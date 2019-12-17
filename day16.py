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
        if m:
            total += s * m
    if total >= 0:
        return total % 10
    else:
        return -(total % -10)

def fft(signal):
    return [fft_one_out(signal, i+1) for i in range(len(signal))]

def fftn(signal, n):
    signal = list(int(s) for s in signal)
    for _ in range(n):
        signal = fft(signal)
    return "".join(str(s) for s in signal)

def test_fft():
    assert fftn("12345678", 1) == "48226158"

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


def end_of_fft(rsignal):
    nsig = []
    acc = 0
    for s in rsignal:
        acc += s
        nsig.append(acc % 10)
    return nsig

def end_fftn(signal, n):
    signal = list(int(s) for s in reversed(signal))
    for _ in range(n):
        signal = end_of_fft(signal)
    return "".join(str(s) for s in reversed(signal))

def real_decode(signal):
    offset = int(signal[:7])
    signal *= 10000
    signal = signal[offset:]
    signal = end_fftn(signal, 100)
    return signal[:8]
    
@pytest.mark.parametrize("signal, output", [
    ('03036732577212944063491565474664', '84462026'),
    ('02935109699940807407585447034323', '78725270'),
    ('03081770884921959731165446850517', '53553731'),
])
def test_real_decode(signal, output):
    assert real_decode(signal) == output

if __name__ == '__main__':
    print(f"Part 2: the eight-digit message is {real_decode(INPUT)}")
