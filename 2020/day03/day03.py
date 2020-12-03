#!/usr/bin/env python
# -*- coding: utf-8 -*-

# You make a map (your puzzle input) of the open squares (.)
# and trees (#) you can see.
TREE = '#'
OPEN = '.'

def run_slope(s):
    pos_x = 0
    pos_y = 0
    trees_encountered = 0
    while pos_y < len(treemap):
        if treemap[pos_y][pos_x] == TREE:
            trees_encountered += 1

        pos_x = (pos_x + s[0]) % len(treemap[0])
        pos_y += s[1]

    return trees_encountered

# Parse the tree map and save each line
with open('day03_input.txt') as f:
    treemap = [line.rstrip('\n') for line in f]

# The toboggan can only follow a few specific slopes
# (you opted for a cheaper model that prefers rational numbers);
# start by counting all the trees you would encounter for the
# slope right 3, down 1
SLOPE = (3, 1)

# From your starting position at the top-left, check the position
# that is right 3 and down 1. Then, check the position that is
# right 3 and down 1 from there, and so on until you go past the
# bottom of the map.

print 'Part One: %d trees encountered.' % run_slope(SLOPE)

# Time to check the rest of the slopes - you need to minimize
# the probability of a sudden arboreal stop, after all.
#
# Determine the number of trees you would encounter if, for
# each of the following slopes, you start at the top-left
# corner and traverse the map all the way to the bottom:
#
# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.
SLOPES = [(1, 1),
          (3, 1),
          (5, 1),
          (7, 1),
          (1, 2)]

trees_product = 1
for s in SLOPES:
    trees_product *= run_slope(s)

print 'Part Two: %d trees encountered.' % trees_product