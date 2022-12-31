#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The walls of the valley are drawn as #; everything else is ground.
# Clear ground - where there is currently no blizzard - is drawn as ..
# Otherwise, blizzards are drawn with an arrow indicating their direction
# of motion: up (^), down (v), left (<), or right (>).
WALL = '#'
GROUND = '.'
BLIZZARDS = ['^', 'v', '<', '>']

DIRECTIONS = { '^': ( 0, -1),
               'v': ( 0,  1),
               '<': (-1,  0),
               '>': ( 1,  0),
               '.': ( 0,  0)}

# Parse the valley and blizzards map file
with open('day24_input.txt') as f:
    valley_list = [line.rstrip('\n')for line in f]

# Convert the list to a dict
blizzards = []
walls = []
valley = {}
for row in range(len(valley_list)):
    for col in range(len(valley_list[row])):
        if valley_list[row][col] in BLIZZARDS:
            blizzards.append((valley_list[row][col], (col, row)))
        elif valley_list[row][col] == WALL:
            walls.append((col, row))

# Determine the starting point
for col in range(len(valley_list[0])):
    if valley_list[0][col] == GROUND:
        pos_start = (col, 0)

        # Add an additional wall so we don't pathfind out of the starting area.
        walls.append((col, -1))
        break

# Determine the ending (goal) point
for col in range(len(valley_list[0])):
    if valley_list[len(valley_list) - 1][col] == GROUND:
        goal = (col, len(valley_list) - 1)

        # Add an additional wall so we don't pathfind past the goal.
        walls.append((goal[0], goal[1] + 1))
        break

# Track three things:
# 1. position;
# 2. having reached the goal the first time;
# 3. having gone back to the start.
positions = set()
positions.add((pos_start, False, False))

minute = 0
first_goal_reached = False
second_goal_reached = False

while True:
    # Your expedition begins in the only non-wall position in the top row and needs to reach
    # the only non-wall position in the bottom row. On each minute, you can move up, down,
    # left, or right, or you can wait in place. You and the blizzards act simultaneously,
    # and you cannot share a position with a blizzard.

    # ...well, kind of. First, simulate the blizzard moving through the valley, and then
    # let's generate all the possible positions we could be in at that minute.
    next_blizzards = []
    minute += 1

    for item, pos in blizzards:
        d = DIRECTIONS[item]
        next_pos = (pos[0] + d[0], pos[1] + d[1])
        if next_pos in walls:
            next_pos = pos
            while next_pos not in walls:
                next_pos = (next_pos[0] - d[0], next_pos[1] - d[1])
            next_pos = (next_pos[0] + d[0], next_pos[1] + d[1])

        next_blizzards.append((item, next_pos))
    blizzards = next_blizzards

    # Blizzard simulation complete for this minute; now figure out places we could be.
    next_positions = set()
    obstacles = [pos for item, pos in blizzards] + walls
    for direction in DIRECTIONS:
        for pos, first, start in positions:
            d = DIRECTIONS[direction]
            next_pos = (pos[0] + d[0], pos[1] + d[1])
            if next_pos not in obstacles:
                if next_pos == goal and not first:
                    first = True
                    if not first_goal_reached: first_goal_reached = minute
                elif next_pos == pos_start and first:
                    start = True
                elif next_pos == goal and start:
                    second_goal_reached = True
                next_positions.add((next_pos, first, start))
    positions = next_positions

    if second_goal_reached:
        # What is the fewest number of minutes required to avoid the blizzards and reach the goal?
        print('Part One: reached the goal in {0} minutes.'.format(first_goal_reached))

        # What is the fewest number of minutes required to reach the goal,
        # go back to the start, then reach the goal again?
        print('Part Two: reached the goal (again) in {0} minutes.'.format(minute))
        break
