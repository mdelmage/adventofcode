#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the piloting commands file
with open('day02_input.txt') as f:
	commands = [line.rstrip('\n').split() for line in f]

# Your horizontal position and depth both start at 0.
depth = 0
h_pos = 0

# It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:
#
# forward X increases the horizontal position by X units.
# down X increases the depth by X units.
# up X decreases the depth by X units.
for c in commands:
	command = c[0]
	value = int(c[1])

	if command == 'forward':
		h_pos += value
	elif command == 'up':
		depth -= value
	elif command == 'down':
		depth += value

print('Part One: product of final horizontal position and final depth is {0}.'.format(depth * h_pos))

# In addition to horizontal position and depth, you'll also need to track a third value, aim,
# which also starts at 0. The commands also mean something entirely different than you first thought:
#
# down X increases your aim by X units.
# up X decreases your aim by X units.
# forward X does two things:
#   - It increases your horizontal position by X units.
#   - It increases your depth by your aim multiplied by X.
depth = 0
h_pos = 0
aim = 0

for c in commands:
	command = c[0]
	value = int(c[1])

	if command == 'forward':
		h_pos += value
		depth += aim * value
	elif command == 'up':
		aim -= value
	elif command == 'down':
		aim += value

print('Part Two: product of final horizontal position and final depth is {0}.'.format(depth * h_pos))