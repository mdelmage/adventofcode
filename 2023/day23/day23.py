#!/usr/bin/env python
# -*- coding: utf-8 -*-

# There's a map of nearby hiking trails (your puzzle input) that indicates
# paths (.), forest (#), and steep slopes (^, >, v, and <).
PATH   = '.'
FOREST = '#'
SLOPES = ['^', '>', 'v', '<']

NORTH = ( 0, -1)
SOUTH = ( 0,  1)
WEST  = (-1,  0)
EAST  = ( 1,  0)
NEIGHBORS = [NORTH, SOUTH, WEST, EAST]

NODE_START = 0
NODE_GOAL  = 1

def reset():
    global trails
    trails = {}
    for row in range(len(rows)):
        for col in range(len(rows[0])):
            trails[(col, row)] = rows[row][col]

# Recursive scan of nodes, keeping track of where we've already visited.
def hike(visited, remaining, hike_length, almost_goal, goal):
    loc = visited[-1]
    if loc == goal:
        # We've reached the goal; we're done! Bail out!

        global longest_hike
        if hike_length > longest_hike:
            # We have a new longest hike; remember that.
            longest_hike = hike_length
        return

    if loc == almost_goal:
        # Shortcut to the goal if we reach the...almost-goal.
        neighbors = [goal]
    else:
        # What other nodes can we visit that we haven't already?
        neighbors = [dest for (src, dest) in graph if src == loc and dest not in visited]
    for n in neighbors:
        # Recurse down!
        hike(visited + [n], [r for r in remaining if n != r], hike_length + graph[(loc, n)], almost_goal, goal)

# Parse the hiking trails.
with open('day23_input.txt') as f:
    rows = [line.rstrip('\n') for line in f]

    trails = {}
    for row in range(len(rows)):
        for col in range(len(rows[0])):
            trails[(col, row)] = rows[row][col]

# You're currently on the single path tile in the top row;
# your goal is to reach the single path tile in the bottom row.
#
# Yes, this could have just been done by inspection, but where's the fun in that?
start = [(x, y) for (x, y) in trails if y == 0 and trails[(x, y)] == PATH][0]
goal = [(x, y) for (x, y) in trails if y == len(rows) - 1 and trails[(x, y)] == PATH][0]

# Traverse the trails a bunch. This is not a good ending condition, but hey.
run = 0
longest_hike = 0
while run < 1000:
    reset()
    pos = start
    trails[pos] = 0
    hike_length = 0
    locations = [start]
    choice = 0
    while len(locations) > 0:
        hike_length += 1
        locations_next = []
        for l in locations:
            for n in NEIGHBORS:
                l_next = (l[0] + n[0], l[1] + n[1])
                tile = trails.get(l_next, FOREST)
                if tile == PATH:
                    trails[l_next] = hike_length
                    locations_next.append(l_next)
                elif (tile == '^' and n == NORTH) or \
                     (tile == 'v' and n == SOUTH) or \
                     (tile == '<' and n == WEST)  or \
                     (tile == '>' and n == EAST):
                    trails[l_next] = hike_length
                    locations_next.append(l_next)
        locations = locations_next

        # Choose where to go based on a hash of the run number.
        if len(locations) > 1:
            c = (run >> choice) % 2
            choice += 1
            locations = [locations[c]]

    run += 1
    if isinstance(trails[goal], int): longest_hike = max(longest_hike, trails[goal])

# Find the longest hike you can take through the hiking trails listed on your map.
# How many steps long is the longest hike?
print('Part One: The longest hike is {0} steps.'.format(longest_hike))

# Start Part Two by generating a consolidated graph of the input.
# Nodes are any tiles that have more than one decision to make after we arrive there.
# And, of course, our starting and ending tiles.
reset()
nodes = [start, goal]
for l in trails:
    slopes = 0
    for x in [(l[0] + n[0], l[1] + n[1]) for n in NEIGHBORS]:
        if trails[l] == PATH and trails.get(x, FOREST) in SLOPES: slopes += 1
    if slopes > 1: nodes.append(l)

# Now that we have our nodes, calculate the distance between each one.
graph = {}
for d in nodes:
    reset()
    locs = [d]
    trails[d] = 0
    path_length = 0

    while len(locs) > 0:
        path_length += 1
        neighbors_filtered = set()
        for l in locs:
            neighbors = [(l[0] + n[0], l[1] + n[1]) for n in NEIGHBORS]
            for n in [n for n in neighbors if trails.get(n, FOREST) == PATH or trails.get(n, FOREST) in SLOPES]:
                if n in nodes:
                    graph[(nodes.index(d), nodes.index(n))] = path_length
                    graph[(nodes.index(n), nodes.index(d))] = path_length
                else:
                    neighbors_filtered.add(n)
                    trails[n] = path_length

        locs = neighbors_filtered

# By inspection: there's only one node connected to the goal, so if we land on it,
# we must visit the goal next. That's because of the no-repeats rule.
#
# Because the almost-goal has three connections in our input, and we've already entered
# from one connection, we only could have chosen from two output connections, so this
# should give us an (almost) 2x speedup.
almost_goal = [src for (src, dest) in graph if dest == NODE_GOAL][0]

# Start hiking! At the start, we haven't gone any distance, we've visited only the
# starting node, and the rest of the nodes are remaining to be explored.
longest_hike = 0
visited = [NODE_START]
remaining = [n for n in range(1, len(nodes))]
hike(visited, remaining, NODE_START, almost_goal, NODE_GOAL)

# Find the longest hike you can take through the surprisingly dry hiking trails listed on your map.
# How many steps long is the longest hike?
print('Part Two: The longest hike (including going up slopes) is {0} steps.'.format(longest_hike))