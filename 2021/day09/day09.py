#!/usr/bin/env python
# -*- coding: utf-8 -*-

NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
MAX_HEIGHT = 9

heightmap = {}
basins = {}

def print_grid():
	for y in range(GRID_SIZE_Y):
		str = ''
		for x in range(GRID_SIZE_X):
			str += '{0}'.format(heightmap[(x, y)])
		print(str)
	print('')

def fill_basin(loc, fill_value):
	# A basin is all locations that eventually flow downward to a single low point.
	# Therefore, every low point has a basin, although some basins are very small.
	# Locations of height 9 do not count as being in any basin, and all other locations
	# will always be part of exactly one basin.
	if loc not in heightmap or heightmap[loc] != fill_value:
		basins[fill_value] = basins.get(fill_value, 0) + 1
		heightmap[loc] = fill_value
	for n in NEIGHBORS:
		neighbor = (loc[0] + n[0], loc[1] + n[1])
		neighbor_height = heightmap.get(neighbor, fill_value)
		if not isinstance(neighbor_height, str) and neighbor_height < MAX_HEIGHT:
			# Flood-style recursive fill of the basin
			fill_basin(neighbor, fill_value)

# Parse the heightmap file
with open('day09_input.txt') as f:
	rows = [line.rstrip('\n') for line in f]
	for y in range(len(rows)):
		for x in range(len(rows[y])):
			heightmap[(x, y)] = int(rows[y][x])

GRID_SIZE_X = len(rows[0])
GRID_SIZE_Y = len(rows)

# Your first goal is to find the low points - the locations that are lower than any
# of its adjacent locations. Most locations have four adjacent locations (up, down,
# left, and right); locations on the edge or corner of the map have three or two
# adjacent locations, respectively. (Diagonal locations do not count as adjacent.)
risk_sum = 0
low_spots = []
for y in range(GRID_SIZE_Y):
	for x in range(GRID_SIZE_X):
		lower_neighbors = 0
		for n in NEIGHBORS:
			# Count up the lower neighbors, treating spaces off the map as "really high".
			if heightmap[(x, y)] < heightmap.get((x + n[0], y + n[1]), MAX_HEIGHT):
				lower_neighbors += 1
		if lower_neighbors == 4:
			# Found a low spot. Mark it, and add its risk value.
			# The risk level of a low point is 1 plus its height.
			low_spots += [(x, y)]
			risk_sum += heightmap[(x, y)] + 1
print('Part One: sum of risk levels of low points is {0}.'.format(risk_sum))

# Now identify the basins, using a flood-fill, starting at each low spot.
# Mark each basin with a character, starting with 'a' and then 
for i in range(len(low_spots)):
	fill_basin(low_spots[i], chr(ord('a') + i))

# Find the three largest basins and multiply their sizes together. 
product = 1
product_count = 0
for item in dict(sorted(basins.items(), key=lambda x: x[1], reverse=True)):
	product *= basins[item]
	product_count += 1
	if product_count == 3: break
print('Part Two: product of three largest basin sizes is {0}.'.format(product))