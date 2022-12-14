#!/usr/bin/env python
# -*- coding: utf-8 -*-

ROCK = '█'
SAND = '░'

# The sand is pouring into the cave from point 500,0.
SOURCE = (500, 0)

def pour_sand(c, deepest_point, bottomless):
    source_reached = False
    sand_count = 0

    while not source_reached:
        sand_loc = SOURCE
        sand_falling = True

        # Sand falling algo
        while sand_falling:
            if bottomless:
                if sand_loc[1] > deepest_point:
                    # Once all 24 units of sand shown above have come to rest,
                    # all further sand flows out the bottom, falling into the endless void.
                    sand_falling = False
                    source_reached = True
            else:
                # You don't have time to scan the floor, so assume the floor is
                # an infinite horizontal line with a y coordinate equal to
                # two plus the highest y coordinate of any point in your scan.
                cave[(sand_loc[0], deepest_point + 2)] = ROCK
                cave[(sand_loc[0] + 1, deepest_point + 2)] = ROCK
                cave[(sand_loc[0] - 1, deepest_point + 2)] = ROCK

            # A unit of sand always falls down one step if possible.
            # If the tile immediately below is blocked (by rock or sand), the unit of sand
            # attempts to instead move diagonally one step down and to the left. If that tile
            # is blocked, the unit of sand attempts to instead move diagonally one step down
            # and to the right. Sand keeps moving as long as it is able to do so, at each step
            # trying to move down, then down-left, then down-right.
            down = (sand_loc[0], sand_loc[1] + 1)
            down_and_left = (sand_loc[0] - 1, sand_loc[1] + 1)
            down_and_right = (sand_loc[0] + 1, sand_loc[1] + 1)

            if down not in cave:
                sand_loc = down
            elif down_and_left not in cave:
                sand_loc = down_and_left
            elif down_and_right not in cave:
                sand_loc = down_and_right
            else:
                # If all three possible destinations are blocked, the unit of sand comes to rest
                # and no longer moves, at which point the next unit of sand is created back at the source.
                sand_falling = False
                sand_count += 1
                cave[sand_loc] = SAND

                # To find somewhere safe to stand, you'll need to simulate falling sand until
                # a unit of sand comes to rest at 500,0, blocking the source entirely and stopping
                # the flow of sand into the cave.
                if sand_loc == SOURCE:
                    source_reached = True

    return sand_count

# Parse the cave mapfile
with open('day14_input.txt') as f:
    rock_lines = [line.rstrip('\n') for line in f]

cave = {}
deepest_point = 0
for line in rock_lines:
    locs = line.split(' -> ')
    for i in range(len(locs) - 1):
        start_point = [int(c) for c in locs[i].split(',')]
        end_point = [int(c) for c in locs[i + 1].split(',')]

        deepest_point = max(deepest_point, start_point[1])
        deepest_point = max(deepest_point, end_point[1])

        if start_point[0] == end_point[0]:
            # Vertical slice
            y_start = min(start_point[1], end_point[1])
            y_end = max(start_point[1], end_point[1])
            for y in range(y_start, y_end + 1):
                cave[(start_point[0], y)] = ROCK
        else:
            # Horizontal slice
            x_start = min(start_point[0], end_point[0])
            x_end = max(start_point[0], end_point[0])
            for x in range(x_start, x_end + 1):
                cave[(x, start_point[1])] = ROCK


print('Part One: {0} units of sand fell before flowing into the abyss.'.format(pour_sand(cave, deepest_point, bottomless=True)))

# Reset the cave, removing any sand that fell in Part One
new_cave = {}
for loc in cave:
    if cave[loc] == ROCK:
        new_cave[loc] = ROCK
cave = new_cave

print('Part Two: {0} units of sand fell before backing up to the source.'.format(pour_sand(cave, deepest_point, bottomless=False)))
