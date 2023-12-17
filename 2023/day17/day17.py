#!/usr/bin/env python
# -*- coding: utf-8 -*-

LEFT  = (-1,  0)
RIGHT = ( 1,  0)
UP    = ( 0, -1)
DOWN  = ( 0,  1)
DIRS = [LEFT, RIGHT, UP, DOWN]

# Poor man's INT_MAX
BIG_NUM = 10 ** 100

# Find the minimum heat loss by searching the map with minimum and maximum traversal lengths specified.
def search_map(t_min, t_max):
    search = {(start, RIGHT): 0, (start, DOWN): 0}
    loss_map = {}
    least_heatloss = BIG_NUM

    # Pathfinding! Perform a step-wise search of the map.
    # The rules for this puzzle mean that multiple next steps are possible for any given step,
    # so remember if we've been here before to avoid extra processing or infinite loops.
    # Include the direction we're facing in the history we remember.
    while len(search) > 0:
        search_next = {}
        for d, t, pos, facing in [(d, t, p, f) for d in DIRS for t in range(t_min, t_max + 1) for (p, f) in search]:
            # Current status: position, direction we're facing
            # New potential places to explore: new direction(s), travel length
            state = (pos, facing)

            # The crucible also can't reverse direction; after entering each city block, it may only turn left,
            # continue straight, or turn right.
            if abs(d[0]) != abs(facing[0]):
                loss = search[state]
                pos_next = (pos[0] + (t * d[0]), pos[1] + (t * d[1]))
                state_next = (pos_next, d)

                if pos_next in heatmap:
                    # Quick-and-dirty way to calculate the heat loss by traveling to the next position:
                    # just traverse tiles one-by-one until we're at the final position, adding loss
                    # along the way.
                    while pos != pos_next:
                        pos = (pos[0] + d[0], pos[1] + d[1])
                        loss += heatmap.get(pos, 0)

                    if pos_next == dest:
                        # We've arrived at the bottom-right; did we improve?
                        least_heatloss = min(least_heatloss, loss)
                    elif state_next not in loss_map or loss < loss_map[state_next]:
                        # We found a new area to explore, add it to the next round!
                        loss_map[state_next] = loss
                        search_next[state_next] = min(search_next.get(state_next, BIG_NUM), loss)

        search = search_next

    return least_heatloss

# Parse the heat loss map.
with open('day17_input.txt') as f:
    h = [line.rstrip('\n') for line in f]
    size_h = len(h[0])
    size_v = len(h)

    # Each city block is marked by a single digit that represents the amount
    # of heat loss if the crucible enters that block.
    heatmap = {}
    for row in range(len(h)):
        for col in range(len(h[0])):
            heatmap[(col, row)] = int(h[row][col])

# The starting point, the lava pool, is the top-left city block;
# the destination, the machine parts factory, is the bottom-right city block.
start = (0, 0)
dest = (size_h - 1, size_v - 1)

# Directing the crucible from the lava pool to the machine parts factory, but not moving
# more than three consecutive blocks in the same direction, what is the least heat loss it can incur?
print('Part One: Least heat loss incurred with a crucible is {0}.'.format(search_map(1, 3)))

# Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have trouble
# going in a straight line, but they also have trouble turning!
#
# Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks
# in that direction before it can turn (or even before it can stop at the end). However, it will
# eventually start to get wobbly: an ultra crucible can move a maximum of ten consecutive blocks
# without turning.
#
# Directing the ultra crucible from the lava pool to the machine parts factory, what is the least
# heat loss it can incur?
print('Part Two: Least heat loss incurred with an ultra crucible is {0}.'.format(search_map(4, 10)))