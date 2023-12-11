#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The pipes are arranged in a two-dimensional grid of tiles:
#
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile,
# but your sketch doesn't show what shape the pipe has.
TILE_NORTH_SOUTH = '|'
TILE_WEST_EAST   = '-'
TILE_NORTH_EAST  = 'L'
TILE_NORTH_WEST  = 'J'
TILE_SOUTH_WEST  = '7'
TILE_SOUTH_EAST  = 'F'
TILE_GROUND      = '.'
TILE_START       = 'S'

# Add our own tile, flood, to indicate blank space that's not a ground tile.
TILE_FLOOD       = '~'

NORTH = 1
SOUTH = 2
WEST  = 3
EAST  = 4

# Determine the next location, based on which way we're facing,
# and assuming that we're on a continuous loop with exactly one entrance and exit
# for each tile in the loop.
def next_loc(n, facing):
    loc_north = (n[0], n[1] - 1)
    loc_south = (n[0], n[1] + 1)
    loc_west  = (n[0] - 1, n[1])
    loc_east  = (n[0] + 1, n[1])
    neighbor_north = pipes.get(loc_north, TILE_GROUND)
    neighbor_south = pipes.get(loc_south, TILE_GROUND)
    neighbor_west  = pipes.get(loc_west, TILE_GROUND)
    neighbor_east  = pipes.get(loc_east, TILE_GROUND)

    if facing == NORTH:
        if neighbor_north == TILE_NORTH_SOUTH: return (loc_north, NORTH)
        if neighbor_north == TILE_SOUTH_WEST:  return (loc_north, WEST)
        if neighbor_north == TILE_SOUTH_EAST:  return (loc_north, EAST)
    elif facing == SOUTH:
        if neighbor_south == TILE_NORTH_SOUTH: return (loc_south, SOUTH)
        if neighbor_south == TILE_NORTH_WEST:  return (loc_south, WEST)
        if neighbor_south == TILE_NORTH_EAST:  return (loc_south, EAST)
    elif facing == WEST:
        if neighbor_west == TILE_WEST_EAST:  return (loc_west, WEST)
        if neighbor_west == TILE_NORTH_EAST: return (loc_west, NORTH)
        if neighbor_west == TILE_SOUTH_EAST: return (loc_west, SOUTH)
    elif facing == EAST:
        if neighbor_east == TILE_WEST_EAST:  return (loc_east, EAST)
        if neighbor_east == TILE_NORTH_WEST: return (loc_east, NORTH)
        if neighbor_east == TILE_SOUTH_WEST: return (loc_east, SOUTH)
    return None

# Parse the surface pipes map.
# Make a backup copy because we're gonna be messing with our copy.
with open('day10_input.txt') as f:
    rows = [line.rstrip('\n') for line in f]

    pipes = {}
    pipes_orig = {}
    for row in range(len(rows)):
        for col in range(len(rows[row])):
            pipes[(col, row)] = rows[row][col]
            pipes_orig[(col, row)] = rows[row][col]
            if rows[row][col] == TILE_START: start = (col, row)

# Save the size, aka axis length. Assume a square surface pipes map.
size = len(rows)

# Every tile in the main loop has exactly two valid neighbors.
# Traverse the whole loop until we return to the start.
steps = 0
loc = start
facing = SOUTH
while True:
    steps += 1
    n = next_loc(loc, facing)
    if not n: break
    (loc, facing) = n
    if loc == start: break
    pipes[loc] = steps

# For any closed loop, the distance of the furthest tile is exactly half the loop length.
furthest_tile = steps // 2

# Find the single giant loop starting at S. How many steps along the loop does it take
# to get from the starting position to the point farthest from the starting position?
print('Part One: Furthest distance away is {0} steps.'.format(furthest_tile))

# Now bring over only the main loop.
pipes_next = {}
for p in pipes:
    if isinstance(pipes[p], int) or pipes[p] == TILE_START: pipes_next[p] = pipes_orig[p]
pipes = pipes_next

# Fill in the field with ground tiles.
# Add a 1-unit border so we can go around tiles at the edge of the map.
for row in range(-1, size + 1):
    for col in range(-1, size + 1):
        if (col, row) not in pipes: pipes[(col, row)] = TILE_GROUND

# By inspection: replace the start tile with the appropriate pipe tile.
# This is wrong and bad and is not a general solution for any input.
pipes[start] = TILE_NORTH_SOUTH

# You quickly reach the farthest point of the loop, but the animal never emerges.#
# Maybe its nest is within the area enclosed by the loop?
#
# To determine whether it's even worth taking the time to search for such a nest,
# you should calculate how many tiles are contained within the loop.

# In fact, there doesn't even need to be a full tile path to the outside for tiles
# to count as outside the loop - squeezing between pipes is also allowed!
#
# This problem is set up for a pretty standard flood implementation, but that
# last little detail -- you can squeeze between pipes -- makes things a little tricky.
# One way to handle this is to blow up the grid to triple its original size.
# This lets our standard flood implementation flow between pipes.
pipes_next = {}
for (col, row) in pipes:
    p = (col, row)
    # Every tile becomes three tiles after magnification, except the ground tile.
    # It doesn't matter which tiles they actually are, as long as they're not the ground tile,
    # but choosing the corect tiles makes for prettier printing/debugging.
    if pipes[p] == TILE_NORTH_SOUTH:
        pipes_next[(3 * col + 0, 3 * row - 1)] = TILE_NORTH_SOUTH
        pipes_next[(3 * col + 0, 3 * row + 0)] = TILE_NORTH_SOUTH
        pipes_next[(3 * col + 0, 3 * row + 1)] = TILE_NORTH_SOUTH
    elif pipes[p] == TILE_WEST_EAST:
        pipes_next[(3 * col - 1, 3 * row + 0)] = TILE_WEST_EAST
        pipes_next[(3 * col + 0, 3 * row + 0)] = TILE_WEST_EAST
        pipes_next[(3 * col + 1, 3 * row + 0)] = TILE_WEST_EAST
    elif pipes[p] == TILE_NORTH_EAST:
        pipes_next[(3 * col + 0, 3 * row - 1)] = TILE_NORTH_SOUTH
        pipes_next[(3 * col + 0, 3 * row + 0)] = TILE_NORTH_EAST
        pipes_next[(3 * col + 1, 3 * row + 0)] = TILE_WEST_EAST
    elif pipes[p] == TILE_NORTH_WEST:
        pipes_next[(3 * col + 0, 3 * row - 1)] = TILE_NORTH_SOUTH
        pipes_next[(3 * col + 0, 3 * row + 0)] = TILE_NORTH_WEST
        pipes_next[(3 * col - 1, 3 * row + 0)] = TILE_WEST_EAST
    elif pipes[p] == TILE_SOUTH_WEST:
        pipes_next[(3 * col + 0, 3 * row + 1)] = TILE_NORTH_SOUTH
        pipes_next[(3 * col + 0, 3 * row + 0)] = TILE_SOUTH_WEST
        pipes_next[(3 * col - 1, 3 * row + 0)] = TILE_WEST_EAST
    elif pipes[p] == TILE_SOUTH_EAST:
        pipes_next[(3 * col + 0, 3 * row + 1)] = TILE_NORTH_SOUTH
        pipes_next[(3 * col + 0, 3 * row + 0)] = TILE_SOUTH_EAST
        pipes_next[(3 * col + 1, 3 * row + 0)] = TILE_WEST_EAST
    elif pipes[p] == TILE_GROUND:
        pipes_next[(3 * col + 0, 3 * row + 0)] = TILE_GROUND
pipes = pipes_next

# Now fill in the gaps with a flood tile. It needs to be distinct
# from the ground tile, since we'll be counting those later on.
#
# Add a 1-unit border (now 3-unit after magnification) so the flood will go around
# tiles at the edge of the map.
for row in range(-1 * 3, size * 3 + 1):
    for col in range(-1 * 3, size * 3 + 1):
        if (col, row) not in pipes: pipes[(col, row)] = TILE_FLOOD

# Standard flood implementation. Keep expanding until there are no more ground or flood tiles left.
# Note the use of a set, to prevent duplicates and to prevent any ping-ponging between two locations.
flood = set()
s = (-1, -1)
flood.add(s)
NEIGHBORS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
while len(flood) > 0:
    flood_next = set()
    for f in flood:
        for n in NEIGHBORS:
            neighbor = (f[0] + n[0], f[1] + n[1]) 
            if neighbor in pipes and pipes[neighbor] in [TILE_GROUND, TILE_FLOOD]: flood_next.add(neighbor)

    # Remove explored locations and continue.
    for f in flood:
        if f in pipes: del pipes[f]
    flood = flood_next

# Figure out whether you have time to search for the nest by calculating the area within the loop.
# How many tiles are enclosed by the loop?
enclosed_tiles = len([t for t in pipes.values() if t == TILE_GROUND])
print('Part Two: There are {0} tiles enclosed by the main loop.'.format(enclosed_tiles))