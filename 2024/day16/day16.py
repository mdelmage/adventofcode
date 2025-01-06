#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E).
# They can move forward one tile at a time (increasing their score by 1 point), but never into a wall (#).
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
            if maze_list[row][col] == START: start = (col, row)
            if maze_list[row][col] == END: end = (col, row)

# The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E).
# Set direction to DIRS[0] == EAST.
d = 0
visited = {(start, d): (0, set([start]))}
tours = {(start, d): (0, set([start]))}
while len(tours) > 0:
    # Flood the maze (indexing by location AND direction, instead of just the usual location).
    # Record the best score for each loc/dir pair, and save the path histories as well.
    tours_next = {}
    for loc, d in tours:
        score, loc_history = tours[(loc, d)]
        for d_next, score_added in [(d, 1), ((d - 1) % len(DIRS), 1001), ((d + 1) % len(DIRS), 1001)]:
            loc_next = (loc[0] + DIRS[d_next][0], loc[1] + DIRS[d_next][1])
            if maze.get(loc_next, WALL) != WALL:
                score_next = score + score_added
                score_check, loc_history_check = visited.get((loc_next, d_next), (score_next + 1, set()))
                if score_next < score_check:
                    # First/better tour of this location was found. Record it! Overwrite any older tour info.
                    visited[(loc_next, d_next)] = (score_next, loc_history | set([loc_next]))
                    tours_next[(loc_next, d_next)] = (score_next, loc_history | set([loc_next]))
                elif score_next == score_check:
                    # Identical (best) score of this location found; merge our tour history with theirs.
                    old_loc_history = tours_next[(loc_next, d_next)][1]
                    if len(old_loc_history ^ loc_history) > 0:
                        # Of course, only merge if it would actually add a new path to the tour.
                        visited[(loc_next, d_next)] = (score_next, old_loc_history | loc_history | set([loc_next]))
                        tours_next[(loc_next, d_next)] = (score_next, old_loc_history | loc_history | set([loc_next]))
    tours = tours_next

# Now that you know what the best paths look like, you can figure out the best spot to sit.
#
# Every non-wall tile (S, ., or E) is equipped with places to sit along the edges of the tile.
# While determining which of these tiles would be the best spot to sit depends on a whole bunch of factors
# (how comfortable the seats are, how far away the bathrooms are, whether there's a pillar blocking your view,
# etc.), the most important factor is whether the tile is on one of the best paths through the maze. If you sit
# somewhere else, you'd miss all the action!
#
# So, you'll need to determine which tiles are part of any best path through the maze, including the S and E tiles.
best_score = None
best_paths_count = None
for d in range(len(DIRS)):
    score, tour = visited.get((end, d), (None, 0))
    if score and (not best_score or score < best_score):
        best_score = score
        best_paths_count = len(tour)

# Analyze your map carefully. What is the lowest score a Reindeer could possibly get?
print('Part One: The best path has a score of {0}.'.format(best_score))

# Analyze your map further. How many tiles are part of at least one of the best paths through the maze?
print('Part Two: The best paths through the maze contain {0} tiles.'.format(best_paths_count))