#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.setrecursionlimit(1500)

GROUND    = '.'
CLAY      = '#'
WATERFALL = '|'
WATER     = '~'
SPRING    = '+'

SPRING_LOCATION = (500, 0)

water_types = [WATER, WATERFALL]
support_types = [WATER, CLAY]
flow_types = [WATER, WATERFALL, GROUND]

# Conversion between characters specified in the assignment
# and UTF-8 block characters for pretty printing
print_chrs = { GROUND:    ' ',
               CLAY:      '█',
               WATERFALL: '░',
               WATER:     '▒',
               SPRING:    'o'}

def pretty_print():
    for y in range(y_max + 2):
        line = ''
        for x in range(x_min - 1, x_max + 2):
            line += print_chrs[ground.get((x, y), GROUND)]
        print line

def find_transitions(x, y):
    # Water flows left!
    x_orig = x
    x -= 1
    while ground.get((x, y), GROUND) in flow_types and ground.get((x, y + 1), GROUND) in support_types:
        x -= 1
    x_left = x

    # Water flows right!
    x = x_orig
    x += 1
    while ground.get((x, y), GROUND) in flow_types and ground.get((x, y + 1), GROUND) in support_types:
        x += 1
    x_right = x

    # Determine the transition types: walls or open space
    transition_left = ground.get((x_left, y), GROUND)
    transition_right = ground.get((x_right, y), GROUND)

    return (x_left, x_right, transition_left, transition_right)

def water_fall(x, y):
    if y > y_max: return

    # Water falls...you know, vertically
    y_top = y
    y_bottom = y
    while (x, y_bottom) not in ground and y_bottom <= y_max:
        y_bottom += 1

    # Fill from the bottom
    for y in range(y_bottom - 1, y_top - 1, -1):
        water_fill(x, y)

def water_fill(x, y):
    if y > 0 and y > y_max: return

    (x_left, x_right, transition_left, transition_right) = find_transitions(x,y)

    if transition_left is CLAY and transition_right is CLAY:
        symbol = WATER
    else:
        symbol = WATERFALL

    # Bounded by clay walls, use static water symbol
    supported = True
    for x in range(x_left + 1, x_right):
        ground[(x, y)] = symbol
        if ground.get((x, y + 1), GROUND) not in support_types:
            supported = False

    # In order for water from a waterfall to flow left or right
    # and become another waterfall, it must be supported from below.
    if symbol is WATERFALL and not supported:
        return

    # Left waterfall!
    if transition_left is GROUND:
        water_fall(x_left, y)

    # Right waterfall!
    if transition_right is GROUND:
        water_fall(x_right, y)

    if transition_left is CLAY and transition_right is CLAY:
        # Second-pass fill to cover uneven containers
        for x in range(x_left + 1, x_right):
            ground[(x, y)] = WATER

# Build the clay containers
with open('day17_input.txt') as f:
    input = [line.rstrip('\n') for line in f]

x_min = 99999
y_min = 99999
x_max = -99999
y_max = -99999
ground = {}

for entry in input:
    entry = entry.replace(' ', '').replace('..', ',').replace('=', ',').split(',')
    #print entry
    entry[1] = int(entry[1])
    entry[3] = int(entry[3])
    entry[4] = int(entry[4])

    if entry[0] is 'y':
        if entry[1] < y_min: y_min = entry[1]
        if entry[1] > y_max: y_max = entry[1]
        if entry[3] < x_min: x_min = entry[3]
        if entry[4] > x_max: x_max = entry[4]
        y = entry[1]
        for x in range(entry[3], entry[4] + 1):
            ground[(x, y)] = CLAY
    else:
        if entry[1] < x_min: x_min = entry[1]
        if entry[1] > x_max: x_max = entry[1]
        if entry[3] < y_min: y_min = entry[3]
        if entry[4] > y_max: y_max = entry[4]
        x = entry[1]
        for y in range(entry[3], entry[4] + 1):
            ground[(x, y)] = CLAY


# Set up the spring and start flowing!
water_location = SPRING_LOCATION
ground[water_location] = SPRING
water_fall(water_location[0], water_location[1] + 1)
pretty_print()

# Count our results
water = 0
retained_water = 0
for location in ground:
    if location[1] >= y_min and ground[location] in water_types:
        water += 1
        if ground[location] is WATER:
            retained_water += 1

print 'I count %d water, %d retained water!' % (water, retained_water)
