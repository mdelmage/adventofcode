#!/usr/bin/env python
# -*- coding: utf-8 -*-

NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

OFF_MAP = '.'

def perimeter(region):
    # Each garden plot is a square and so has four sides. The perimeter of a region is the number of sides
    # of garden plots in the region that do not touch another garden plot in the same region.
    p = 0
    for plot in region:
        for n in NEIGHBORS:
            if garden.get((plot[0] + n[0], plot[1] + n[1]), OFF_MAP) != garden[plot]:
                p += 1
    return p

def sides(region):
    # Identify the plant for this region.
    for plot in region:
        plant = garden[plot]
        break

    # To determine how many 'sides' the region has, first identify all fencing
    # for each cardinal direction, and sort it by primary axis (the row for east/west fencing,
    # and the column for north/south) and then secondary axis (whichever row/col is not the primary).
    west_fences = {}
    east_fences = {}
    north_fences = {}
    south_fences = {}
    for col, row in region:
        if garden.get((col - 1, row), OFF_MAP) != plant:
            if col not in west_fences: west_fences[col] = []
            west_fences[col].append(row)
        if garden.get((col + 1, row), OFF_MAP) != plant:
            if col not in east_fences: east_fences[col] = []
            east_fences[col].append(row)
        if garden.get((col, row - 1), OFF_MAP) != plant:
            if row not in north_fences: north_fences[row] = []
            north_fences[row].append(col)
        if garden.get((col, row + 1), OFF_MAP) != plant:
            if row not in south_fences: south_fences[row] = []
            south_fences[row].append(col)

    # Now that we have the fencing identified, let's sort it and look for gaps.
    # For each gap that we identify, that counts as a new 'side' for that region.
    sides = 0
    for fence in [west_fences, east_fences, north_fences, south_fences]:
        for primary_axis in fence:
            last_secondary_axis = -2
            for secondary_axis in sorted(fence[primary_axis]):
                if secondary_axis != last_secondary_axis + 1:
                    sides += 1
                last_secondary_axis = secondary_axis

    return sides

# Parse the map of garden plots.
with open('day12_input.txt') as f:
    g = [line.rstrip('\n') for line in f]
    garden = {}
    for row in range(len(g)):
        for col in range(len(g[0])):
            garden[(col, row)] = g[row][col]

# Break out the garden into regions.
# This is a little inefficient, but the fencing calculations are very quick
# once the regions are set.
unmapped_plots = [(a, b) for a in range(len(g)) for b in range(len(g[0]))]
regions = []
while len(unmapped_plots) > 0:
    plant = garden[unmapped_plots[0]]
    region = set([unmapped_plots[0]])
    del unmapped_plots[0]
    while True:
        region_next = []
        for plot in region:
            for n in NEIGHBORS:
                neighbor = (plot[0] + n[0], plot[1] + n[1])
                if garden.get(neighbor, OFF_MAP) == plant:
                    if neighbor in unmapped_plots:
                        region_next.append(neighbor)
                        del unmapped_plots[unmapped_plots.index(neighbor)]
        if len(region_next) > 0:
            for plot in region_next: region.add(plot)
        else:
            break
    regions.append(region)

fence_price_part_one = 0
fence_price_part_two = 0
for region in regions:
    # Due to "modern" business practices, the price of fence required for a region is found
    # by multiplying that region's area by its perimeter. The total price of fencing all regions
    # on a map is found by adding together the price of fence for every region on the map.
    fence_price_part_one += len(region) * perimeter(region)

    # Fortunately, the Elves are trying to order so much fence that they qualify for a bulk discount!
    #
    # Under the bulk discount, instead of using the perimeter to calculate the price, you need to use
    # the number of sides each region has. Each straight section of fence counts as a side, regardless
    # of how long it is.
    fence_price_part_two += len(region) * sides(region)

# What is the total price of fencing all regions on your map?
print('Part One: Total price of fencing all regions is {0}.'.format(fence_price_part_one))

# What is the new total price of fencing all regions on your map?
print('Part Two: Total price of fencing all regions is {0}.'.format(fence_price_part_two))
