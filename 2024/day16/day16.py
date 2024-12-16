#!/usr/bin/env python
# -*- coding: utf-8 -*-

START = 'S'
END   = 'E'
SPACE = '.'
WALL  = '#'

NORTH = (0, -1)
SOUTH = (0,  1)
WEST  = (-1, 0)
EAST  = ( 1, 0)

DIRS = [EAST, SOUTH, WEST, NORTH]

# Parse the Reindeer Maze map.
with open('day16_input.txt') as f:
    maze_list = [line.rstrip('\n') for line in f]
    maze = {}
    for row in range(len(maze_list)):
        for col in range(len(maze_list[0])):
            if maze_list[row][col] in [SPACE, START, END]:
                maze[(col, row)] = {}
            else:
                maze[(col, row)] = maze_list[row][col]
            if maze_list[row][col] == START: pos = (col, row)
            if maze_list[row][col] == END: end = (col, row)

# The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E).
# Set direction to DIRS[0] == EAST.
d = 0

# Traverse the maze via flood-fill, a time-honored AoC tradition.
# This one tracks the best score per tile, for each direction you entered via.
maze[pos] = {d: 0}
just_visited = [(pos, d, 0)]
while len(just_visited) > 0:
    visit_next = just_visited
    just_visited = []
    for (pos, d, score) in visit_next:
        vel = DIRS[d]
        pos_noturn = (pos[0] + vel[0], pos[1] + vel[1])
        neighbor = maze[pos_noturn]
        if neighbor != WALL:
            if d not in neighbor or neighbor[d] > score:
                neighbor[d] = score + 1
                just_visited.append((pos_noturn, d, score + 1))

        d_left = (d - 1) % len(DIRS)
        vel_left = DIRS[d_left]
        pos_turnleft = (pos[0] + vel_left[0], pos[1] + vel_left[1])
        neighbor = maze[pos_turnleft]
        if neighbor != WALL:
            if d not in neighbor or neighbor[d] > score:
                neighbor[d] = score + 1001
                just_visited.append((pos_turnleft, d_left, score + 1001))

        d_right = (d + 1) % len(DIRS)
        vel_right = DIRS[d_right]
        pos_turnright= (pos[0] + vel_right[0], pos[1] + vel_right[1])
        neighbor = maze[pos_turnright]
        if neighbor != WALL:
            if d not in neighbor or neighbor[d] > score:
                neighbor[d] = score + 1001
                just_visited.append((pos_turnright, d_right, score + 1001))


best_score = 999999999999999999
for d in maze[end]:
    best_score = min(best_score, maze[end][d])

# Analyze your map carefully. What is the lowest score a Reindeer could possibly get?
print('Part One: The best path has a score of {0}.'.format(best_score))
