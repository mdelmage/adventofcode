#!/usr/bin/env python
# -*- coding: utf-8 -*-

# the cubes in this region start in the specified active (#) or inactive (.) state.
ACTIVE   = '#'
INACTIVE = '.'

# The energy source then proceeds to boot up by executing six cycles.
CYCLE_COUNT = 6

def neighbor_count(x, y, z, w=None):
    n = 0

    # Runtime check for the dimensionality of the grid
    for c in grid:
        dimension = len(c)
        break

    if dimension == 4:
        # Count neighbors in 4 dimensions
        for (dx, dy, dz, dw) in neighbors:
            if grid.get((x + dx, y + dy, z + dz, w + dw), INACTIVE) == ACTIVE: n += 1
    else:
        # Count neighbors in 3 dimensions
        for (dx, dy, dz) in neighbors:
            if grid.get((x + dx, y + dy, z + dz), INACTIVE) == ACTIVE: n += 1

    return n

def fill_grid(size):
    f = range(-size, size + 1)

    # Runtime check for the dimensionality of the grid
    for c in grid:
        dimension = len(c)
        break

    if dimension == 4:
        # Fill in 4 dimensions
        new_cells = [(x, y, z, w) for x in f for y in f for z in f for w in f]
    else:
        # Fill in 3 dimensions
        new_cells = [(x, y, z) for x in f for y in f for z in f]

    for c in new_cells:
        if c not in grid:
            grid[c] = INACTIVE

# Parse the Conway "pocket dimension" map and save each line
with open('day17_input.txt') as f:
    initial_state = [line.rstrip('\n').strip(':') for line in f]

# The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional
# coordinate (x,y,z), there exists a single cube which is either active or inactive.
grid = {}

for y in range(len(initial_state)):
    for x in range(len(initial_state[y])):
        # Even though the pocket dimension is 3-dimensional, this initial state represents
        # a small 2-dimensional slice of it. (In particular, this initial state defines
        # a 3x3x1 region of the 3-dimensional space.)
        grid[(x, y, 0)] = initial_state[y][x]

# Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates
# differ by at most 1. For example, given the cube at x=1,y=2,z=3, its neighbors include the cube
# at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.
d = [-1, 0, 1]
neighbors = [(x, y, z) for x in d for y in d for z in d]
neighbors.remove((0, 0, 0))

# Fill out the grid in all (3) dimensions.
fill_size = len(initial_state[0])

for cycle in range(CYCLE_COUNT):
    fill_grid(fill_size)
    grid_next = {}
    for (x, y, z) in grid:
        if grid[(x, y, z)] == ACTIVE and neighbor_count(x, y, z) in [2, 3]: grid_next[(x, y, z)] = ACTIVE
        if grid[(x, y, z)] == INACTIVE and neighbor_count(x, y, z) == 3: grid_next[(x, y, z)] = ACTIVE
    grid = grid_next
    fill_size += 1

print 'Part One: {0} active cubes left after {1} cycles.'.format(len(grid), CYCLE_COUNT)


# Reset the grid for 4 dimensions
grid = {}

for y in range(len(initial_state)):
    for x in range(len(initial_state[y])):
        # The pocket dimension contains an infinite 4-dimensional grid. At every integer 4-dimensional
        # coordinate (x,y,z,w), there exists a single cube (really, a hypercube) which is still either active or inactive.
        grid[(x, y, 0, 0)] = initial_state[y][x]

# Each cube only ever considers its neighbors: any of the 80 other cubes where any of their coordinates differ
# by at most 1. For example, given the cube at x=1,y=2,z=3,w=4, its neighbors include the cube at x=2,y=2,z=3,w=3,
# the cube at x=0,y=2,z=3,w=4, and so on.
neighbors = [(x, y, z, w) for x in d for y in d for z in d for w in d]
neighbors.remove((0, 0, 0, 0))

# Fill out the grid in all (4) dimensions.
fill_size = len(initial_state[0])

for cycle in range(CYCLE_COUNT):
    fill_grid(fill_size)
    grid_next = {}
    for (w, x, y, z) in grid:
        if grid[(x, y, z, w)] == ACTIVE and neighbor_count(x, y, z, w) in [2, 3]: grid_next[(x, y, z, w)] = ACTIVE
        if grid[(x, y, z, w)] == INACTIVE and neighbor_count(x, y, z, w) == 3: grid_next[(x, y, z, w)] = ACTIVE
    grid = grid_next
    fill_size += 1

print 'Part Two: {0} active cubes left after {1} cycles.'.format(len(grid), CYCLE_COUNT)
