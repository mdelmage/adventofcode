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

# Traverse the maze via flood-fill, a time-honored AoC tradition.
# This one tracks the best score per tile, for each direction you entered via.
maze[start] = {d: 0}
just_visited = [(start, d, 0)]
while len(just_visited) > 0:
    visit_next = just_visited
    just_visited = []
    for (pos, d, score) in visit_next:
        # They can move forward one tile at a time (increasing their score by 1 point),
        # but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time
        # (increasing their score by 1000 points).
        for d_next, score_next in [(d, 1), ((d - 1) % len(DIRS), 1001), ((d + 1) % len(DIRS), 1001)]:
            vel = DIRS[d_next]
            pos_next = (pos[0] + vel[0], pos[1] + vel[1])
            neighbor = maze[pos_next]

            # Record the best score for the new tile/direction.
            if neighbor != WALL and neighbor.get(d, score + 1) > score:
                neighbor[d] = score + score_next
                just_visited.append((pos_next, d_next, score + score_next))

# Find the best score for the ending tile.
best_score = maze[end][0]
for d in maze[end]:
    best_score = min(best_score, maze[end][d])

# Analyze your map carefully. What is the lowest score a Reindeer could possibly get?
print('Part One: The best path has a score of {0}.'.format(best_score))

# Now that you know what the best paths look like, you can figure out the best spot to sit.
#
# Every non-wall tile (S, ., or E) is equipped with places to sit along the edges of the tile.
# While determining which of these tiles would be the best spot to sit depends on a whole bunch of factors
# (how comfortable the seats are, how far away the bathrooms are, whether there's a pillar blocking your view,
# etc.), the most important factor is whether the tile is on one of the best paths through the maze. If you sit
# somewhere else, you'd miss all the action!
#
# So, you'll need to determine which tiles are part of any best path through the maze, including the S and E tiles.
all_best_paths = set()
tours = [([start], 0, 0)]
while len(tours) > 0:
    tours_next = []
    search_set = set()
    for (visited, d, score) in tours:
        # They can move forward one tile at a time (increasing their score by 1 point),
        # but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time
        # (increasing their score by 1000 points).
        pos = visited[-1]
        next_d_score = [(d, 1), ((d - 1) % len(DIRS), 1001), ((d + 1) % len(DIRS), 1001)]
        neighbors = [((pos[0] + DIRS[d][0], pos[1] + DIRS[d][1]), d, score) for d, score in next_d_score]
        neighbors = [n for n in neighbors if n[0] not in visited and maze[n[0]] != WALL]

        # Try to prune the search space by looking for neighbors that have the same score and direction
        # as a path we've already explored.
        # If we find one, just add that path to ours.
        for n, n_d, n_score in neighbors:
            if score + n_score <= best_score:
                doubles = False
                if (n, n_d, score + n_score) in search_set:
                    for i in range(len(tours_next)):
                        v, tnd, sc = tours_next[i]
                        if v[-1] == n and tnd == n_d and sc == score + n_score:
                            # Found a previously-explored path; add our path's tiles to theirs.
                            tours_next[i] = (list(set(v) | set(visited)) + [n], tnd, sc)
                            doubles = True
                            break

                if not doubles:
                    # Not a previously-explored path, so explore further.
                    tours_next.append((visited + [n], n_d, score + n_score))
                    search_set.add((n, n_d, score + n_score))

    tours = tours_next

    for visited, d, score in tours:
        if visited[-1] == end and score == best_score:
            # Found a tour that is a best path. Save all tiles we used.
            for space in visited: all_best_paths.add(space)

# Analyze your map further. How many tiles are part of at least one of the best paths through the maze?
print('Part Two: The best paths through the maze contain {0} tiles.'.format(len(all_best_paths)))