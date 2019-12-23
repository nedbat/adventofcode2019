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

@contextlib.contextmanager
def terminal():
    term = blessings.Terminal()
    print(term.clear())
    try:
        with term.hidden_cursor():
            yield term
    finally:
        print(term.move(51, 0))

class Network:
    CPU_COLUMN = 80
    Q_COLUMN = 78
    PACKET_COLUMN = 120
    PACKET_WIDTH = 30

    def __init__(self):
        program = program_from_file("day23_input.txt")
        self.nics = [Nic(self, list(program), num) for num in range(50)]
        self.queues = [collections.deque([num]) for num in range(50)]
        self.packet_history = []
        self.packet255 = None

    def get_input(self, num):
        if self.queues[num]:
            val = self.queues[num].popleft()
            self.draw_queue(num)
            return val
        else:
            return -1

    def send_packet(self, nic, x, y):
        self.packet_history.append((nic, x, y))
        if nic == 255:
            self.packet255 = (x, y)
        else:
            self.queues[nic].extend([x, y])
            self.draw_queue(nic)
            for i, packet in enumerate(self.packet_history[-50:]):
                with self.term.location(self.PACKET_COLUMN, i):
                    print(str(packet).ljust(self.PACKET_WIDTH))

    def draw_queue(self, num):
        queuestr = " ".join(str(val) for val in self.queues[num])
        queuestr = queuestr[-self.Q_COLUMN:].rjust(self.Q_COLUMN)
        with self.term.location(0, num):
            print(queuestr)

    def step_one(self, num):
        self.nics[num].cpu.step()

    def draw_cpu(self, num):
        nic = self.nics[num]
        with self.term.location(self.CPU_COLUMN, num):
            print(f"| {nic.number:3d} {nic.cpu.steps}")

    def run(self):
        should_log = OnceEvery(seconds=.01)
        with terminal() as self.term:
            for num in range(50):
                self.draw_queue(num)
            while self.packet255 is None:
                self.step_one(random.randrange(50))
                if should_log.now():
                    for num in range(50):
                        self.draw_queue(num)
                        self.draw_cpu(num)

if __name__ == '__main__':
    network = Network()
    network.run()
    print(f"Packet 255 has y value of {network.packet255[1]}")
