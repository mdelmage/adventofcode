#!/usr/bin/env python
# -*- coding: utf-8 -*-

# There are lots of numbers and symbols you don't really understand, but apparently any number adjacent
# to a symbol, even diagonally, is a "part number" and should be included in your sum.
# (Periods (.) do not count as a symbol.)
def symbol_nearby(d, x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor_loc = (x + i, y + j)
            neighbor = d.get(neighbor_loc, '.')
            # Be sure to exclued ourselves -- aka offset (0, 0) -- and periods.
            if (i, j) != (0, 0) and neighbor != '.' and not neighbor.isdigit(): return neighbor_loc

    return None

# Parse the schematic
with open('day03_input.txt') as f:
    schematic = [line.rstrip('\n') for line in f]

# Convert the schematic from a list-of-lists, to a dict.
d = {}
for y in range(len(schematic)):
    for x in range(len(schematic[y])):
        d[(x, y)] = schematic[y][x]

# A little bit of cheating here, but by inspection, inputs are square, so dynamically
# calculate the size of each axis by taking the square root.
size = int(len(d) ** 0.5)

part_number_sum = 0
is_part_number = False
number = 0
star_nearby = None
gears = {}

# Scan the whole schematic, row by row and left-to-right, for digits.
# Those digits will be part of numbers, which only appear horizontally.
# Some of those numbers will be part numbers (if they're near a symbol).
# Some of those part numbers will be gear ratios (if the nearby symbol is a *).
for y in range(size):
    for x in range(size):
        if d[(x, y)].isdigit():
            # A digit. Could be the start, middle, or end of a number.
            digit = int(d[(x, y)])

            # Scan for symbols.
            # This implementation assumes there will only be a maximum of one nearby.
            symbol = symbol_nearby(d, x, y)
            if symbol:
                # A symbol was nearby, so this number is a part number.
                is_part_number = True

                # A * symbol was nearby, so this part number is also a gear ratio.
                if d[symbol] == '*': star_nearby = symbol

            # Shift the number and add the current digit.
            number *= 10
            number += digit
        else:
            # Not a digit. If we were parsing a number, record it and start looking for another.
            if number > 0 and is_part_number:
                # The engineer explains that an engine part seems to be missing from the engine,
                # but nobody can figure out which one. If you can add up all the part numbers
                # in the engine schematic, it should be easy to work out which part is missing.
                part_number_sum += number
                if star_nearby:
                    if star_nearby in gears:
                        gears[star_nearby].append(number)
                    else:
                        gears[star_nearby] = [number]

            is_part_number = False
            number = 0
            star_nearby = None

print('Part One: Sum of all the part numbers is {0}.'.format(part_number_sum))

# The missing part wasn't the only issue - one of the gears in the engine is wrong.
# A gear is any * symbol that is adjacent to exactly two part numbers.
# Its gear ratio is the result of multiplying those two numbers together.
gear_ratio_sum = 0
for g in gears:
    ratios = gears[g]
    if len(ratios) == 2: gear_ratio_sum += ratios[0] * ratios[1]

print('Part Two: Sum of all the gear ratios is {0}.'.format(gear_ratio_sum))