#!/usr/bin/env python
# -*- coding: utf-8 -*-

NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# He gives you an up-to-date map (your puzzle input) of
# his starting position (S), garden plots (.), and rocks (#).
START = 'S'
PLOT  = '.'
ROCK  = '#'

# Parse the garden map.
with open('day21_input.txt') as f:
    rows = [line.rstrip('\n') for line in f]

    garden = {}
    for row in range(len(rows)):
        for col in range(len(rows[0])):
            tile = rows[row][col]
            if tile == START:
                start = (col, row)
                garden[(col, row)] = PLOT
            else:
                garden[(col, row)] = tile

traversal = {0: set([start])}
for step in range(1, 64 + 1):
    traversal[step] = set()
    for pos in traversal[step - 1]:
        for n in NEIGHBORS:
            pos_next = (pos[0] + n[0], pos[1] + n[1])
            if pos_next in garden and garden[pos_next] == PLOT: traversal[step].add(pos_next)

# Starting from the garden plot marked S on your map, how many garden plots
# could the Elf reach in exactly 64 steps?
print('Part One: Number of garden plots reachable in exactly 64 steps is {0}.'.format(len(traversal[64])))