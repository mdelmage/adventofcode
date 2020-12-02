#!/usr/bin/env python
# -*- coding: utf-8 -*-

def manhattan_distance(p):
    return (abs(p[0]) + abs(p[1]))

# Each square on the grid is allocated in a spiral pattern starting at a location marked 1
# and then counting up while spiraling outward. For example, the first few squares
# are allocated like this:
#
# 17  16  15  14  13
# 18   5   4   3  12
# 19   6   1   2  11
# 20   7   8   9  10
# 21  22  23---> ...

INPUT = 265149

DIRS = [(1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)]

dir_idx = 0
dir_len = 1
num = 1
loc_x = 0
loc_y = 0
larger_than_input = None

# Part One grid is a reverse lookup, value --> location
grid1 = {num : (loc_x, loc_y)}

# Part Two grid is a forward lookup, location --> value
grid2 = {(loc_x, loc_y) : num}

# Naïve City: just construct the spiral pattern programatically
while num < INPUT:
    # We go two directions in the spiral before lengthening the sides
    for r in range(2):
        for i in range(dir_len):
            loc_x += DIRS[dir_idx][0]
            loc_y += DIRS[dir_idx][1]
            num += 1
            grid1[num] = (loc_x,loc_y)
            
            # As a stress test on the system, the programs here clear the grid and then
            # store the value 1 in square 1. Then, in the same allocation order as shown above,
            # they store the sum of the values in all adjacent squares, including diagonals.
            grid2[(loc_x, loc_y)] = grid2.get((loc_x + 1, loc_y), 0) + \
                                    grid2.get((loc_x - 1, loc_y), 0) + \
                                    grid2.get((loc_x, loc_y + 1), 0) + \
                                    grid2.get((loc_x, loc_y - 1), 0) + \
                                    grid2.get((loc_x + 1, loc_y + 1), 0) + \
                                    grid2.get((loc_x + 1, loc_y - 1), 0) + \
                                    grid2.get((loc_x - 1, loc_y + 1), 0) + \
                                    grid2.get((loc_x - 1, loc_y - 1), 0)
            if not larger_than_input and grid2[(loc_x, loc_y)] > INPUT:
                larger_than_input = grid2[(loc_x, loc_y)]

        # Change directionsin the spiral
        dir_idx = (dir_idx + 1) % len(DIRS)

    # Spiral is now longer for two more sides
    dir_len += 1

print 'Part One: square %d is %d steps away.' % (INPUT, manhattan_distance(grid1[INPUT]))
print 'Part Two: first value > %d was %d.' % (INPUT, larger_than_input)