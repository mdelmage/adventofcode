#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The robots outside the actual bathroom are in a space which is 101 tiles wide
# and 103 tiles tall (when viewed from above).
WIDTH = 101
HEIGHT = 103

def safety_factor():
    quadrant_product = 1
    quadrant_map = {}

    for pos, vel in robots:
        # Robots that are exactly in the middle (horizontally or vertically)
        # don't count as being in any quadrant.
        if pos[0] * 2 == WIDTH - 1: continue
        if pos[1] * 2 == HEIGHT - 1: continue

        quadrant = (pos[0] < WIDTH / 2, pos[1] < HEIGHT / 2)
        quadrant_map[quadrant] = quadrant_map.get(quadrant, 0) + 1

    # Safety factor is the product of the robots counts in each quadrant.
    for q in quadrant_map:
        quadrant_product *= quadrant_map[q]

    return(quadrant_product)

# Parse the list of the robots' current positions and velocities.
with open('day14_input.txt') as f:
    robots = [line.rstrip('\n').replace('p=','').replace(' v=', ',') for line in f]

robots_next = []
for robot in robots:
    # Extract position and velocity for each robot.
    pv = [int(n) for n in robot.split(',')]
    robots_next.append(((pv[0], pv[1]), (pv[2], pv[3])))
robots = robots_next

# By inspection, the robot positions loop every WIDTH * HEIGHT ticks.
# So we only need to search in that space.
min_safety_factor = None
tree_tick = None
for tick in range(1, WIDTH * HEIGHT):
    # Iterate for this tick by adding each robot's velocity to its position.
    robots_next = []
    for pos, vel in robots:
        robots_next.append((((pos[0] + vel[0]) % WIDTH, (pos[1] + vel[1]) % HEIGHT), vel))
    robots = robots_next

    # Find the Christmas tree by looking for the lowest safety factor, which is an analog
    # for entropy. This isn't guaranteed to work on all inputs, but it did work for mine.
    s = safety_factor()
    if not min_safety_factor: min_safety_factor = s
    if s < min_safety_factor:
        min_safety_factor = s
        tree_tick = tick

    if tick == 100:
        # Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall.
        # What will the safety factor be after exactly 100 seconds have elapsed?
        print('Part One: The safety factor after 100 seconds is {0}.'.format(safety_factor()))

# During the bathroom break, someone notices that these robots seem awfully similar to ones built
# and used at the North Pole. If they're the same type of robots, they should have a hard-coded Easter egg:
# very rarely, most of the robots should arrange themselves into a picture of a Christmas tree.
#
# What is the fewest number of seconds that must elapse for the robots to display the Easter egg?
print('Part Two: The Easter egg is displayed after {0} seconds.'.format(tree_tick))
