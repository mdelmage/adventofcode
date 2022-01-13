#!/usr/bin/env python
# -*- coding: utf-8 -*-


def taxi_distance(pos):
    return abs(pos[0]) + abs(pos[1])


NORTH = 0
EAST  = 1
SOUTH = 2
WEST  = 3

# Describe how to take one step in the direction we're currently facing.
# To turn left, index one backward.
# To turn right, index one forward.
# The list starts with North.
DIRECTIONS = { NORTH: ( 0,  1),
               EAST:  ( 1,  0),
               SOUTH: ( 0, -1),
               WEST:  (-1,  0)}

# The Document indicates that you should start at the given coordinates
# (where you just landed) and face North.
facing = NORTH
pos = (0, 0)

# Remember where we've walked, and where Easter Bunny HQ actually is.
history = set()
hq = None

# Parse the Easter Bunny Recruiting Document
with open('day01_input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

for line in lines:
    dirs = line.split(', ')
    for d in dirs:
        # Turn the way the directions say.
        if d[0] == 'R':
            facing = (facing + 1) % len(DIRECTIONS)
        else:
            facing = (facing - 1) % len(DIRECTIONS)

        # Figure out which way we're going, and how far.
        distance = int(d[1:])
        delta = DIRECTIONS[facing]

        # Take each step one by one.
        # If we just take the steps in bulk, we may miss a previous location we've visited
        # if we cross our path at some in-between location.
        for step in range(distance):
            pos = (pos[0] + delta[0], pos[1] + delta[1])

            # Record where we are, and check if we've been there before.
            if pos in history and hq is None: hq = pos
            history.add(pos)

print('Part One: Easter Bunny HQ is {0} blocks away.'.format(taxi_distance(pos)))
print('Part Two: Easter Bunny HQ is actually {0} blocks away.'.format(taxi_distance(hq)))
