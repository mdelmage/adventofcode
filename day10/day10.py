#!/usr/bin/python

import copy

SYMBOL_ASTEROID    = '#'
SYMBOL_EMPTY_SPACE = '.'

# Shamelessly lifted from:
# https://stackoverflow.com/questions/11175131/code-for-greatest-common-divisor-in-python/11175154
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

# Open input file
filename = "day10.txt"
f = open(filename, "r")

asteroids = set()
observations = {}

with open(filename, "r") as f:
    row = 0
    for line in f:
        for col in range(len(line.strip())):
            if SYMBOL_ASTEROID == line[col]:
                asteroids.add((col, row))
        row += 1

    for a in asteroids:
        neighbors = copy.deepcopy(asteroids)
        neighbors.remove(a)
        angles = set()

        # Reduce each neighbor to its GCD direction from us.
        # Honor absolute direction (use absolute value for GCD).
        # Example: (-150, -100) --> (-3, -2)
        for n in neighbors:
            dist = (n[0] - a[0], n[1] - a[1])
            denom = abs(gcd(dist[0], dist[1]))
            angles.add((dist[0] / denom, dist[1] / denom))
        observations[(a[0], a[1])] = len(angles)

    best_observations = sorted(observations.items(), reverse=True, key=lambda x: x[1])
    print "Best observation station is at {0} with {1} asteroids visible.".format(best_observations[0][0], best_observations[0][1])
