#!/usr/bin/python

import copy
from collections import namedtuple

COLOR_BLACK = 0
COLOR_WHITE = 1

SYMBOL_BLACK = '.'
SYMBOL_WHITE = '#'

STATE_PAINT = 0
STATE_TURN  = 1

TURN_LEFT  = 0
TURN_RIGHT = 1

# Up, Right, Down, Left
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

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

    opcode_lengths = { 1:  4,
                       2:  4,
                       3:  2,
                       4:  2,
                       5:  0,
                       6:  0,
                       7:  4,
                       8:  4,
                       9:  2,
                       99: 0 }

    location = (0, 0)
    direction = 0
    panel = {}

    def __init__(self, program):
        self.program = copy.deepcopy(program)
        self.relative_base = 0
        self.state = STATE_PAINT
        self.pc = 0
        self.panel[self.location] = COLOR_WHITE

    def read(self, address):
        if address in self.program:
            return self.program[address]
        else:
            return 0

    def write(self, address, value):
        self.program[address] = value
 
    def current_color(self):
        if self.location not in self.panel or COLOR_BLACK == self.panel[self.location]:
            return COLOR_BLACK
        else:
            return COLOR_WHITE
    
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
                self.write(param1.address, self.current_color())
            elif self.OPCODE_OUTPUT == opcode:
                if STATE_PAINT == self.state:
                    self.panel[self.location] = param1.value
                elif STATE_TURN == self.state:
                    if TURN_LEFT == param1.value:
                        self.direction = (self.direction - 1) % len(directions)
                    elif TURN_RIGHT == param1.value:
                        self.direction = (self.direction + 1) % len(directions)
                    else:
                        print "Unknown direction {0}!".format(param1.value)
                        return
                    self.location = (self.location[0] + directions[self.direction][0], self.location[1] + directions[self.direction][1])
                else:
                    print "Unknown state {0}!".format(self.state)
                    return
                self.state ^= 1
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


# Open input file
filename = "day11.txt"
f = open(filename, "r")

with open(filename, "r") as f:
    for line in f:
        i = 0
        program = {}
        for item in line.strip().split(","):
            program[i] = int(item)
            i += 1

        node = IntcodeNode(program)
        node.execute()

        for y in range(-5, 10):
            for x in range(0, 50):
                if node.location[0] == x and node.location[1] == y:
                    print "^",
                elif (x, y) in node.panel and COLOR_WHITE == node.panel[(x, y)]:
                    print SYMBOL_WHITE,
                else:
                    print SYMBOL_BLACK,
            print ""
        print "Robot has painted {0} total unique panels.".format(len(node.panel))