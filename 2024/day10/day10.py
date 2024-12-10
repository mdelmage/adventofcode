#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Use a negative number to indicate that we've gone off the map.
HEIGHT_OFF_MAP = -1

# A trailhead is any position that starts one or more hiking trails -
# here, these positions will always have height 0.
HEIGHT_TRAILHEAD = 0

# Assembling more fragments of pages, you establish that a trailhead's score
# is the number of 9-height positions reachable from that trailhead via a hiking trail.
HEIGHT_FINISH = 9

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
            if topo[(col, row)] == HEIGHT_TRAILHEAD: trailheads.append((col, row))

trailhead_scores = 0
trailhead_ratings = 0
for trailhead in trailheads:
    # Based on un-scorched scraps of the book, you determine that a good hiking trail is as long as possible
    # and has an even, gradual, uphill slope. For all practical purposes, this means that a hiking trail
    # is any path that starts at height 0, ends at height 9, and always increases by a height of exactly 1
    # at each step.
    height_next = HEIGHT_TRAILHEAD + 1
    trails = set([trailhead])
    while height_next <= HEIGHT_FINISH:
        trails_next = set()
        for trail in trails:
            # Determine which neighbors are on the topo map and are one level up.
            # If we find any, add them to the list of trails we're navigating.
            for n in NEIGHBORS:
                neighbor = (trail[-2] + n[0], trail[-1] + n[1])
                if topo.get(neighbor, HEIGHT_OFF_MAP) == height_next:
                    trails_next.add(trail + neighbor)
        # Continue the search at the next level.
        trails = trails_next
        height_next += 1

    # For the trails that we navigated, determine how many unique peaks there were.
    # These will be added up for the Part One score.
    summits = set()
    for trail in trails:
        summits.add((trail[-2], trail[-1]))
    trailhead_scores += len(summits)

    # Add the number of trails that we navigated to the ratings.
    # These will be added up for the Part Two score.
    trailhead_ratings += len(trails)

# The reindeer gleefully carries over a protractor and adds it to the pile.
# What is the sum of the scores of all trailheads on your topographic map?
print('Part One: The sum of trailhead scores is {0}.'.format(trailhead_scores))

# You're not sure how, but the reindeer seems to have crafted some tiny flags out of toothpicks
# and bits of paper and is using them to mark trailheads on your topographic map.
# What is the sum of the ratings of all trailheads?
print('Part Two: The sum of trailhead ratings is {0}.'.format(trailhead_ratings))