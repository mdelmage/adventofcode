#!/usr/bin/python

OPCODE_ADD      = 1
OPCODE_MULTIPLY = 2
OPCODE_HALT     = 99

# Open input file
filename = "day2.txt"
f = open(filename, "r")

with open(filename, "r") as f:
    for line in f:
        mem = [int(i) for i in line.strip().split(",")] 
        pc = 0

        # Fix 1202 Program Alarm
        mem[1] = 12
        mem[2] = 2

        while mem[pc] != OPCODE_HALT:
            if mem[pc] == OPCODE_ADD:
                mem[mem[pc + 3]] = mem[mem[pc + 1]] + mem[mem[pc + 2]]
            elif mem[pc] == OPCODE_MULTIPLY:
                mem[mem[pc + 3]] = mem[mem[pc + 1]] * mem[mem[pc + 2]]
            else:
                print "Unknown opcode {0} @ PC {1}!".format(mem[pc], pc)
                break

            pc += 4

        print mem