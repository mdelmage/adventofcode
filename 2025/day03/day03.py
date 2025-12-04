#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For a given bank and starting position, find the best choice for the next
# battery to enable, and return that battery's position.
# If there are multiple options, return the first (e.g, leftmost) choice.
def highest_battery(bank, position, space_needed):
    # First, determine what the highest battery value is.
    # Leave enough space on the right side (the space_needed parameter)
    # so that we can enable the required number of batteries.
    highest_digit = 0
    for p in [position]:
        highest_digit = max(highest_digit, max(bank[p + 1: len(bank) - space_needed + 1]))

    # Now determine the first (leftmost) position with that highest value.
    while True:
        position += 1
        if bank[position] == highest_digit: return position

# Determine the highest joltage we can make for a given battery bank
# and number of batteries to enable.
def max_joltage(bank, num_batteries):
    position = -1
    joltage = 0
    for level in range(num_batteries):
        space_needed = num_batteries - level
        position = highest_battery(bank, position, space_needed)

        # Enable the selected battery, increasing the current joltage.
        joltage *= 10
        joltage += bank[position]
    return joltage

# Parse the battery bank / joltage map
with open('day03_input.txt') as f:
    banks = [[int(n) for n in line.rstrip('\n')] for line in f]

total_output_joltage_part_one = 0
total_output_joltage_part_two = 0
for bank in banks:
    total_output_joltage_part_one += max_joltage(bank, 2)
    total_output_joltage_part_two += max_joltage(bank, 12)

# There are many batteries in front of you.
# Find the maximum joltage possible from each bank; what is the total output joltage?
print('Part Two: The new total output joltage is {0}.'.format(total_output_joltage_part_one))

# What is the new total output joltage?
print('Part Two: The new total output joltage is {0}.'.format(total_output_joltage_part_two))