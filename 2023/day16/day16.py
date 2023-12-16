#!/usr/bin/env python
# -*- coding: utf-8 -*-

LEFT  = (-1,  0)
RIGHT = ( 1,  0)
UP    = ( 0, -1)
DOWN  = ( 0,  1)

SPACE       = '.'
MIRRORS     = ['/', '\\']
MIRROR_SW   = '/'
MIRROR_SE   = '\\'
SPLITTERS   = ['|', '-']
SPLITTER_NS = '|'
SPLITTER_WE = '-'

# If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending
# on the angle of the mirror. For instance, a rightward-moving beam that encounters
# a / mirror would continue upward in the mirror's column, while a rightward-moving beam
# that encounters a \ mirror would continue downward from the mirror's column.
MIRROR_MAP = {(MIRROR_SW, LEFT): DOWN,
              (MIRROR_SW, RIGHT): UP,
              (MIRROR_SW, UP): RIGHT,
              (MIRROR_SW, DOWN): LEFT,

              (MIRROR_SE, LEFT): UP,
              (MIRROR_SE, RIGHT): DOWN,
              (MIRROR_SE, UP): LEFT,
              (MIRROR_SE, DOWN): RIGHT}

SPLITTER_MAP = {
                # If the beam encounters the pointy end of a splitter (| or -), the beam passes through
                # the splitter as if the splitter were empty space. For instance, a rightward-moving beam
                # that encounters a - splitter would continue in the same direction.
                (SPLITTER_NS, UP): [UP],
                (SPLITTER_NS, DOWN): [DOWN],
                (SPLITTER_WE, LEFT): [LEFT],
                (SPLITTER_WE, RIGHT): [RIGHT],

                # If the beam encounters the flat side of a splitter (| or -), the beam is split into two
                # beams going in each of the two directions the splitter's pointy ends are pointing.
                # For instance, a rightward-moving beam that encounters a | splitter would split into two beams:
                # one that continues upward from the splitter's column and one that continues downward from
                # the splitter's column.
                (SPLITTER_NS, LEFT): [UP, DOWN],
                (SPLITTER_NS, RIGHT): [UP, DOWN],
                (SPLITTER_WE, UP): [LEFT, RIGHT],
                (SPLITTER_WE, DOWN): [LEFT, RIGHT]}

def shine_light(entry):
    # Beams do not interact with other beams; a tile can have many beams passing through it
    # at the same time. A tile is energized if that tile has at least one beam pass through it,
    # reflect in it, or split in it.
    energized = set()

    history = set()
    beams = set([entry])
    while len(beams) > 0:
        beams_next = set()
        for (x, y, d) in beams:
            x_next = x + d[0]
            y_next = y + d[1]
            if x_next >= 0 and x_next < len(contraption[0]) and y_next >= 0 and y_next < len(contraption):
                tile = contraption[y_next][x_next]
                energized.add((x_next, y_next))

                if tile == SPACE:
                    beams_next.add((x_next, y_next, d))
                elif tile in MIRRORS:
                    beams_next.add((x_next, y_next, MIRROR_MAP[(tile, d)]))
                elif tile in SPLITTERS:
                    dirs = SPLITTER_MAP[(tile, d)]
                    for d_next in dirs:
                        beams_next.add((x_next, y_next, d_next))

        # Because of how splitters work, there can be ways to generate infinitely looping light beams.
        # To detect this, remember every previous state we've encountered, and stop processing a beam
        # if its location and direction have been previously seen.
        beams = set()
        for b in beams_next:
            if b not in history:
                history.add(b)
                beams.add(b)

    return len(energized)

# Parse the contraption layout.
with open('day16_input.txt') as f:
    contraption = [line.rstrip('\n') for line in f]

# The beam enters in the top-left corner from the left and heading to the right.
entry = (-1, 0, RIGHT)

# The light isn't energizing enough tiles to produce lava; to debug the contraption,
# you need to start by analyzing the current situation. With the beam starting in the
# top-left heading right, how many tiles end up being energized?
print('Part One: {0} tiles end up being energized.'.format(shine_light(entry)))

# As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you
# to a nearby control panel. There, a collection of buttons lets you align the contraption
# so that the beam enters from any edge tile and heading away from that edge.
#
# So, the beam could start on any tile in the top row (heading downward), any tile in
# the bottom row (heading upward), any tile in the leftmost column (heading right), or
# any tile in the rightmost column (heading left). To produce lava, you need to find
# the configuration that energizes as many tiles as possible.
best_energy = 0
for i in range(len(contraption)):
    best_energy = max(best_energy, shine_light((-1, i, RIGHT)))
    best_energy = max(best_energy, shine_light((len(contraption), i, LEFT)))
    best_energy = max(best_energy, shine_light((i, -1, DOWN)))
    best_energy = max(best_energy, shine_light((i, len(contraption), UP)))

# Find the initial beam configuration that energizes the largest number of tiles;
# how many tiles are energized in that configuration?
print('Part Two: Most energized configuration was {0}.'.format(best_energy))