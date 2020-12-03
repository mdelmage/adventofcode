#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the jump list and save each line
with open('day05_input.txt') as f:
    jumps = [int(line.rstrip('\n')) for line in f]

ip = 0
cycle_count = 0

while ip < len(jumps):
    # ...these instructions are a little strange; after each jump,
    # the offset of that instruction increases by 1.
    jump_amount = jumps[ip]
    jumps[ip] += 1

    ip += jump_amount
    cycle_count += 1

print 'Part One: program terminated after %d cycles.' % cycle_count

# Parse the jump list and save each line
with open('day05_input.txt') as f:
    jumps = [int(line.rstrip('\n')) for line in f]

ip = 0
cycle_count = 0

while ip < len(jumps):
    # Now, the jumps are even stranger: after each jump, if the offset was three
    # or more, instead decrease it by 1. Otherwise, increase it by 1 as before.
    jump_amount = jumps[ip]
    if jumps[ip] >= 3:
        jumps[ip] -= 1
    else:
        jumps[ip] += 1

    ip += jump_amount
    cycle_count += 1

print 'Part Two: program terminated after %d cycles.' % cycle_count