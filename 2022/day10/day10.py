#!/usr/bin/env python
# -*- coding: utf-8 -*-

# You count the pixels on the CRT: 40 wide and 6 high.
CRT_WIDTH = 40
CRT_HEIGHT = 6

# For now, consider the signal strength (the cycle number multiplied
# by the value of the X register) during the 20th cycle and every
# 40 cycles after that (that is, during the 20th, 60th, 100th, 140th,
# 180th, and 220th cycles).
SIGNAL_STRENGTH_CYCLES = [20, 60, 100, 140, 180, 220]

# Parse the program file
with open('day10_input.txt') as f:
    program = [line.rstrip('\n') for line in f]

# The CPU has a single register, X, which starts with the value 1.
pc = 0
x = 1

strength = 0
crt = []

for line in program:
    if line == 'noop':
        # noop takes one cycle to complete. It has no other effect.
        cycles_remaining = 1
        pending_write = x
    else:
        # addx V takes two cycles to complete. After two cycles,
        # the X register is increased by the value V. (V can be negative.)
        cycles_remaining = 2
        pending_write = x + int(line.split(' ')[1])

    while cycles_remaining > 0:
        if abs((pc % 40) - x) <= 1:
            crt.append('█')
        else:
            crt.append(' ')

        pc += 1
        cycles_remaining -= 1

        # Find the signal strength during the 20th, 60th, 100th, 140th,
        # 180th, and 220th cycles. What is the sum of these six signal strengths?
        if pc in SIGNAL_STRENGTH_CYCLES: strength += (pc * x)

    x = pending_write


print('Part One: Sum of the six signal strengths is {0}.'.format(strength))

print('Part Two: CRT renders:')
for row in range(6):
    line = ''
    for col in range(40):
        line += crt[row*40 + col]
    print(line)