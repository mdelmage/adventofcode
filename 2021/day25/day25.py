#!/usr/bin/env python
# -*- coding: utf-8 -*-

FACING_EAST = '>'
FACING_SOUTH = 'v'

def move_herd(direction):
	global cucumbers

	# When a herd moves forward, every sea cucumber in the herd first simultaneously considers whether
	# there is a sea cucumber in the adjacent location it's facing (even another sea cucumber facing
	# the same direction), and then every sea cucumber facing an empty location simultaneously moves
	# into that location.
	done = True
	cucumbers_next = {}
	for pos in cucumbers:
		if cucumbers[pos] == direction:
			if direction == FACING_EAST:
				pos_next = ((pos[0] + 1) % map_size_x, pos[1])
			else:
				pos_next = (pos[0], (pos[1] + 1) % map_size_y)

			if pos_next in cucumbers:
				cucumbers_next[pos] = cucumbers[pos]
			else:
				done = False
				cucumbers_next[pos_next] = cucumbers[pos]
		else:
			cucumbers_next[pos] = cucumbers[pos]

	cucumbers = cucumbers_next
	return done

# Parse the sea cucumbers map file
with open('day25_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

cucumbers = {}
for row in range(len(lines)):
	for col in range(len(lines[row])):
		obj = lines[row][col]
		if obj == FACING_EAST or obj == FACING_SOUTH:
			cucumbers[(col, row)] = lines[row][col]

map_size_x = len(lines[0])
map_size_y = len(lines)
iterations = 0

done = False
while not done:
	done = True
	iterations += 1

	# Every step, the sea cucumbers in the east-facing herd attempt to move forward one location,
	# then the sea cucumbers in the south-facing herd attempt to move forward one location.
	done &= move_herd(FACING_EAST)
	done &= move_herd(FACING_SOUTH)

print('Part One: Done iterating after {0} steps.'.format(iterations))