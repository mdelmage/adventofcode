#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The tall, vertical chamber is exactly seven units wide.
CHAMBER_WIDTH = 7

# To prove to the elephants your simulation is accurate, they want to know how tall
# the tower will get after 2022 rocks have stopped (but before the 2023rd rock begins falling).
PART_ONE_COUNT = 2022

# The elephants are not impressed by your simulation. They demand to know how tall the tower
# will be after 1000000000000 rocks have stopped! Only then will they feel confident enough
# to proceed through the cave.
PART_TWO_COUNT = 1000000000000

# The five types of rocks have the following peculiar shapes, where # is rock and . is empty space:
#
#  ████
#
#   █ 
#  ███
#   █
#
#    █
#    █
#  ███
#
#  █
#  █
#  █
#  █
#
#  ██
#  ██
# (converted by the author to block Unicode for better readability)

rocks = [[(0, 0), (1, 0), (2, 0), (3, 0)],
         [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
         [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
         [(0, 0), (0, 1), (0, 2), (0, 3)],
         [(0, 0), (1, 0), (0, 1), (1, 1)]]

def left_edge(rock):
    # All rock shapes have an x=0 coordinate
    return 0

def right_edge(rock):
    edge = 0
    for (x, y) in rock:
        if x > edge: edge = x
    return edge

def bottom_edge(rock):
    # All rock shapes have a y=0 coordinate
    return 0

def top_edge(rock):
    edge = 0
    for (x, y) in rock:
        if y > edge: edge = y
    return edge

def collided(rock, offset, chamber):
    for c in rock:
        if (c[0] + offset[0], c[1] + offset[1]) in chamber:
            # Rock collided because it hit some other rock(s)
            return True
        elif c[1] + offset[1]== 0:
            # Rock collided because it hit the chamber floor
            return True
    return False

# Parse the hot gas jets file
with open('day17_input.txt') as f:
    jets = [line.rstrip('\n') for line in f][0]

chamber = {}
tower_height = 0
tick = 0
rock_num = 0

repeat_found = False
experiment_states = {}

while rock_num < PART_TWO_COUNT:
    # The rocks fall in the order shown above: first the - shape, then the + shape, and so on.
    # Once the end of the list is reached, the same order repeats: the - shape falls first,
    # sixth, 11th, 16th, etc.
    rock_idx = rock_num % len(rocks)
    rock = rocks[rock_idx]

    # Each rock appears so that its left edge is two units away from the left wall
    # and its bottom edge is three units above the highest rock in the room
    # (or the floor, if there isn't one).
    offset = (left_edge(rock) + 2, tower_height + bottom_edge(rock) + 3 + 1)

    # After a rock appears, it alternates between being pushed by a jet of hot gas
    # one unit (in the direction indicated by the next symbol in the jet pattern)
    # and then falling one unit down. If any movement would cause any part of the rock
    # to move into the walls, floor, or a stopped rock, the movement instead does not occur.
    # If a downward movement would have caused a falling rock to move into the floor or an
    # already-fallen rock, the falling rock stops where it is (having landed on something)
    # and a new rock immediately begins falling.
    falling = True
    while falling:
        if jets[tick] == '<':
            if left_edge(rock) + offset[0] > 0:
                # Moving left would not hit the left wall
                test_offset = (offset[0] - 1, offset[1])
        else:
            if right_edge(rock) + offset[0] < CHAMBER_WIDTH - 1:
                # Moving right would not hight the right wall
                test_offset = (offset[0] + 1, offset[1])

        # We still need to do further collision testing, as there could be
        # fallen rock that we would hit from the side
        if not collided(rock, test_offset, chamber):
            offset = test_offset

        # Now simulate the rock dropping one unit down and do another collision check
        test_offset = (offset[0], offset[1] - 1)
        if not collided(rock, test_offset, chamber):
            offset = test_offset
        else:
            # Collision! Stop this rock.
            falling = False

            # Add the rock's final coordinates to the chamber mapping.
            for c in rock:
                chamber[(c[0] + offset[0], c[1] + offset[1])] = '█'

            # Recalculate the tower height -- depending on where the rock fell,
            # it may or may not have grown the tower, so it is not sufficient to use
            # the top of the rock as the new tower height.
            tower_height = max(tower_height, top_edge(rock) + offset[1])

        tick = (tick + 1) % len(jets)

    if rock_num > PART_ONE_COUNT and not repeat_found:
        floor_state = ''
        for i in range(10):
            for col in range(CHAMBER_WIDTH):
                floor_state += chamber.get((col, tower_height - i), '.')

        if (tick, rock_idx, floor_state) in experiment_states:
            # We've found a cyclical condition in the rock-dropping experiment!
            # We're dropping the same rock shape, at the same part of the hot gas jets pattern,
            # onto the same floor shape. We can figure out how high the tower grew in this cycle,
            # and then calculate how high the tower would grow over a very large number of drops
            # (in this case, a trillion drops).
            repeat_found = True
            (last_rock_num, last_tower_height) = experiment_states[(tick, rock_idx, floor_state)]

            # Determine the period of the cycle and how high the tower grew, by subtracting the
            # values from the beginning of the cycle.
            period = rock_num - last_rock_num
            height_per_period = tower_height - last_tower_height

            # Calculate the number of full cycles that we can skip. There will likely be
            # some remainder, but we can continue the direct simulation until we hit the target
            # value of rock drops. By definition, it will be less cycles than we've already simulated.
            periods_to_skip = (PART_TWO_COUNT - rock_num) // period
            height_to_add = height_per_period * periods_to_skip

            # Now, cheat a little bit and just raise up our existing tower by the calculated height.
            # We have to raise both the height tracker and each coordinate in the mapping.
            tower_height += height_to_add
            new_chamber = {}
            for c in chamber:
                new_chamber[(c[0], c[1] + height_to_add)] = '█'
            chamber = new_chamber

            # More cheating -- advance our rock counter by the calculated number.
            rock_num += period * periods_to_skip
        else:
            # New state in our cycle history -- record it.
            experiment_states[(tick, rock_idx, floor_state)] = (rock_num, tower_height)

    rock_num += 1

    if rock_num == PART_ONE_COUNT:
        print('Part One: tower is {0} blocks tall after {1} rocks have stopped.'.format(tower_height, PART_ONE_COUNT))

print('Part Two: tower is {0} blocks tall after {1} rocks have stopped.'.format(tower_height, PART_TWO_COUNT))
