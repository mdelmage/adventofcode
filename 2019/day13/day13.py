#!/usr/bin/python
# coding: utf-8

import copy
from collections import namedtuple

TILE_EMPTY  = 0
TILE_WALL   = 1
TILE_BLOCK  = 2
TILE_PADDLE = 3
TILE_BALL   = 4

SPRITES = [' ', '|', '█', '▂', 'o']

COORD_SCORE = (-1, 0)

MEMORY_QUARTERS = 0
FREE_PLAY_CHEAT_CODE = 2

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

        # Day 13-specific attributes
        self.x_ball = None
        self.x_paddle = None
        self.score = 0
        self.screen = {}

        for x in range(50):
            for y in range(25):
                self.screen[(x, y)] = TILE_EMPTY

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
        print "Score: {0}".format(self.score)
        for y in range(25):
            row = ""
            for x in range(50):
                row += SPRITES[self.screen[(x, y)]]
            print row

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
                if self.x_ball < self.x_paddle:
                    correction = -1
                elif self.x_ball > self.x_paddle:
                    correction = 1
                else:
                    correction = 0
                self.write(param1.address, correction)
                self.print_screen()

            elif self.OPCODE_OUTPUT == opcode:
                self.output.append(param1.value)
                if 3 == len(self.output):
                    coord = (self.output[0], self.output[1])
                    tile = self.output[2]
                    if TILE_PADDLE == tile:
                        self.x_paddle = coord[0]
                    elif TILE_BALL == tile:
                        self.x_ball = coord[0]

                    if COORD_SCORE == coord:
                        self.score = self.output[2]
                    else:
                        self.screen[coord] = self.output[2]
                    self.output = []
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

        #print "halt @ PC {0} ({1})".format(self.pc, self.read(self.pc))
        self.print_screen()

# Open input file
filename = "day13.txt"
f = open(filename, "r")

with open(filename, "r") as f:
    for line in f:
        i = 0
        program = {}
        for item in line.strip().split(","):
            program[i] = int(item)
            i += 1

        node = IntcodeNode(program)
        node.program[MEMORY_QUARTERS] = FREE_PLAY_CHEAT_CODE
        node.execute()
