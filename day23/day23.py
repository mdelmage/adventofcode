#!/usr/bin/python
# coding: utf-8

import copy
from collections import namedtuple
from queue import Queue
from __builtin__ import True

QUEUE_EMPTY = -1
NETWORK_SIZE = 50
 
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

    def __init__(self, program, address):
        self.program = copy.deepcopy(program)
        self.relative_base = 0
        self.pc = 0
        self.output = ""

        # Day 23-specific attributes
        self.address = address
        self.provisioned = False
        self.input_queue = Queue()
        self.output_queue = Queue()

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

    def execute(self):
        timeslice = 0
        while timeslice < 100 and self.read(self.pc) != self.OPCODE_HALT:
            timeslice += 1
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
                if not self.provisioned:
                    input_val = self.address
                    self.provisioned = True
                elif self.input_queue.empty():
                    input_val = QUEUE_EMPTY
                else:
                    input_val = self.input_queue.get_nowait()
                self.write(param1.address, input_val)
            elif self.OPCODE_OUTPUT == opcode:
                output_val = param1.value
                self.output_queue.put_nowait(output_val)
                if 3 == self.output_queue.qsize():
                    self.pc += self.opcode_lengths[opcode]
                    return (self.output_queue.get_nowait(),
                            self.output_queue.get_nowait(),
                            self.output_queue.get_nowait())
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
        return None

# Open input file
with open("day23.txt", "r") as f:
    for line in f:
        i = 0
        program = {}
        for item in line.strip().split(","):
            program[i] = int(item)
            i += 1

        nodes = [IntcodeNode(program, addr) for addr in range(NETWORK_SIZE)]

        i = 0
        while True:
            o = nodes[i].execute()
            if o is not None:
                if 255 == o[0]:
                    print o
                    break
                else:
                    nodes[o[0]].input_queue.put_nowait(o[1])
                    nodes[o[0]].input_queue.put_nowait(o[2])
            i = (i + 1) % NETWORK_SIZE

