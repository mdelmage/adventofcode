#!/usr/bin/env python
# -*- coding: utf-8 -*-

def partial_overlap(range1, range2):
    return range2[0] <= range1[1] and range2[0] >= range1[0] and range2[1] > range1[1]

def full_overlap(range1, range2):
    return range2[0] <= range1[0] and range2[1] >= range1[1]

# Parse the ingredients database
with open('day05_input.txt') as f:
    ingredients = [line.rstrip('\n') for line in f]
    split = ingredients.index('')
    fresh_ingredients = [(int(x), int(y)) for (x, y) in [x.split('-') for x in ingredients[:split]]]
    available_ingredients = [int(x) for x in ingredients[split + 1:]]

# The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5
# are all fresh. The ranges can also overlap; an ingredient ID is fresh if it is in any range.
#
#The Elves are trying to determine which of the available ingredient IDs are fresh.
fresh_count = 0
for i in available_ingredients:
    for start, end in fresh_ingredients:
        if i >= start and i <= end:
            fresh_count += 1
            break

# So that they can stop bugging you when they get new inventory, the Elves would like to know
# all of the IDs that the fresh ingredient ID ranges consider to be fresh. An ingredient ID
# is still considered fresh if it is in any range.
done = False
while not done:
    done = True
    # Iterate through all combinations of ranges and see if there are overlaps to consolidate.
    for i, j in [(i, j) for i in range(len(fresh_ingredients)) for j in range(len(fresh_ingredients)) if i != j]:
        range1 = fresh_ingredients[i]
        range2 = fresh_ingredients[j]
        if partial_overlap(range1, range2):
            # Range 2 partially overlaps ("extends") Range 1. Join them.
            fresh_ingredients[i] = (range1[0], range2[1])
            fresh_ingredients = fresh_ingredients[:j] + fresh_ingredients[j + 1:]
            done = False
            break
        elif full_overlap(range1, range2):
            # Range 2 fully overlaps (is a superset of) Range 1. Join them.
            fresh_ingredients[i] = (range2[0], range2[1])
            fresh_ingredients = fresh_ingredients[:j] + fresh_ingredients[j + 1:]
            done = False
            break            

# Add up the size of all ranges.
total_fresh_ingredients = sum([j - i + 1 for (i, j) in fresh_ingredients])

# Process the database file from the new inventory management system.
# How many of the available ingredient IDs are fresh?
print('Part One: {0} of the available ingredient IDs are fresh.'.format(fresh_count))

# Process the database file again. How many ingredient IDs are considered to be fresh
# according to the fresh ingredient ID ranges?
print('Part Two: {0} total ingredient IDs are fresh.'.format(total_fresh_ingredients))