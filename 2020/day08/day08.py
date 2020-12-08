#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# Parse the program and save each line
with open('day08_input.txt') as f:
    program_listing = [line.rstrip('\n') for line in f]

program = []
for line in program_listing:
    # The boot code is represented as a text file with one instruction per line of text. Each instruction
    # consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).
    tokens = line.split()
    op = tokens[0]
    val = int(tokens[1])
    program.append((op, val))

accumulator = 0
ip = 0
previous_ip = set()

# Run your copy of the boot code. Immediately before any instruction is executed
# a second time, what value is in the accumulator?
while ip not in previous_ip:
    # Record the instruction we're about to execute
    previous_ip.add(ip)

    # This ALU only knows two instructions, acc and jmp
    (op, val) = program[ip]
    if op == 'acc': accumulator += val
    elif op == 'jmp': ip += val - 1

    # Increment instruction pointer
    ip += 1

print 'Part One: value in accumulator at start of second loop is {0}.'.format(accumulator)

# Fix the program so that it terminates normally by changing exactly one jmp (to nop)
# or nop (to jmp). What is the value of the accumulator after the program terminates?
for modified_ip in range(len(program)):
    accumulator = 0
    ip = 0
    previous_ip = set()

    while ip not in previous_ip:
        # Record the instruction we're about to execute
        previous_ip.add(ip)

        (op, val) = program[ip]

        # Modify the selected instruction, if we're about to execute it
        if ip == modified_ip:
            if op == 'jmp': op = 'nop'
            elif op == 'nop': op = 'jmp'
    
        # This ALU only knows two instructions, acc and jmp
        if op == 'acc': accumulator += val
        if op == 'jmp': ip += val - 1

        # Increment instruction pointer
        ip += 1
        if ip >= len(program):
            print 'Part Two: value in accumulator after the program terminates is {0}.'.format(accumulator)
            sys.exit()