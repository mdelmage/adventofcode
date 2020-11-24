#!/usr/bin/python

import copy
import math
import sys

SYMBOL_ASTEROID    = '#'
SYMBOL_EMPTY_SPACE = '.'

# Shamelessly lifted from:
# https://stackoverflow.com/questions/11175131/code-for-greatest-common-divisor-in-python/11175154
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

# Shamelessly mashed up from:
# https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates
# https://www.mathsisfun.com/polar-cartesian-coordinates.html
def radius(x, y):
    return (x ** 2 + y ** 2) ** .5

def degrees(x, y):
    # Convert to Advent coordinate system
    y *= -1

    theta = math.degrees(math.atan2(y, x))

    if x >= 0 or y < 0:
        return 90 - theta
    else:
        return 360 + 90 - theta

# Open input file
filename = "day10.txt"
f = open(filename, "r")

asteroids = set()
observations = {}
blast_order = {}

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
    best_station = best_observations[0][0]
    asteroids_visible = best_observations[0][1]
    print "Best observation station is at {0} with {1} asteroids visible.".format(best_station, asteroids_visible)

    neighbors = copy.deepcopy(asteroids)
    neighbors.remove(best_station)
    for n in neighbors:
        delta = (n[0] - best_station[0], n[1] - best_station[1])
        angle = round(degrees(delta[0], delta[1]), 6)
        d = radius(delta[0], delta[1])
        if angle not in blast_order:
            blast_order[angle] = {}
        blast_order[angle][d] = n

    # We have a nested dict, ordered first by angle and then by distance.
    # Go around in a circle and start blasting!
    i = 1
    while len(blast_order) > 0:
        for angle in sorted(blast_order):
            print "{0}: Angle {1}".format(i, angle),
            print blast_order[angle][sorted(blast_order[angle])[0]]
            del blast_order[angle][sorted(blast_order[angle])[0]]
            if 0 == len(blast_order[angle]):
                del blast_order[angle]
            i += 1
