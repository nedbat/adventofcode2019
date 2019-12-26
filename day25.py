# https://adventofcode.com/2019/day/25

import itertools
import re

from intcode import IntCode, program_from_file

import pytest

class Day25Computer:
    MAX_STEPS = 1_000_000

    def __init__(self):
        program = program_from_file("day25_input.txt")
        self.cpu = IntCode(program, self.input_fn, self.output_fn)
        self.input = []
        self.output = ""
        self.done = False
    
    def input_fn(self):
        if not self.input:
            command = self.command_fn(self.output)
            self.output = ""
            self.input = ["\n"]
            self.input.extend(reversed(command))
        return ord(self.input.pop())

    def output_fn(self, val):
        self.output += chr(val)

    def run(self):
        while not self.done and self.cpu.steps < self.MAX_STEPS:
            if not self.cpu.step():
                break
        self.done = True


def parse_text(text):
    msgs = [
        ('normal', r"""(?xs)
            \n\n\n
            ==\ (?P<room>[^=]+?)\ ==\n
            (?P<description>[^\n]+)\n\n
            (?:Doors\ here\ lead:\n(?P<doors>[^A-Z]+)\n\n)?
            (?:Items\ here:\n(?P<items>.+)\n\n)?
            Command\?\n
            """),
        ('took', r"\nYou take the (?P<item>.*).\n\nCommand\?\n"),
        ('dropped', r"\nYou drop the (?P<item>.*).\n\nCommand\?\n"),
        ('inv', r"\nItems in your inventory:\n(?P<items>.+)\n\nCommand\?\n"),
        ('weighed', r"(?s)\n\n\n== (?P<room>[^=]+) ==\n.*Alert! Droids on this ship are (?P<weight>\S+) than the detected value!.*"),
    ]

    for state, pattern in msgs:
        m = re.match(pattern, text)
        if m:
            data = m.groupdict()
            for things in ['doors', 'items']:
                if things in data and data[things]:
                    data[things] = [door.lstrip("- ") for door in data[things].split("\n")]
            data['state'] = state
            return data
    else:
        return {'state': 'confused', 'text': text}


@pytest.mark.parametrize("text, data", [
    (
    '\n\n\n== Hull Breach ==\nYou got in through a hole in the floor here. To keep your ship from also freezing, the hole has been sealed.\n\nDoors here lead:\n- north\n- east\n- south\n\nCommand?\n',
    {
        'state': 'normal',
        'room': 'Hull Breach',
        'description': 'You got in through a hole in the floor here. To keep your ship from also freezing, the hole has been sealed.',
        'doors': ['north', 'east', 'south'],
        'items': None,
    }),
    (
    "\n\n\n== Hallway ==\nThis area has been optimized for something; you're just not quite sure what.\n\nDoors here lead:\n- south\n\nItems here:\n- giant electromagnet\n\nCommand?\n",
    {
        'state': 'normal',
        'room': 'Hallway',
        'description': "This area has been optimized for something; you're just not quite sure what.",
        'doors': ['south'],
        'items': ['giant electromagnet'],
    }),
    (
    '\nYou take the mouse.\n\nCommand?\n',
    {
        'state': 'took',
        'item': 'mouse',
    }),
    (
    '\nYou drop the dead mouse.\n\nCommand?\n',
    {
        'state': 'dropped',
        'item': 'dead mouse',
    }),
    (
    '\nItems in your inventory:\n- mouse\n\nCommand?\n',
    {
        'state': 'inv',
        'items': ['mouse'],
    }),
    (
    '\nThis is another thing that happened!\n',
    {
        'state': 'confused',
        'text': '\nThis is another thing that happened!\n',
    }),
    (
    '\n\n\n== Pressure-Sensitive Floor ==\nAnalyzing...\n\nDoors here lead:\n- north\n\nA loud, robotic voice says "Alert! Droids on this ship are heavier than the detected value!" and you are ejected back to the checkpoint.\n'
    '\n\n\n== Security Checkpoint ==\nIn the next room, a pressure-sensitive floor will verify your identity.\n\nDoors here lead:\n- north\n- south\n\nCommand?\n',
    {
        'state': 'weighed',
        'room': 'Pressure-Sensitive Floor',
        'weight': 'heavier',
    }),
])
def test_parse_text(text, data):
    assert parse_text(text) == data

class InteractiveComputer(Day25Computer):
    def command_fn(self, text):
        print(repr(text))
        print(parse_text(text))
        print(text)
        command = input("> ")
        return command

class FixedCommandsComputer(Day25Computer):
    def __init__(self, commands):
        super().__init__()
        self.commands = commands
        self.data = {'state': None}

    def command_fn(self, text):
        if self.commands:
            command = self.commands[0]
            self.commands = self.commands[1:]
            return command
        else:
            data = parse_text(text)
            self.data = data
            self.done = True
            return "inv"

def room_at_end_of_path(path):
    comp = FixedCommandsComputer(path)
    comp.run()
    return comp.data

@pytest.mark.parametrize("path, room", [
    ([], "Hull Breach"),
    (["north"], "Hallway"),
    (["north", "south", "east", "south"], "Warp Drive Maintenance"),
])
def test_room_at_end_of_path(path, room):
    assert room_at_end_of_path(path)['room'] == room

def map_rooms():
    start = room_at_end_of_path([])
    start['path'] = []
    # map room names to data about the room.
    rooms = {start['room']: start}
    edge = set([start['room']])
    while edge:
        next_edge = set()
        for room_name in edge:
            room = rooms[room_name]
            for door in room['doors']:
                npath = room['path'] + [door]
                next_room = room_at_end_of_path(npath)
                if next_room['state'] == 'weighed':
                    next_room['doors'] = next_room['items'] = []
                if next_room['room'] not in rooms:
                    next_room['path'] = npath
                    next_edge.add(next_room['room'])
                    rooms[next_room['room']] = next_room
        edge = next_edge
    return rooms

def item_map(rooms):
    items = {}
    for room_name, room in rooms.items():
        for item in room['items'] or ():
            items[item] = room_name
    return items

def takable_items(rooms, items):
    takable = {}
    for item, in_room in items.items():
        commands = []
        commands += rooms[in_room]['path']
        commands += [f"take {item}", f"drop {item}"] 
        comp = FixedCommandsComputer(commands)
        comp.run()
        data = comp.data
        if data['state'] == 'dropped':
            takable[item] = in_room
    return takable

BACK = {
    'north': 'south',
    'east': 'west',
    'south': 'north',
    'west': 'east',
}

def common_head_len(seq1, seq2):
    num = 0
    for a, b in zip(seq1, seq2):
        if a != b:
            break
        num += 1
    return num

@pytest.mark.parametrize("seq1, seq2, head", [
    ("abcde", "abcxy", 3),
    ("xyz", "abc", 0),
    ("", "abc", 0),
    ("abcde", "abcde", 5),
])
def test_common_head_len(seq1, seq2, head):
    assert common_head_len(seq1, seq2) == head

def navigate(from_room, to_room):
    fpath = from_room['path']
    tpath = to_room['path']
    head = common_head_len(fpath, tpath)
    back_to_common = [BACK[d] for d in reversed(fpath[head:])]
    return back_to_common + tpath[head:]


def weigh_items(rooms, items, to_take):
    at = next(room for room in rooms.values() if room['path'] == [])
    finish = next(room for room in rooms.values() if room['state'] == 'weighed')
    commands = []
    for item in to_take:
        item_room = rooms[items[item]]
        commands += navigate(at, item_room)
        commands += [f"take {item}"] 
        at = item_room
    commands += navigate(at, finish)
    comp = FixedCommandsComputer(commands)
    comp.run()
    data = comp.data
    if 'weight' not in data:
        return comp.output

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, len(s)+1))

def test_powerset():
    assert set("".join(them) for them in powerset("abc")) == set("a b c ab bc ac abc".split())

if 1 and __name__ == "__main__":
    rooms = map_rooms()
    items = item_map(rooms)
    items = takable_items(rooms, items)
    for to_take in powerset(items):
        data = weigh_items(rooms, items, to_take)
        if data is not None:
            print(data)
            break

if 0 and __name__ == "__main__":
    comp = InteractiveComputer()
    comp.run()
