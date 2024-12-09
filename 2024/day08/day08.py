#!/usr/bin/env python
# -*- coding: utf-8 -*-

SPACE = '.'

# Parse the antenna map.
with open('day08_input.txt') as f:
    m = [line.rstrip('\n')for line in f]
    # Build a dict of antennas, by frequency.
    antennas = {}
    for row in range(len(m)):
        for col in range(len(m[0])):
            if m[row][col] != SPACE:
                a = m[row][col]
                if a not in antennas: antennas[a] = []
                antennas[a].append((col, row))

# The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies
# of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two
# antennas of the same frequency - but only when one of the antennas is twice as far away as the other.
# This means that for any pair of antennas with the same frequency, there are two antinodes, one on
# either side of them.
antinodes = set()
for a in antennas:
    # Generate every combination of antenna pairings, for every frequency.
    for (l1, l2) in [(l1, l2) for l1 in antennas[a] for l2 in antennas[a] if l1 != l2]:
        antinode = (l2[0] + l2[0] - l1[0], l2[1] + l2[1] - l1[1])
        # If the antinode inside the bounds of the map, add it.
        if antinode[0] >= 0 and antinode[0] < len(m) and antinode[1] >= 0 and antinode[1] < len(m):
            antinodes.add(antinode)

# Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?
print('Part One: There are {0} antinodes within the bounds of the map.'.format(len(antinodes)))

# Whoops!
#
# After updating your model, it turns out that an antinode occurs at any grid position exactly in line
# with at least two antennas of the same frequency, regardless of distance. This means that some of the
# new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).
antinodes = set()
for a in antennas:
    # Generate every combination of antenna pairings, for every frequency.
    for (l1, l2) in [(l1, l2) for l1 in antennas[a] for l2 in antennas[a] if l1 != l2]:
        # Now generate a line of antinodes instead of just one.
        # The number of antinodes generated is complete overkill, but isn't too unperformant
        # for the given puzzle input size.
        for i in range(len(m)):
            # Generate the 'i-th' antinode away.
            delta = (l2[0] - l1[0], l2[1] - l1[1])
            antinode = (l1[0] + (i * delta[0]), l1[1] + (i * delta[1]))
            if antinode[0] >= 0 and antinode[0] < len(m) and antinode[1] >= 0 and antinode[1] < len(m):
                antinodes.add(antinode)

# Calculate the impact of the signal using this updated model.
# How many unique locations within the bounds of the map contain an antinode?
print('Part Two: There are {0} antinodes within the bounds of the map.'.format(len(antinodes)))