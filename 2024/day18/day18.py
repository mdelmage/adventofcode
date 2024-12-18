#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Your memory space is a two-dimensional grid with coordinates that range from 0 to 70
# both horizontally and vertically.
SIZE = 71

# As bytes fall into your memory space, they make that coordinate corrupted.
SAFE = '.'
CORRUPTED = '#'

# You and The Historians are currently in the top left corner of the memory space
# (at 0,0) and need to reach the exit in the bottom right corner.
START = (0, 0)
EXIT = (SIZE - 1, SIZE - 1)

# List of the 4 possible neighbor positions.
NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def traverse(falling_bytes):
    # Set up the (clean) memory space.
    memory = {}
    for col in range(SIZE):
        for row in range(SIZE):
            memory[(col, row)] = SAFE

    # As bytes fall into your memory space, they make that coordinate corrupted.
    # Corrupted memory coordinates cannot be entered by you or The Historians,
    # so you'll need to plan your route carefully.
    for falling_byte in falling_bytes:
        memory[falling_byte] = CORRUPTED


    # Explore the corrupted space via flood-fill. Return the number of steps it took
    # to reach the exit, or None if we couldn't reach it at all.
    step = 0
    path = set([START])
    memory[START] = step
    while len(path) > 0:
        step += 1
        path_next = set()
        for cell in [(p[0] + n[0], p[1] + n[1]) for p in path for n in NEIGHBORS]:
            if memory.get(cell, CORRUPTED) == SAFE: path_next.add(cell)
        for p in path_next: memory[p] = step
        path = path_next

    if memory[EXIT] == SAFE:
        # Couldn't reach the exit, we never marked it.
        return None
    else:
        # The exit space will contain the number of steps it took to reach.
        return memory[EXIT]

# Parse the list of which bytes will fall.
with open('day18_input.txt') as f:
    falling_bytes = [tuple([int(n) for n in line.rstrip('\n').split(',')]) for line in f]

# Simulate the first kilobyte (1024 bytes) falling onto your memory space.#
# Afterward, what is the minimum number of steps needed to reach the exit?
num_bytes = 1024
print('Part One: The minimum number of steps needed to reach the exit is {0}.'.format(traverse(falling_bytes[:num_bytes])))

# The Historians aren't as used to moving around in this pixelated universe as you are.
# You're afraid they're not going to be fast enough to make it to the exit before the path is completely blocked.
#
# To determine how fast everyone needs to go, you need to determine the first byte that will cut off
# the path to the exit.
#
# Simulate more of the bytes that are about to corrupt your memory space.
while traverse(falling_bytes[:num_bytes]) is not None:
    num_bytes += 1
failing_byte = falling_bytes[num_bytes - 1]

# What are the coordinates of the first byte that will prevent the exit from being reachable
# from your starting position?
print('Part Two: The first byte that will prevent the exit from being reachable is {0}.'.format(failing_byte))