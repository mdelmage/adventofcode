#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Greatest Common Divisor
def gcd(a, b):
    if b == 0: return a
    return gcd(b, a % b)

# Least Common Multiple (of a list)
def lcm(l):
    result = 1
    for item in l:
        result = result * item // gcd(result, item)
    return result

# Parse the documents file
with open('day08_input.txt') as f:
    document = [line.rstrip('\n') for line in f]
    directions = document[0]
    maps = {}
    for line in document[2:]:
        tokens = line.split(' = ')
        src = tokens[0]
        dests = tokens[1][1:-1].split(', ')
        maps[src] = dests

# After examining the maps for a bit, two nodes stick out: AAA and ZZZ.
# You feel like AAA is where you are now, and you have to follow the left/right instructions
# until you reach ZZZ.
loc = 'AAA'
steps = 0
while loc != 'ZZZ':
    # Of course, you might not find ZZZ right away. If you run out of left/right instructions,
    # repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on.
    if directions[steps % len(directions)] == 'L':
        loc = maps[loc][0]
    else:
        loc = maps[loc][1]
    steps += 1

# Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
print('Part One: Total steps required to reach ZZZ is {0}.'.format(steps))

# After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes
# with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just
# start at every node that ends with A and follow all of the paths at the same time until they all
# simultaneously end up at nodes that end with Z.
#
# Simultaneously start on every node that ends with A. 
locs = [l for l in maps if l[2] == 'A']

# By inspection: the input is crafted to have specific, deterministic paths.
# These paths have the following properties:
#
# 1. There is a direct path from each starting node ('XXA') to a unique ending node ('XXZ');
# 2. There are no other starting or ending nodes encountered on a given path;
# 3. The path loops from the ending node back to the ending node continuously;
# 4. The length of the starting-to-ending path is exactly the same length as the ending-to-ending loop.
#
# Because of these properties, the ghost will pass through each ending node with some specific period.
# When the periods of these loop align, our navigation exercise is complete.
steps = 0
periods = {}
# Keep going until we have a looping period for every path
while len(periods) != len(locs):
    locs_next = []
    for loc in locs:
        if directions[steps % len(directions)] == 'L':
            loc = maps[loc][0]
        else:
            loc = maps[loc][1]

        # Save the destination node in our list
        locs_next.append(loc)

        # If we arrived at an ending node, determine the loop period
        if loc[2] == 'Z':
            pos = len(locs_next) - 1
            periods[pos] = steps + 1 - periods.get(pos, 0)
    locs = locs_next
    steps += 1

# The shortest period of a set of simple loops, as described above, is the least common multiple
# (LCM) of all loops' periods.
steps = lcm(periods.values())

# How many steps does it take before you're only on nodes that end with Z?
print('Part Two: Total steps required to reach only nodes that end with Z is {0}.'.format(steps))