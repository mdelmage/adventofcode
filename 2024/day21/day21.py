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
    'A<': ['v<<A'],
    '<A': ['>>^A'],
    'A^': ['<A'],
    '^A': ['>A'],
    'A>': ['vA'],
    '>^': ['<^A'],
    '^^': ['A'],
    'Av': ['<vA'],
    'vv': ['A'],
    'vA': ['^>A'],
    '^>': ['>vA'],
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

def shortest_next_sequences(sequences):
    #print(sequences)
    best_seqs = []
    best_len = 9999999999999999999999999
    for seq in sequences:
        sequences_next = ['']
        seq = 'A' + seq
        for i in range(len(seq) - 1):
            sequences_next = [p + n for p in sequences_next for n in directional_keypad[seq[i:i+2]]]
        for seq_next in sequences_next:
            seq_len = len(seq_next)
            if seq_len < best_len:
                best_len = seq_len
                best_seqs = []
            if seq_len == best_len:
                best_seqs.append(seq_next)
    return best_seqs

# Parse the door codes list.
with open('day21_input.txt') as f:
    door_codes = [line.rstrip('\n') for line in f]

complexity_sum = 0
for code in door_codes:
    directional_sequences_l1 = ['']
    code = 'A' + code
    shortest_sequence = None
    for i in range(len(code) - 1):
        directional_sequences_l1 = [p + n for p in directional_sequences_l1 for n in numeric_keypad[code[i:i+2]]]

    for i in range(25):
        directional_sequences_l1 = shortest_next_sequences(directional_sequences_l1)
        print(i, len(directional_sequences_l1), len(directional_sequences_l1[0]))

    # The complexity of a single code (like 029A) is equal to the result of multiplying these two values:
    #
    # The length of the shortest sequence of button presses you need to type on your directional keypad
    # in order to cause the code to be typed on the numeric keypad; for 029A, this would be 68.
    # The numeric part of the code (ignoring leading zeroes); for 029A, this would be 29.
    complexity_sum += int(code.replace('A', '')) * len(directional_sequences_l1[0])

# Find the fewest number of button presses you'll need to perform in order to cause the robot in front of the door to type each code.
# What is the sum of the complexities of the five codes on your list?
print('Part One: Sum of complexities of the five codes is {0}.'.format(complexity_sum))
