#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use a negative number to indicate that we've gone off the map.
OFF_MAP = -1

# A trailhead is any position that starts one or more hiking trails -
# here, these positions will always have height 0.
TRAILHEAD = 0

# Assembling more fragments of pages, you establish that a trailhead's score
# is the number of 9-height positions reachable from that trailhead via a hiking trail.
FINISH = 9

# Hiking trails never include diagonal steps - only up, down, left, or right
# (from the perspective of the map).
NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Parse the topographic map.
with open('day10_input.txt') as f:
    t = [line.rstrip('\n') for line in f]

    # Convert the list to a dict. Find all the trailheads.
    topo = {}
    trailheads = []
    for row in range(len(t)):
        for col in range(len(t[0])):
            topo[(col, row)] = int(t[row][col])
            if topo[(col, row)] == TRAILHEAD: trailheads.append((col, row))

trailhead_scores = 0
for trailhead in trailheads:
    next_level = TRAILHEAD + 1
    trails = set([trailhead])
    while next_level <= FINISH:
        trails_next = set()
        for trail in trails:
            for n in NEIGHBORS:
                neighbor = (trail[0] + n[0], trail[1] + n[1])
                if topo.get(neighbor, OFF_MAP) == next_level:
                    trails_next.add(neighbor)
        trails = trails_next
        next_level += 1
    trailhead_scores += len(trails_next)

# The reindeer gleefully carries over a protractor and adds it to the pile.
# What is the sum of the scores of all trailheads on your topographic map?
print('Part One: The sum of trailhead scores is {0}.'.format(trailhead_scores))