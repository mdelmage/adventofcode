#!/usr/bin/python
# coding: utf-8

import copy
from collections import namedtuple
import random

MOVE_NORTH = 1
MOVE_SOUTH = 2
MOVE_WEST  = 3
MOVE_EAST  = 4

NEXT_COMMAND = { MOVE_NORTH: MOVE_EAST,
                 MOVE_SOUTH: MOVE_WEST,
                 MOVE_WEST:  MOVE_NORTH,
                 MOVE_EAST:  MOVE_SOUTH }

MOVEMENT = { MOVE_NORTH: ( 0,  1),
             MOVE_SOUTH: ( 0, -1),
             MOVE_WEST:  (-1,  0),
             MOVE_EAST:  ( 1,  0) }

MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]

STATUS_BLOCKED = 0
STATUS_OK      = 1
STATUS_OXYGEN  = 2

TILE_EMPTY  = '.'
TILE_WALL   = '#'
TILE_OXYGEN = 'O'
TILE_START  = 's'

# By inspection
MAP_SIZE = 1659

class IntcodeNode:
    Pointer = namedtuple('Pointer', 'address value')

    OPCODE_ADD      = 1
    OPCODE_MULTIPLY = 2
    OPCODE_INPUT    = 3
    OPCODE_OUTPUT   = 4
    OPCODE_JIT      = 5
    OPCODE_JIF      = 6
    OPCODE_LT       = 7
    OPCODE_EQ       = 8
    OPCODE_RELATIVE = 9
    OPCODE_HALT     = 99

    ADDRESS_POSITION  = 0
    ADDRESS_IMMEDIATE = 1
    ADDRESS_RELATIVE  = 2

    opcode_lengths = { OPCODE_ADD      : 4,
                       OPCODE_MULTIPLY : 4,
                       OPCODE_INPUT    : 2,
                       OPCODE_OUTPUT   : 2,
                       OPCODE_JIT      : 0,
                       OPCODE_JIF      : 0,
                       OPCODE_LT       : 4,
                       OPCODE_EQ       : 4,
                       OPCODE_RELATIVE : 2,
                       OPCODE_HALT     : 0 }

    def __init__(self, program):
        self.program = copy.deepcopy(program)
        self.relative_base = 0
        self.pc = 0
        self.output = []

        # Day 15-specific attributes
        self.location = (0, 0)
        self.next_location = (0, 1)
        self.command = MOVE_NORTH
        self.map = {(0, 0): TILE_START}
        self.oxygen = None

    def read(self, address):
        if address in self.program:
            return self.program[address]
        else:
            return 0

    def write(self, address, value):
        self.program[address] = value

    def parameter(self, address, mode):
        param = 0

        # Use exceptions to simplify command processing.
        # Shorter opcodes may dereference invalid memory
        # when calculating extra params.
        try:
            if self.ADDRESS_POSITION == mode:
                # Return (parameter, *parameter)
                param = self.Pointer(self.read(self.pc + address), self.read(self.read(self.pc + address)))
            elif self.ADDRESS_IMMEDIATE == mode:
                # Return (&parameter, parameter)
                param = self.Pointer(self.pc + address, self.read(self.pc + address))
            elif self.ADDRESS_RELATIVE == mode:
                # Return (parameter + relative base, *(parameter + relative base)
                param = self.Pointer(self.read(self.pc + address) + self.relative_base, self.read(self.read(self.pc + address) + self.relative_base))
            else:
                print "Unknown parameter mode {0}!".format(mode)
        except:
            pass

        return param

    def print_screen(self):
        print "Map size: {0}".format(len(self.map))
        for y in range(25, -25, -1):
            row = ""
            for x in range(-25, 25):
                if self.location == (x, y):
                    row += "R"
                elif (x, y) in self.map:
                    try:
                        row += str(self.map[(x, y)] % 10)
                    except:
                        row += str(self.map[(x, y)])
                else:
                    row += " "
            print row

    def measure_paths(self, source):
        paths = {0: [source]}
        path_len = 0

        while len(paths[path_len]) > 0:
            paths[path_len + 1] = []
            for coord in paths[path_len]:
                self.map[coord] = path_len
                for move in MOVES:
                    next_coord = (coord[0] + move[0], coord[1] + move[1])
                    if self.map[next_coord] in (TILE_EMPTY, TILE_OXYGEN, TILE_START):
                        paths[path_len + 1].append(next_coord)
            path_len += 1

        return path_len - 1

    def execute(self):
        while self.read(self.pc) != self.OPCODE_HALT:
            instruction = self.read(self.pc)
            opcode = instruction % 100
            param1_mode = (instruction / 100) % 10
            param2_mode = (instruction / 1000) % 10
            param3_mode = (instruction / 10000) % 10

            param1 = self.parameter(1, param1_mode)
            param2 = self.parameter(2, param2_mode)
            param3 = self.parameter(3, param3_mode)

            if self.OPCODE_ADD == opcode:
                self.write(param3.address, param1.value + param2.value)
            elif self.OPCODE_MULTIPLY == opcode:
                self.write(param3.address, param1.value * param2.value)
            elif self.OPCODE_INPUT == opcode:
                # Wayfinding?? Uh, roll dice, go that way.
                self.command = random.randint(1, len(MOVES))

                self.next_location = (self.location[0] + MOVEMENT[self.command][0],
                                      self.location[1] + MOVEMENT[self.command][1])
                self.write(param1.address, self.command)
            elif self.OPCODE_OUTPUT == opcode:
                if STATUS_BLOCKED == param1.value:
                    self.map[self.next_location[0], self.next_location[1]] = TILE_WALL
                    #self.command = NEXT_COMMAND[self.command]
                    #self.next_location = (self.location[0] + MOVEMENT[self.command][0],
                    #                      self.location[1] + MOVEMENT[self.command][1])
                    #print "trying to move from {0} to {1}".format(self.location, self.next_location)
                elif STATUS_OK == param1.value:
                    if self.next_location not in self.map:
                        self.map[self.next_location] = TILE_EMPTY
                    self.location = self.next_location
                else:
                    self.map[self.next_location[0], self.next_location[1]] = TILE_OXYGEN
                    self.location = self.next_location
                    self.oxygen = self.location
            elif self.OPCODE_JIT == opcode:
                self.pc = param2.value if param1.value != 0 else self.pc + 3
            elif self.OPCODE_JIF == opcode:
                self.pc = param2.value if param1.value == 0 else self.pc + 3
            elif self.OPCODE_LT == opcode:
                self.write(param3.address, 1 if param1.value < param2.value else 0)
            elif self.OPCODE_EQ == opcode:
                self.write(param3.address, 1 if param1.value == param2.value else 0)
            elif self.OPCODE_RELATIVE == opcode:
                self.relative_base += param1.value
            else:
                print "Unknown opcode {0} @ PC {1} RB {2}!".format(opcode, self.pc, self.relative_base)
                break

            self.pc += self.opcode_lengths[opcode]

            if MAP_SIZE == len(self.map):
                break

        #print "halt @ PC {0} ({1})".format(self.pc, self.read(self.pc))
        self.print_screen()

# Open input file
filename = "day15.txt"
f = open(filename, "r")

random.seed(0)

with open(filename, "r") as f:
    for line in f:
        i = 0
        program = {}
        for item in line.strip().split(","):
            program[i] = int(item)
            i += 1

        # Phase I: Produce a map with Intcode program
        node = IntcodeNode(program)
        node.execute()

        # Phase II: Pathfinding
        n1 = copy.deepcopy(node)
        n1.measure_paths((0, 0))
        n1.print_screen()
        print "The shortest path to the oxygen system is {0}!".format(n1.map[node.oxygen])

        # Phase III: Oxygenating
        n2 = copy.deepcopy(node)
        print "It took {0} minutes to replenish the ship with O2!".format(n2.measure_paths(node.oxygen))