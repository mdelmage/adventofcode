#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The tiles are all white on one side and black on the other. They start with the white side
# facing up. The lobby is large enough to fit whatever pattern might need to appear there.
WHITE = 0
BLACK = 1

WEST      = 0
EAST      = 1
NORTHWEST = 2
NORTHEAST = 3
SOUTHWEST = 4
SOUTHEAST = 5

# How many tiles will be black after 100 days?
DAYS = 100

# Because the tiles are hexagonal, every tile has six neighbors:
# east, southeast, southwest, west, northwest, and northeast.
# These directions are given in your list, respectively, as e, se, sw, w, nw, and ne.
# A tile is identified by a series of these directions with no delimiters;
# for example, esenee identifies the tile you land on if you start at the reference tile
# and then move one tile east, one tile southeast, one tile northeast, and one tile east.
directions = { WEST      : 'w',
               EAST      : 'e',
               NORTHWEST : 'nw',
               NORTHEAST : 'ne',
               SOUTHWEST : 'sw',
               SOUTHEAST : 'se'}

# A hexagonal grid can be back-ended by a regular square grid, with odd and even
# rows shifted by a "half-column". What this means is that the tile you end up at
# after a move, depends on whether you started on an odd or even row.
#
# East and west moves are the same for all tiles.
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

# To move to a neighbor, just apply the move from the appropriate odd/even dict.
def move(pos, direction):
    if (pos[1] % 2) == 0:
        delta = moves_even[direction]
    else:
        delta = moves_odd[direction]

    return (pos[0] + delta[0], pos[1] + delta[1])

# Use the move() function to make it easy to count the neighbors.
def neighbors(pos):
    count = 0
    for d in directions:
        neighbor = move(pos, d)
        if grid.get(neighbor, WHITE) == BLACK: count += 1
    return count  

# Parse the list of tiles that need to be flipped over, and save each line
with open('day24_input.txt') as f:
    flips = [line.rstrip('\n').rstrip(')') for line in f]

grid = {}
max_flips_len = 0
for f in flips:
    pos = (0, 0)
    flips_len = 0
    while len(f) > 0:
        # Consume the flip string by matching any directions we can.
        for d in directions:
            dir = directions[d]
            if f[:len(dir)] == dir:
                # We got a match; trim the flip string and update our position.
                f = f[len(dir):]
                pos = move(pos, d)
                flips_len += 1

    # This is the final position for the string. Flip this tile.
    grid[pos] = grid.get(pos, WHITE) ^ 1

    # Was this the longest excursion so far?
    max_flips_len = max(max_flips_len, flips_len)

count = 0
for tile in grid:
    if grid[tile] == BLACK: count += 1
print 'Part One: there are {0} black tiles initially.'.format(count)

for i in range(DAYS):
    flip_set = set([])

    # The grid size can only expand at a rate of 1 per day, so limit our consideration accordingly.
    frange = max_flips_len + i

    # The tile floor in the lobby is meant to be a living art exhibit.
    # Every day, the tiles are all flipped according to the following rules:
    for tile in [(x, y) for x in range(-frange, frange + 1) for y in range(-frange, frange + 1)]:
        neighbor_count = neighbors(tile)
        # Any black tile with zero or more than 2 black tiles
        # immediately adjacent to it is flipped to white.
        if grid.get(tile, WHITE) == BLACK and neighbor_count not in [1, 2]: flip_set.add(tile)

        # Any white tile with exactly 2 black tiles immediately adjacent
        # to it is flipped to black.
        if grid.get(tile, WHITE) == WHITE and neighbor_count == 2: flip_set.add(tile)

    # The rules are applied simultaneously to every tile; put another way,
    # it is first determined which tiles need to be flipped, then they are all flipped
    # at the same time.
    for tile in flip_set:
        grid[tile] = grid.get(tile, WHITE) ^ 1

    # How many tiles will be black after 100 days?
    count = 0
    for tile in grid:
        if grid[tile] == BLACK: count += 1

print 'Part Two: there are {0} black tiles after {1} days.'.format(count, DAYS)