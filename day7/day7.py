#!/usr/bin/python

from itertools import permutations 

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

class IntcodeNode:
    def __init__(self, program):
        self.program = program
        self.pc = 0

    def execute(self, argv):
        mem = self.program #copy.deepcopy(self.program)
        pc = self.pc
        result = 0
        argc = 0

        while mem[pc] != OPCODE_HALT:
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

            if opcode == OPCODE_ADD:
                mem[param3] = param1 + param2
            elif opcode == OPCODE_MULTIPLY:
                mem[param3] = param1 * param2
            elif opcode == OPCODE_INPUT:
                param1 = mem[pc + 1]
                mem[param1] = argv[argc]
                argc += 1
            elif opcode == OPCODE_OUTPUT:
                result = param1
            elif opcode == OPCODE_JIT:
                pc = param2 if param1 != 0 else pc + 3
            elif opcode == OPCODE_JIF:
                pc = param2 if param1 == 0 else pc + 3
            elif opcode == OPCODE_LT:
                mem[param3] = 1 if param1 < param2 else 0
            elif opcode == OPCODE_EQ:
                mem[param3] = 1 if param1 == param2 else 0
            else:
                print "Unknown opcode {0} @ PC {1}!".format(opcode, pc)
                break

            pc += opcode_lengths[opcode]

        return result

# Open input file
filename = "day7.txt"
f = open(filename, "r")


with open(filename, "r") as f:
    for line in f:
        program = list(map(int, line.strip().split(",")))

        max_thrust = 0
        max_phase = None
        phases = permutations([0, 1, 2, 3, 4])

        for phase in list(phases):
            result = 0
            # 5-stage pipeline
            for i in range(5):
                node = IntcodeNode(program)
                result = node.execute((phase[i], result))
            if result > max_thrust:
                max_thrust = result
                max_phase = phase
            
        print "Max thruster signal is {0} (from phase settings {1}".format(max_thrust, max_phase)
        