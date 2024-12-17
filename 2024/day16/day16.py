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

tours = [([start], 0, 0)]
all_best_paths = set()
tick = 0
while len(tours) > 0:
    tours_next = []
    search_set = set()
    for (visited, d, score) in tours:
        # ([a, b, c], d, score)
        pos = visited[-1]
        d_next = [(d - 1) % len(DIRS), d, (d + 1) % len(DIRS)]
        score_next = [1001, 1, 1001]
        neighbors = [((pos[0] + DIRS[d_next[i]][0], pos[1] + DIRS[d_next[i]][1]), d_next[i], score_next[i]) for i in range(len(d_next))]
        neighbors = [n for n in neighbors if n[0] not in visited and maze[n[0]] != WALL]
#        print(d_next)
#        print(score_next)
#        print(neighbors)
        for n, n_d, n_score in neighbors:
            if score + n_score <= best_score:
                doubles = False
                if (n, n_d, score + n_score) in search_set:
                    for i in range(len(tours_next)):
                        v, tnd, sc = tours_next[i]
                        if v[-1] == n and tnd == n_d and sc == score + n_score:
                            #print('double match found @ {0} {1} {2}'.format(n, n_d, score + n_score))
                            doubles = True
                            tours_next[i] = (list(set(v) | set(visited)) + [n], tnd, sc)
                            #print(tours_next[i])
                            break
                if not doubles:
                    tours_next.append((visited + [n], n_d, score + n_score))
                    search_set.add((n, n_d, score + n_score))
                    #print(tours_next[-1])

    tours = tours_next
    if len(tours) > 0: print(tick, len(tours), len(all_best_paths))
    for visited, d, score in tours:
        if visited[-1] == end and score == best_score:
            for space in visited: all_best_paths.add(space)
    tick += 1


print(len(all_best_paths))
