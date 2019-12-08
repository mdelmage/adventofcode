#!/usr/bin/python

OPCODE_ADD      = 1
OPCODE_MULTIPLY = 2
OPCODE_INPUT    = 3
OPCODE_OUTPUT   = 4
OPCODE_HALT     = 99

opcode_lengths = { 1:  4,
                   2:  4,
                   3:  2,
                   4:  2,
                   99: 0 }

# Open input file
filename = "day5.txt"
f = open(filename, "r")

with open(filename, "r") as f:
    for line in f:
        mem = list(map(int, line.strip().split(",")))
        pc = 0

        while mem[pc] != OPCODE_HALT:
            opcode = mem[pc] % 100
            param1_mode = (mem[pc] / 100) % 10
            param2_mode = (mem[pc] / 1000) % 10
            param3_mode = (mem[pc] / 10000) % 10

            if opcode == OPCODE_ADD:
                param1 =  mem[pc + 1] if param1_mode == 1 else mem[mem[pc + 1]]
                param2 =  mem[pc + 2] if param2_mode == 1 else mem[mem[pc + 2]]
                param3 =  mem[pc + 3]
                mem[param3] = param1 + param2
            elif opcode == OPCODE_MULTIPLY:
                param1 =  mem[pc + 1] if param1_mode == 1 else mem[mem[pc + 1]]
                param2 =  mem[pc + 2] if param2_mode == 1 else mem[mem[pc + 2]]
                param3 =  mem[pc + 3]
                mem[param3] = param1 * param2
            elif opcode == OPCODE_INPUT:
                param1 =  mem[pc + 1]
                mem[param1] = input("Input: ")
            elif opcode == OPCODE_OUTPUT:
                param1 =  mem[pc + 1]
                print "Output: {0}".format(mem[param1])
            else:
                print "Unknown opcode {0} @ PC {1}!".format(opcode, pc)
                break

            pc += opcode_lengths[opcode]
