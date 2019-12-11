#!/usr/bin/python

OPCODE_ADD      = 1
OPCODE_MULTIPLY = 2
OPCODE_HALT     = 99

PC_ADVANCE      = 4
TARGET          = 19690720

# Open input file
filename = "day02.txt"
f = open(filename, "r")

with open(filename, "r") as f:
    for line in f:
        for noun in range(100):
            for verb in range(100):
                mem = list(map(int, line.strip().split(",")))
                pc = 0

                # Inject noun and verb into program
                mem[1] = noun
                mem[2] = verb

                while mem[pc] != OPCODE_HALT:
                    if mem[pc] == OPCODE_ADD:
                        mem[mem[pc + 3]] = mem[mem[pc + 1]] + mem[mem[pc + 2]]
                    elif mem[pc] == OPCODE_MULTIPLY:
                        mem[mem[pc + 3]] = mem[mem[pc + 1]] * mem[mem[pc + 2]]
                    else:
                        print "Unknown opcode {0} @ PC {1}!".format(mem[pc], pc)
                        break

                    pc += PC_ADVANCE

                if mem[0] == TARGET:
                    print "Noun: {0} Verb: {1}".format(noun, verb)
                    print "100 * noun + verb = {0}".format(100 * noun + verb)
                    exit