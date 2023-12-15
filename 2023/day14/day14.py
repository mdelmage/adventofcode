#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The rounded rocks (O) will roll when the platform is tilted,
# while the cube-shaped rocks (#) will stay in place.
# You note the positions of all of the empty spaces (.) and rocks
# (your puzzle input).
SPACE        = '.'
CUBE_ROCK    = '#'
ROUNDED_ROCK = 'O'

NORTH = (0, -1)
SOUTH = (0,  1)
WEST  = (-1, 0)
EAST  = ( 1, 0)

# Roll all the rounded rocks as far as they will go in one direction.
def roll(r, d):
    rocks_rolled = True
    while rocks_rolled:
        rocks_rolled = False
        for (x, y) in [loc for loc in r if r[loc] == ROUNDED_ROCK]:
            # Calculate the potential next position n.
            n = (x + d[0], y + d[1])

            # If we're in bounds and there's a free space, roll the rock!
            if n[0] >= 0 and n[1] >= 0 and n[0] < size and n[1] < size and r[n] == SPACE:
                r[n] = ROUNDED_ROCK
                r[(x, y)] = SPACE
                rocks_rolled = True
    return r

# The amount of load caused by a single rounded rock (O) is equal to the number of rows
# from the rock to the south edge of the platform, including the row the rock is on.
# (Cube-shaped rocks (#) don't contribute to load.)
def load(r):
    return sum([size - y for (x, y) in r if r[(x, y)] == ROUNDED_ROCK])

# Parse the input.
with open('day14_input.txt') as f:
    r = [line.rstrip('\n') for line in f]
    size = len(r)
    rocks = {}
    for row in range(len(r)):
        for col in range(len(r[0])):
            rocks[(col, row)] = r[row][col]

# Tilt the platform so that the rounded rocks all roll north.
# Afterward, what is the total load on the north support beams?
rocks_part_one = {}
for r in rocks: rocks_part_one[r] = rocks[r]
rocks_part_one = roll(rocks_part_one, NORTH)
print('Part One: Total load on the north support beams is {0}.'.format(load(rocks_part_one)))

cycle = 0
while True:
    # Each cycle tilts the platform four times so that the rounded rocks roll north,
    # then west, then south, then east. After each tilt, the rounded rocks roll as far
    # as they can before the platform tilts in the next direction. After one cycle,
    # the platform will have finished rolling the rounded rocks in those four directions
    # in that order.
    for d in [NORTH, WEST, SOUTH, EAST]:
        rocks = roll(rocks, d)

    cycle += 1

    # By inspection: my input settles into a cycle with period 27, offset 1.
    # (The sample input has a cycle of period 7, offset 6.)
    # Instead of writing fancy cycle detection, just figure out that cycle 1000000000
    # is really cycle 1 (after some settling, about a hundred and thirty cycles).
    period = 27
    offset = 1
    settling = 150

    if cycle % period == offset and cycle > settling:
        print('Part Two: Total load on the north support beams is {0}.'.format(load(rocks)))
        break