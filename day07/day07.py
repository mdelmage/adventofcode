#!/usr/bin/python

from itertools import permutations 
import copy

class IntcodeNode:
    OPCODE_ADD      = 1
    OPCODE_MULTIPLY = 2
    OPCODE_INPUT    = 3
    OPCODE_OUTPUT   = 4
    OPCODE_JIT      = 5
    OPCODE_JIF      = 6
    OPCODE_LT       = 7
    OPCODE_EQ       = 8
    OPCODE_HALT     = 99

    opcode_lengths = { 1:  4,
                       2:  4,
                       3:  2,
                       4:  2,
                       5:  0,
                       6:  0,
                       7:  4,
                       8:  4,
                       99: 0 }

    def __init__(self, program, phase):
        self.program = copy.deepcopy(program)
        self.phase = phase
        self.pc = 0

    def execute(self, input):
        mem = self.program
        pc = self.pc

        while mem[pc] != self.OPCODE_HALT:
            opcode = mem[pc] % 100
            param1_mode = (mem[pc] / 100) % 10
            param2_mode = (mem[pc] / 1000) % 10
            param3_mode = (mem[pc] / 10000) % 10

            # Use exceptions to simplify command processing.
            # Shorter opcodes may dereference invalid memory
            # when calculating extra params.
            try:
                param1 = mem[pc + 1] if param1_mode == 1 else mem[mem[pc + 1]]
                param2 = mem[pc + 2] if param2_mode == 1 else mem[mem[pc + 2]]
                param3 = mem[pc + 3]
            except:
                pass

            if opcode == self.OPCODE_ADD:
                mem[param3] = param1 + param2
            elif opcode == self.OPCODE_MULTIPLY:
                mem[param3] = param1 * param2
            elif opcode == self.OPCODE_INPUT:
                param1 = mem[pc + 1]
                if self.phase:
                    mem[param1] = self.phase
                    self.phase = None
                else:
                    mem[param1] = input
            elif opcode == self.OPCODE_OUTPUT:
                self.pc = pc + self.opcode_lengths[opcode]
                return (param1, False)
            elif opcode == self.OPCODE_JIT:
                pc = param2 if param1 != 0 else pc + 3
            elif opcode == self.OPCODE_JIF:
                pc = param2 if param1 == 0 else pc + 3
            elif opcode == self.OPCODE_LT:
                mem[param3] = 1 if param1 < param2 else 0
            elif opcode == self.OPCODE_EQ:
                mem[param3] = 1 if param1 == param2 else 0
            else:
                print "Unknown opcode {0} @ PC {1}!".format(opcode, pc)
                break

            pc += self.opcode_lengths[opcode]

        return (0, True)

# Open input file
filename = "day07.txt"
f = open(filename, "r")

with open(filename, "r") as f:
    for line in f:
        program = list(map(int, line.strip().split(",")))

        max_thrust = 0
        max_phase = None
        phases = permutations([5, 6, 7, 8, 9])

        for phase in list(phases):
            nodes = []
            result = 0
            thrust = 0
            done = False
            # 5-stage pipeline
            for i in range(5):
                nodes.append(IntcodeNode(program, phase[i]))

            i = 0
            while not done:
                result, done = nodes[i % len(nodes)].execute(result)
                if (len(nodes) - 1 == i % len(nodes)) and not done: thrust = result
                i += 1

            if thrust > max_thrust:
                max_thrust = thrust
                max_phase = phase
            
        print "Max thruster signal is {0} (from phase settings {1})".format(max_thrust, max_phase)
        