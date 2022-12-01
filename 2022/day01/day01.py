#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the food Calories list file
with open('day01_input.txt') as f:
    calories = [line.rstrip('\n') for line in f]

# The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations, etc.
# that they've brought with them, one item per line. Each Elf separates their own inventory from the previous
# Elf's inventory (if any) by a blank line.
elves = [0]
for c in calories:
    if len(c) > 0:
        elves[-1] += int(c)
    else:
        elves.append(0)

# Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
elves = sorted(elves, reverse=True)
print('Part One: Elf with the most Calories has {0}.'.format(elves[0]))

# Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
print('Part Two: The top three Elves are carrying {0} Calories.'.format(elves[0] + elves[1] + elves[2]))
