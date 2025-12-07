#!/usr/bin/env python
# -*- coding: utf-8 -*-

START = 'S'
SPLITTER = '^'

# Parse the tachyon manifold diagram
with open('day07_input.txt') as f:
    manifold = [line.rstrip('\n') for line in f]

splits = 0
beams = {(0, manifold[0].find(START)): 1}
for row in range(len(manifold) - 1):
    beams_next = {}
    for (row, col) in beams:
        # Tachyon beams pass freely through empty space (.). However, if a tachyon beam encounters
        # a splitter (^), the beam is stopped; instead, a new tachyon beam continues from the
        # immediate left and from the immediate right of the splitter.
        if manifold[row + 1][col] == SPLITTER:
            # With a quantum tachyon manifold, only a single tachyon particle is sent through the manifold.
            # A tachyon particle takes both the left and right path of each splitter encountered.
            beams_next[(row + 1, col - 1)] = beams_next.get((row + 1, col - 1), 0) + beams[(row, col)]
            beams_next[(row + 1, col + 1)] = beams_next.get((row + 1, col + 1), 0) + beams[(row, col)]
            splits += 1
        else:
            # Tachyon beams always move downward.
            beams_next[(row + 1, col)] = beams_next.get((row + 1, col), 0) + beams[(row, col)]
    beams = beams_next

# Analyze your manifold diagram. How many times will the beam be split?
print('Part One: The beam will be split {0} times.'.format(splits))

# Apply the many-worlds interpretation of quantum tachyon splitting to your
# manifold diagram. In total, how many different timelines would a single
# tachyon particle end up on?
timelines = sum([beams[b] for b in beams])
print('Part Two: The beam will be split {0} times.'.format(timelines))