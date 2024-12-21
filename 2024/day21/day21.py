#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The numeric keypad has four rows of buttons: 789, 456, 123, and finally an empty gap followed by 0A.
# Visually, they are arranged like this:
#
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
numeric_keypad = {
    'A0': ['<A'],
    '02': ['^A'],
    '29': ['>^^A', '^>^A', '^^>A'],
    '9A': ['vvvA'],

    'A9': ['^^^A'],
    '98': ['<A'],
    '80': ['vvvA'],
    '0A': ['>A'],

    'A1': ['^<<A', '<^<A'],
    '17': ['^^A'],
    '79': ['>>A'],

    'A4': ['^^<<A', '^<<^A', '<^^<A', '<^<^A', '^<^<A'],
    '45': ['>A'],
    '56': ['>A'],
    '6A': ['vvA'],

    'A3': ['^A'],
    '37': ['^^<<A', '^<^<A', '^<<^A', '<<^^A', '<^<^A', '<^^<A'],

    'A7': ['^^^<<A', '^^<^<A', '^^<<^A', '<^^^<A', '<^<^^A', '<^^<^A'],
    '78': ['>A'],

    'A5': ['^^<A', '^<^A', '<^^A'],
    '53': ['v>A', '>vA'],

    '39': ['^^A'],

    '34': ['<<^A', '^<<A', '^<<A'],

    '41': ['vA'],
    '1A': ['>>vA', '>v>A'],

    '18': ['>^^A', '^>^A', '^^>A'],

    '89': ['>A'],

    'A6': ['^^A'],

    '68': ['<^A', '^<A'],

    '82': ['vvA'],
    '2A': ['>vA', 'v>A']
}

# The directional keypad has two rows of buttons: a gap / ^ (up) / A (activate) on the first row
# and < (left) / v (down) / > (right) on the second row. Visually, they are arranged like this:
#
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
directional_keypad = {
    'A<': ['<v<A', 'v<<A'],
    '<A': ['>>^A', '>^vA'],
    'A^': ['<A'],
    '^A': ['>A'],
    'A>': ['vA'],
    '>^': ['<^A', '^<A'],
    '^^': ['A'],
    'Av': ['<vA', 'v<A'],
    'vv': ['A'],
    'vA': ['^>A', '>^A'],
    '^>': ['>vA', 'v>A'],
    '>A': ['^A'],
    '^<': ['v<A'],
    '<<': ['A'],
    '>>': ['A'],
    '<^': ['>^A'],
    '<v': ['>A'],
    'v<': ['<A'],
    'AA': ['A'],
    '^v': ['vA'],
    '>v': ['<A'],
    'v>': ['>A']
}

def manhattan_dist(src, dest):
    return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

# Parse the door codes list.
with open('day21_input.txt') as f:
    door_codes = [line.rstrip('\n') for line in f]

complexity_sum = 0
for code in door_codes:
    directional_sequences_l1 = ['']
    code = 'A' + code
    shortest_sequence = 99999999999999999
    for i in range(len(code) - 1):
        directional_sequences_l1 = [p + n for p in directional_sequences_l1 for n in numeric_keypad[code[i:i+2]]]
    
    for seql1 in directional_sequences_l1:
        directional_sequences_l2 = ['']
        seql1 = 'A' + seql1
        for i in range(len(seql1) - 1):
            directional_sequences_l2 = [p + n for p in directional_sequences_l2 for n in directional_keypad[seql1[i:i+2]]]

        for seql2 in directional_sequences_l2:
            directional_sequences_l3 = ['']
            seql2 = 'A' + seql2
            for i in range(len(seql2) - 1):
                # We only need one sequence at Level 3, since they'll all be the same length.
                directional_sequences_l3 = [p + n for p in [directional_sequences_l3[0]] for n in directional_keypad[seql2[i:i+2]]]
            shortest_sequence = min(shortest_sequence, len(directional_sequences_l3[0]))

    # The complexity of a single code (like 029A) is equal to the result of multiplying these two values:
    #
    # The length of the shortest sequence of button presses you need to type on your directional keypad
    # in order to cause the code to be typed on the numeric keypad; for 029A, this would be 68.
    # The numeric part of the code (ignoring leading zeroes); for 029A, this would be 29.
    complexity_sum += int(code[1:-1]) * shortest_sequence

# Find the fewest number of button presses you'll need to perform in order to cause the robot in front of the door to type each code.
# What is the sum of the complexities of the five codes on your list?
print('Part One: Sum of complexities of the five codes is {0}.'.format(complexity_sum))
