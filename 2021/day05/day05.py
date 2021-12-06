#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the hydrothermal vents file
with open('day05_input.txt') as f:
	vents = [line.rstrip('\n').split(' -> ') for line in f]

vent_map = {}
vent_map_diag = {}
for vent in vents:
	start = [int(x) for x in vent[0].split(',')]
	end = [int(x) for x in vent[1].split(',')]
	if start[1] == end[1]:
		# Horizontal
		x_start = min(start[0], end[0])
		x_end = max(start[0], end[0])
		y  = start[1]
		for x in range(x_start, x_end + 1):
			vent_map[(x, y)] = vent_map.get((x, y), 0) + 1
	elif start[0] == end[0]:
		# Vertical
		y_start = min(start[1], end[1])
		y_end = max(start[1], end[1])
		x  = start[0]
		for y in range(y_start, y_end + 1):
			vent_map[(x, y)] = vent_map.get((x, y), 0) + 1
	else:
		# Diagonal
		if start[0] < end[0]:
			x_inc = 1
		else:
			x_inc = -1

		if start[1] < end[1]:
			y_inc = 1
		else:
			y_inc = -1

		x = start[0]
		y = start[1]

		for i in range(abs(start[0] - end[0]) + 1):
			vent_map_diag[(x, y)] = vent_map_diag.get((x, y), 0) + 1
			x += x_inc
			y += y_inc

collisions = 0
for coord in vent_map:
	if vent_map[coord] > 1: collisions += 1
print('Part One: {0} points have at least two overlapping lines.'.format(collisions))

# Now overlay the diagonal vents onto the main map.
for coord in vent_map_diag:
	vent_map[coord] = vent_map.get(coord, 0) + vent_map_diag[coord]

collisions = 0
for coord in vent_map:
	if vent_map[coord] > 1: collisions += 1
print('Part Two: {0} points have at least two overlapping lines after including diagonals.'.format(collisions))