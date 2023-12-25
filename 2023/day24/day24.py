#!/usr/bin/env python
# -*- coding: utf-8 -*-

# However, you'll need to search a much larger test area if you want to see if any hailstones
# might collide. Look for intersections that happen with an X and Y position each at least
# 200000000000000 and at most 400000000000000. Disregard the Z axis entirely.
WINDOW = (200000000000000, 400000000000000)

def test_intersection(h1, h2):
    pos1, vel1 = h1
    pos2, vel2 = h2

    # mx + b all up in here, so specifically: ax + c = bx + d.
    # This is also called slope-intercept notation.
    a = vel1[1] / vel1[0]
    b = vel2[1] / vel2[0]

    if a == b:
        # Hailstones have the same slope, so will never intersect.
        return False

    # Given the slopes and the pos/vel data, determine the X-intercepts.
    c = pos1[1] - (pos1[0] / vel1[0]) * vel1[1]
    d = pos2[1] - (pos2[0] / vel2[0]) * vel2[1]

    # Determine the intersection point.
    # Reference: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    intersection_x = (d - c) / (a - b)
    intersection_y = a * (d - c) / (a - b) + c

    if (intersection_x < pos1[0] or vel1[0] < 0) and (intersection_x > pos1[0] or vel1[0] > 0):
        # Intersection occurs in the past for Hailstone 1; bail out.
        return False

    if (intersection_x < pos2[0] or vel2[0] < 0) and (intersection_x > pos2[0] or vel2[0] > 0):
        # Intersection occurs in the past for Hailstone 2; bail out.
        return False

    if intersection_x < WINDOW[0] or intersection_x > WINDOW[1] or \
       intersection_y < WINDOW[0] or intersection_y > WINDOW[1]:
        # Intersection occurs in the future, but outside the test area. Nope.
        return False

    # All good! Intersection is in the future for both hailstones, and inside the test area.
    return True

# Parse the hailstone notes.
with open('day24_input.txt') as f:
    rows = [line.rstrip('\n').split(' @ ') for line in f]

    hailstones = []
    for pos, vel in rows:
        pos = [int(n) for n in pos.split(',')]
        vel = [int(n) for n in vel.split(',')]
        hailstones.append((pos, vel))

# Perhaps you won't have to do anything. How likely are the hailstones to collide
# with each other and smash into tiny ice crystals?
#
# To estimate this, consider only the X and Y axes; ignore the Z axis. Looking forward
# in time, how many of the hailstones' paths will intersect within a test area?
valid_intersections = 0
for n1, n2 in [(n1, n2) for n1 in range(len(hailstones)) for n2 in range(len(hailstones)) if n1 < n2]:
    if test_intersection(hailstones[n1], hailstones[n2]): valid_intersections += 1

# Considering only the X and Y axes, check all pairs of hailstones' future paths for intersections.
# How many of these intersections occur within the test area?
print('Part One: The number of future intersections inside the test area is {0}.'.format(valid_intersections))