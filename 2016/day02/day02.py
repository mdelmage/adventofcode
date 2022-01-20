#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The document goes on to explain that each button to be pressed can be found by starting on the previous button
# and moving to adjacent buttons on the keypad: U moves up, D moves down, L moves left, and R moves right.
DIRECTIONS = { 'U': ( 0, -1),
               'R': ( 1,  0),
               'D': ( 0,  1),
               'L': (-1,  0)}

# You can't hold it much longer, so you decide to figure out the code as you walk to the bathroom.
# You picture a keypad like this:
#
# 1 2 3
# 4 5 6
# 7 8 9
KEYPAD_PART1 = { (0, 0): '1',
                 (1, 0): '2',
                 (2, 0): '3',
                 (0, 1): '4',
                 (1, 1): '5',
                 (2, 1): '6',
                 (0, 2): '7',
                 (1, 2): '8',
                 (2, 2): '9'}

# Much to your bladder's dismay, the keypad is not at all like you imagined it.
# Instead, you are confronted with the result of hundreds of man-hours of bathroom-keypad-design meetings:
#
#     1
#   2 3 4
# 5 6 7 8 9
#   A B C
#     D
KEYPAD_PART2 = { (2, 0): '1',
                 (1, 1): '2',
                 (2, 1): '3',
                 (3, 1): '4',
                 (0, 2): '5',
                 (1, 2): '6',
                 (2, 2): '7',
                 (3, 2): '8',
                 (4, 2): '9',
                 (1, 3): 'A',
                 (2, 3): 'B',
                 (3, 3): 'C',
                 (2, 4): 'D'}

# Parse the bathroom codes instructions file
with open('day02_input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

pos = (1, 1)
bathroom_code = ''
for line in lines:
    for d in line:
        # Each line of instructions corresponds to one button, starting at the previous button
        # (or, for the first line, the "5" button); press whatever button you're on at the end of each line.
        # If a move doesn't lead to a button, ignore it.
        new_pos = (pos[0] + DIRECTIONS[d][0], pos[1] + DIRECTIONS[d][1])
        if new_pos in KEYPAD_PART1:
            pos = new_pos
    bathroom_code += KEYPAD_PART1[pos]

print('Part One: Bathroom code is {0}.'.format(bathroom_code))

# You still start at "5" and stop when you're at an edge...
pos = (0, 2)
bathroom_code = ''
for line in lines:
    for d in line:
        # Each line of instructions corresponds to one button, starting at the previous button
        # (or, for the first line, the "5" button); press whatever button you're on at the end of each line.
        # If a move doesn't lead to a button, ignore it.
        new_pos = (pos[0] + DIRECTIONS[d][0], pos[1] + DIRECTIONS[d][1])
        if new_pos in KEYPAD_PART2:
            pos = new_pos
    bathroom_code += KEYPAD_PART2[pos]

print('Part Two: Bathroom code is {0}.'.format(bathroom_code))
