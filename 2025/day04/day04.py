#!/usr/bin/env python
# -*- coding: utf-8 -*-

SPACE = '.'
ROLL = '@'

NEIGHBORS = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]

# Parse the paper roll map
with open('day04_input.txt') as f:
    rolls_list = [line.rstrip('\n') for line in f]

rolls = {}
for y in range(len(rolls_list)):
    for x in range(len(rolls_list[y])):
        if rolls_list[y][x] == ROLL: rolls[(x, y)] = rolls_list[y][x]

forklift_accessible_count = None
total_rolls_removed = 0
while True:
    rolls_to_remove = []
    for (x, y) in rolls:
        # Count how many neighbors are rolls. Gracefully handle edges of the map.
        adjacent_rolls = 0
        for (x_n, y_n) in NEIGHBORS:
            if rolls.get((x + x_n, y + y_n), SPACE) == ROLL: adjacent_rolls += 1

        # The forklifts can only access a roll of paper if there are fewer than four rolls of paper
        # in the eight adjacent positions. 
        if adjacent_rolls < 4: rolls_to_remove.append((x, y))

    # First time through the loop; save how many rolls were accessible for Part One.
    if not forklift_accessible_count: forklift_accessible_count = len(rolls_to_remove)

    # Remove the rolls that the forklift can access.
    for (x, y) in rolls_to_remove:
        del rolls[(x, y)]

    # Record how many rolls we removed. (Are we done?)
    total_rolls_removed += len(rolls_to_remove)
    if len(rolls_to_remove) == 0: break


# Consider your complete diagram of the paper roll locations.
# How many rolls of paper can be accessed by a forklift?
print('Part One: {0} rolls of paper are forklift-accessible.'.format(forklift_accessible_count))

# Start with your original diagram.
# How many rolls of paper in total can be removed by the Elves and their forklifts?
print('Part Two: Total rolls that can be removed is {0}.'.format(total_rolls_removed))