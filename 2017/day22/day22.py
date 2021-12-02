#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dictionaries that know how to change velocity left or right
left_turn = { (1, 0) : (0, -1),
              (0, 1) : (1, 0),
              (-1, 0): (0, 1),
              (0, -1): (-1, 0)}


right_turn = { (1, 0) : (0, 1),
               (0, 1) : (-1, 0),
               (-1, 0): (0, -1),
               (0, -1): (1, 0)}

NODE_INFECTED = '#'
NODE_CLEAN = '.'
NODE_WEAKENED = 'W'
NODE_FLAGGED = 'F'

ITERATION_COUNT_PART_ONE = 10000
ITERATION_COUNT_PART_TWO = 10000000

# Parse the map file
with open('day22_input.txt') as f:
    node_map = [line.rstrip('\n') for line in f]

infected_nodes = {}
for y in range(len(node_map)):
    for x in range(len(node_map[y])):
        if node_map[y][x] == NODE_INFECTED: infected_nodes[(x, y)] = NODE_INFECTED

# The virus carrier begins in the middle of the map facing up.
height = len(node_map)
width = len(node_map[0])
pos = (width / 2, height / 2)
vel = (0, -1)

# The following steps are all executed in order one time each burst:
#
# If the current node is infected, it turns to its right. Otherwise, it turns to its left.
# (Turning is done in-place; the current node does not change.)
#
# If the current node is clean, it becomes infected. Otherwise, it becomes cleaned.
# (This is done after the node is considered for the purposes of changing direction.)
#
# The virus carrier moves forward one node in the direction it is facing.
infection_count = 0
for burst in range(ITERATION_COUNT_PART_ONE):
    if pos in infected_nodes:
        vel = right_turn[vel]
        del infected_nodes[pos]
    else:
        vel = left_turn[vel]
        infected_nodes[pos] = NODE_INFECTED
        infection_count += 1

    pos = (pos[0] + vel[0], pos[1] + vel[1])

print 'Part One: {0} bursts cause a node to become infected.'.format(infection_count)

nodes = {}
for y in range(len(node_map)):
    for x in range(len(node_map[y])):
        nodes[(x, y)] = node_map[y][x]

# The virus carrier begins in the middle of the map facing up.
height = len(node_map)
width = len(node_map[0])
pos = (width / 2, height / 2)
vel = (0, -1)

# The virus carrier still functions in a similar way, but now uses the following logic during its bursts of action:
#
# Decide which way to turn based on the current node:
# If it is clean, it turns left.
# If it is weakened, it does not turn, and will continue moving in the same direction.
# If it is infected, it turns right.
# If it is flagged, it reverses direction, and will go back the way it came.
#
# Modify the state of the current node, as described above:
# Clean nodes become weakened.
# Weakened nodes become infected.
# Infected nodes become flagged.
# Flagged nodes become clean.
#
# The virus carrier moves forward one node in the direction it is facing.
infection_count = 0
for burst in range(ITERATION_COUNT_PART_TWO):
    status = nodes.get(pos, NODE_CLEAN)
    if status == NODE_CLEAN:
        vel = left_turn[vel]
        status = NODE_WEAKENED
    elif status == NODE_WEAKENED:
        infection_count += 1
        status = NODE_INFECTED
    elif status == NODE_INFECTED:
        vel = right_turn[vel]
        status = NODE_FLAGGED
    elif status == NODE_FLAGGED:
        vel = left_turn[left_turn[vel]]
        status = NODE_CLEAN

    nodes[pos] = status
    pos = (pos[0] + vel[0], pos[1] + vel[1])

print 'Part Two: {0} bursts cause a node to become infected.'.format(infection_count)