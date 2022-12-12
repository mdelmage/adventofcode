#!/usr/bin/env python
# -*- coding: utf-8 -*-

SYMBOL_START = 'S'
SYMBOL_END = 'E'

# Letter heights will be mapped a-z --> 1-26, so start at
# height 0 and search for the ending location at 27.
HEIGHT_START = 0
HEIGHT_END = 27

# Determine which neighbors are actually in the grid.
# This function effectively does edge- and corner-bounds checks.
def neighbors(g, loc):
    neighbor_list = []
    for n in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        possible_neighbor = (loc[0] + n[0], loc[1] + n[1]) 
        if possible_neighbor in g:
            neighbor_list.append(possible_neighbor)
    return neighbor_list

# Convert 'a'-'z' heights to integer (1-26).
# Also handle Start and End locations.
def height(letter):
    if letter == SYMBOL_START: return HEIGHT_START
    if letter == SYMBOL_END: return HEIGHT_END
    return ord(letter) - ord('a') + 1

# Starting at one or more locations in the grid, traverse until
# we find the ending square. Determine the shortest path there.
def walk(g, starting_locations):
    path_len = 0
    shortest_path = len(g)
    locs = starting_locations

    paths = {}
    for loc in starting_locations:
        paths[loc] = 0

    while len(locs) > 0:
        new_locs = []
        for loc in locs:
            if grid[loc] == SYMBOL_END: shortest_path = min(shortest_path, path_len)
            for n in neighbors(grid, loc):
                # To avoid needing to get out your climbing gear, the elevation of the destination
                # square can be at most one higher than the elevation of your current square;
                # that is, if your current elevation is m, you could step to elevation n, but not
                # to elevation o. (This also means that the elevation of the destination square
                # can be much lower than the elevation of your current square.)
                if height(grid[n]) <= height(grid[loc]) + 1:
                    if path_len < paths.get(n, len(g)):
                        # We found a new shorter path to this location! Mark it and queue it up
                        # for further traversal.
                        paths[n] = path_len
                        new_locs.append(n)

        locs = new_locs
        path_len += 1

    return shortest_path

# Parse the heightmap file
with open('day12_input.txt') as f:
    heightmap = [line.rstrip('\n') for line in f]

grid = {}
lowest_spots = []
for row in range(len(heightmap)):
    for col in range(len(heightmap[0])):
        # Convert the heightmap list to a location dict
        grid[(col, row)] = heightmap[row][col]

        if heightmap[row][col] == SYMBOL_START:
            # Mark the starting spot ('S')
            starting_spot = [(col, row)]
        elif heightmap[row][col] == 'a':
            # As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail.
            # The beginning isn't very scenic, though; perhaps you can find a better starting point.
            #
            # To maximize exercise while hiking, the trail should start as low as possible: elevation a.
            lowest_spots.append((col, row))

print('Part One: from S, it is {0} steps to the location with the best signal.'.format(walk(grid, starting_spot)))
print('Part Two: from elevation a, it is {0} steps to the location with the best signal.'.format(walk(grid, lowest_spots)))
