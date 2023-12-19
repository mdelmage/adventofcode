#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on.
dirs = {'U': ( 0, -1),
        'D': ( 0,  1),
        'L': (-1,  0),
        'R': ( 1,  0)}

# Parse the dig plan.
with open('day18_input.txt') as f:
    # The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U),
    # down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen
    # from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with
    # the color that the edge of the trench should be painted as an RGB hexadecimal color code.
    dig_plan = [(d, int(n), c[2:-1]) for (d, n, c) in [line.rstrip('\n').split() for line in f]]

# # The digger starts in a 1 meter cube hole in the ground.
loc = (0, 0)
dig = set([loc])

for (direction, length, color) in dig_plan:
    d = dirs[direction]
    loc_new = (loc[0] + (d[0] * length), loc[1] + (d[1] * length))

    # Simple method to add to the dig: keep iterating until we're at the next location.
    while loc != loc_new:
        loc = (loc[0] + d[0], loc[1] + d[1])
        dig.add(loc)
    loc = loc_new

# Now, flood the dig to see how much lava it can hold.
# The flood should start one tile diagonally from our starting hole.
#
# By inspection: the southeast neighbor works on both the sample and real inputs.
flood = set([(1, 1)])
while len(flood) > 0:
    flood_next = set()
    for pos in flood:
        # We only need to check neighbors within a Manhattan Distance of 1 during each iteration.
        # Think of Hollywood Squares, if we were the center square.
        for neighbor in [(pos[0] + i, pos[1] + j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]:
            if neighbor not in dig:
                # Found a new spot to explore; add it to the next iteration!
                dig.add(neighbor)
                flood_next.add(neighbor)

    flood = flood_next

if False:#for row in range(-100, 100):
    s = ''
    for col in range(-15, 150):
        if (col, row) == (0, 0):
            s += 'O'
        elif (col, row) in dig:
            s += '#'
        else:
            s += ' '
    print(s)

# The Elves are concerned the lagoon won't be large enough; if they follow their dig plan,
# how many cubic meters of lava could it hold?
print('Part One: Lagoon can hold {0} cubic meters of lava.'.format(len(dig)))