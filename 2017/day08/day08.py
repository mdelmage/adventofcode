#!/usr/bin/env python
# -*- coding: utf-8 -*-

registers = {}

def execute(op, register, value, condreg, cond, condval):
    if register not in registers: registers[register] = 0
    if condreg not in registers: registers[condreg] = 0
    
    increment_value = value if op == 'inc' else -value

    condregval = registers[condreg]
    if cond == '>' : condition = (condregval >  condval)
    if cond == '<' : condition = (condregval <  condval)
    if cond == '>=': condition = (condregval >= condval)
    if cond == '<=': condition = (condregval <= condval)
    if cond == '==': condition = (condregval == condval)
    if cond == '!=': condition = (condregval != condval)

    if condition:
        registers[register] += increment_value

    return

# Parse the program and save each line
with open('day08_input.txt') as f:
    program = [line.rstrip('\n') for line in f]

max_ever_value = -1000000
for line in program:
    # Each instruction consists of several parts: the register to modify,
    # whether to increase or decrease that register's value, the amount by which
    # to increase or decrease it, and a condition. If the condition fails, skip
    # the instruction without modifying the register. The registers all start at 0.
    tokens = line.split()
    register = tokens[0]
    op       = tokens[1]
    value    = int(tokens[2])
    condreg  = tokens[4]
    cond     = tokens[5]
    condval  = int(tokens[6])

    execute(op, register, value, condreg, cond, condval)

    # To be safe, the CPU also needs to know the highest value held in any register
    # during this process so that it can decide how much memory to allocate to
    # these operations.
    max_register = max(registers, key=registers.get)
    max_value = registers[max_register]
    if max_value > max_ever_value:
        max_ever_value = max_value

max_register = max(registers, key=registers.get)
max_value = registers[max_register]
print 'Part One: Register {0} has the largest value, {1}.'.format(max_register, max_value)
print 'Part Two: the largest value ever seen was {0}.'.format(max_ever_value)