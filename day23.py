# https://adventofcode.com/2019/day/23

import collections
import contextlib
import random
import time

import blessings

from astar import OnceEvery
from intcode import IntCode, program_from_file

class Nic:
    def __init__(self, network, program, number):
        self.network = network
        self.cpu = IntCode(program, self.input_fn, self.output_fn)
        self.number = number
        self.output = []

    def input_fn(self):
        return self.network.get_input(self.number)

    def output_fn(self, val):
        self.output.append(val)
        if len(self.output) == 3:
            self.network.send_packet(*self.output)
            self.output = []

CPU_COLUMN = 60
Q_COLUMN = CPU_COLUMN - 2
PACKET_COLUMN = CPU_COLUMN + 30
PACKET_WIDTH = 30
PACKET255_COLUMN = PACKET_COLUMN + PACKET_WIDTH + 10
BOTTOM_LINE = 51

@contextlib.contextmanager
def terminal():
    term = blessings.Terminal()
    print(term.clear())
    try:
        with term.hidden_cursor():
            yield term
    finally:
        print(term.move(BOTTOM_LINE+2, 0))

class Network:
    def __init__(self):
        program = program_from_file("day23_input.txt")
        self.nics = [Nic(self, list(program), num) for num in range(50)]
        self.queues = [collections.deque([num]) for num in range(50)]
        self.idle_nics = set()
        self.packet_history = []
        self.packet255 = None
        self.packet255_history = []

    def is_idle(self):
        return all(not q for q in self.queues) and len(self.idle_nics) == 50

    def get_input(self, num):
        if self.queues[num]:
            val = self.queues[num].pop()
            self.draw_queue(num)
            if num in self.idle_nics:
                self.idle_nics.remove(num)
            return val
        else:
            self.idle_nics.add(num)
            return -1

    def draw_list(self, vals, column, width):
        head = max(len(vals) - 50, 0)
        for i, packet in enumerate(vals[-50:]):
            with self.term.location(column, i):
                print(f"{i + head:4}: {packet!s:<{width}}")

    def send_packet(self, nic, x, y):
        self.packet_history.append((nic, x, y))
        if nic == 255:
            if not self.packet255:
                with self.term.location(0, BOTTOM_LINE):
                    print(f"Part 1: Packet 255 has y value of {y}")
            self.packet255 = (x, y)
        else:
            self.queues[nic].extendleft([x, y])
            self.draw_queue(nic)
            self.draw_list(self.packet_history, PACKET_COLUMN, PACKET_WIDTH)

    def draw_queue(self, num):
        queuestr = " ".join(str(val) for val in self.queues[num])
        queuestr = queuestr[-Q_COLUMN:].rjust(Q_COLUMN)
        with self.term.location(0, num):
            print(queuestr)

    def step_one(self, num):
        self.nics[num].cpu.step()

    def draw_cpu(self, num):
        nic = self.nics[num]
        with self.term.location(CPU_COLUMN, num):
            idle = '-' if (num in self.idle_nics) else ' '
            print(f"| {nic.number:3d}{idle} {nic.cpu.steps}")

    def run(self):
        should_log = OnceEvery(seconds=.25)
        with terminal() as self.term:
            for num in range(50):
                self.draw_queue(num)
            while True:
                if self.is_idle() and self.packet255:
                    self.send_packet(0, *self.packet255)
                    p255h = self.packet255_history
                    p255h.append(self.packet255)
                    self.draw_list(p255h, PACKET255_COLUMN, PACKET_WIDTH)
                    if len(p255h) >= 2 and p255h[-1][1] == p255h[-2][1]:
                        with self.term.location(0, BOTTOM_LINE+1):
                            print(f"Part 2: the first y value delivered twice in a row is {p255h[-1][1]}")
                        break
                self.step_one(random.randrange(50))
                if should_log.now():
                    for num in range(50):
                        self.draw_queue(num)
                        self.draw_cpu(num)

if __name__ == '__main__':
    network = Network()
    network.run()
