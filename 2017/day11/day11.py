#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The hexagons ("hexes") in this grid are aligned such that adjacent hexes
# can be found to the north, northeast, southeast, south, southwest, and northwest:
#
#   \ n  /
# nw +--+ ne
#   /    \
# -+      +-
#   \    /
# sw +--+ se
#   / s  \

# Opposite directions cancel out.
CANCEL_PAIRS = [('n', 's'),
                ('sw', 'ne'),
                ('se', 'nw')]

# For each direction, there exists a pair of directions that we can optimize
# down to that single direction.
REDUCE_PAIRS = {('nw', 'ne') :  'n',
                ('sw', 'se') :  's',
                ('nw',  's') : 'sw',
                ('ne',  's') : 'se',
                ('sw',  'n') : 'nw',
                ('se',  'n') : 'ne'}

def optimize():
    done = False

    while not done:
        done = True
        steps_away = sum(moves.values())

        # Remove the directly-cancelling moves.
        for (d1, d2) in CANCEL_PAIRS:
            cancels = min(moves[d1], moves[d2])
            moves[d1] -= cancels
            moves[d2] -= cancels

        # Simplify any pairs to single moves.
        for (d1, d2) in REDUCE_PAIRS:
            cancels = min(moves[d1], moves[d2])
            moves[d1] -= cancels
            moves[d2] -= cancels
            moves[REDUCE_PAIRS[(d1, d2)]] += cancels

        # If the number of moves went down, we're not done yet.
        if sum(moves.values()) < steps_away: done = False
    
# Parse the hexagonal moves, and save each line
with open('day11_input.txt') as f:
    moves_list = [line.rstrip('\n').rstrip(')') for line in f]

for m in moves_list:
    max_dist = 0
    moves = {'n': 0,
             's': 0,
             'nw': 0,
             'sw': 0,
             'ne': 0,
             'se': 0}

    for d in m.split(','):
        moves[d] = moves.get(d, 0) + 1
        optimize()
        dist = sum(moves.values())
        max_dist = max(max_dist, dist)

    print 'Part One: the fewest steps required is {0}.'.format(dist)
    print 'Part Two: the furthest steps away was {0}.'.format(max_dist)