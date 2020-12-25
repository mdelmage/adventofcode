#!/usr/bin/env python
# -*- coding: utf-8 -*-

WHITE = 0
BLACK = 1

WEST      = 0
EAST      = 1
NORTHWEST = 2
NORTHEAST = 3
SOUTHWEST = 4
SOUTHEAST = 5

DAYS = 100

directions = { WEST      : 'w',
               EAST      : 'e',
               NORTHWEST : 'nw',
               NORTHEAST : 'ne',
               SOUTHWEST : 'sw',
               SOUTHEAST : 'se'}

moves_odd = { WEST      : (-1,  0),
              EAST      : ( 1,  0),
              NORTHWEST : (-1,  1),
              NORTHEAST : ( 0,  1),
              SOUTHWEST : (-1, -1),
              SOUTHEAST : ( 0, -1)}

moves_even = { WEST      : (-1,  0),
               EAST      : ( 1,  0),
               NORTHWEST : ( 0,  1),
               NORTHEAST : ( 1,  1),
               SOUTHWEST : ( 0, -1),
               SOUTHEAST : ( 1, -1)}

def move(pos, direction):
    if (pos[1] % 2) == 0:
        delta = moves_even[direction]
    else:
        delta = moves_odd[direction]

    return (pos[0] + delta[0], pos[1] + delta[1])

def neighbors(pos):
    count = 0
    for d in directions:
        if (pos[1] % 2) == 0:
            delta = moves_even[d]
        else:
            delta = moves_odd[d]
        neighbor = (pos[0] + delta[0], pos[1] + delta[1])
        if grid.get(neighbor, WHITE) == BLACK: count += 1
    return count
    

# Parse the list of tiles that need to be flipped over, and save each line
with open('day24_input.txt') as f:
    flips = [line.rstrip('\n').rstrip(')') for line in f]

print flips
grid = {}
for f in flips:
    pos = (0, 0)
    while len(f) > 0:
        for d in directions:
            dir = directions[d]
            if f[:len(dir)] == dir:
                f = f[len(dir):]
                pos = move(pos, d)
    grid[pos] = grid.get(pos, WHITE) ^ 1

count = 0
for tile in grid:
    if grid[tile] == BLACK: count += 1
print 'Part One: there are {0} black tiles initially.'.format(count)

for i in range(DAYS):
    flip_set = set([])
    for tile in [(x, y) for x in range(-100 - i, 100 + i) for y in range(-100 -i, 100 + i)]:
        neighbor_count = neighbors(tile)
        if grid.get(tile, WHITE) == BLACK and neighbor_count not in [1, 2]: flip_set.add(tile)
        if grid.get(tile, WHITE) == WHITE and neighbor_count == 2: flip_set.add(tile)
    for tile in flip_set:
        grid[tile] = grid.get(tile, WHITE) ^ 1

    count = 0
    for tile in grid:
        if grid[tile] == BLACK: count += 1

print 'Part Two: there are {0} black tiles after {1} days.'.format(count, DAYS)