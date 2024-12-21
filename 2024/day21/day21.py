#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A chain of directional robots with depth=25 is too long to calculate directly.
# Instead, pre-generate outputs for pairs up to depth=15, and then record their lengths.
PRE_OPTIMIZATION_LEVEL = 15

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
    # Mapping of directional keypad inputs to achieve a numeric keypad transition.
    # This is based on my coor codes input, and thereby sparse/incomplete.
    # Fill in your code pairs here.
    '0A': ['>A'],
    '1A': ['>>vA', '>v>A'],
    '18': ['>^^A', '^>^A', '^^>A'],
    '2A': ['>vA', 'v>A'],
    '39': ['^^A'],
    '34': ['<<^A', '^<<A', '^<<A'],
    '41': ['vA'],
    '53': ['v>A', '>vA'],
    '68': ['<^A', '^<A'],
    '78': ['>A'],
    '80': ['vvvA'],
    '82': ['vvA'],
    '89': ['>A'],
    '9A': ['vvvA'],
    'A1': ['^<<A', '<^<A'],
    'A3': ['^A'],
    'A5': ['^^<A', '^<^A', '<^^A'],
    'A6': ['^^A'],
    'A7': ['^^^<<A', '^^<^<A', '^^<<^A', '<^^^<A', '<^<^^A', '<^^<^A'],
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
    # Mapping of directional keypad inputs to achieve a (downstream) directional keypad transition.
    'A<': ['v<<A'],#, '<v<A'],
    '<A': ['>>^A'],#, '>^>A'],
    'A^': ['<A'],
    '^A': ['>A'],
    'A>': ['vA'],
    '>^': ['<^A'],#, '^<A'],
    '^^': ['A'],
    'Av': ['<vA'],#, 'v<A'],
    'vv': ['A'],
    'vA': ['^>A'],#, '>^A'],
    '^>': ['v>A'], #'>vA'],
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

def complexity(level):
    optimized = (level > PRE_OPTIMIZATION_LEVEL)
    if optimized: level -= PRE_OPTIMIZATION_LEVEL

    complexity_sum = 0
    for code in ['A' + code for code in door_codes]:
        # The robot has no problem navigating the ship and finding the numeric keypad, but it's not designed
        # for button pushing: it can't be told to push a specific button directly. Instead, it has a robotic arm
        # that can be controlled remotely via a directional keypad.
        numeric_seq = ['']
        for i in range(len(code) - 1):
            numeric_seq = [n + k for n in numeric_seq for k in numeric_keypad[code[i:i+2]]]

        # Unfortunately, the area containing this directional keypad remote control is currently experiencing
        # high levels of radiation and nobody can go near it. A robot needs to be sent instead.
        #
        # When the robot arrives at the directional keypad, its robot arm is pointed at the A button in the
        # upper right corner. After that, a second, different directional keypad remote control is used to control
        # this robot (in the same way as the first robot, except that this one is typing on a directional keypad
        # instead of a numeric keypad).
        min_buttons = None
        for seq in numeric_seq:
            for step in range(level):
                seq = 'A' + seq
                seq = ''.join([directional_keypad[seq[j:j+2]][0] for j in range(len(seq) - 1)])

            if optimized:
                seq = 'A' + seq
                result = sum([lookup[seq[j:j+2]] for j in range(len(seq) - 1)])
            else:
                result = len(seq)

            if not min_buttons: min_buttons = result
            min_buttons = min(min_buttons, result)

        # The complexity of a single code (like 029A) is equal to the result of multiplying these two values:
        #
        # The length of the shortest sequence of button presses you need to type on your directional keypad
        # in order to cause the code to be typed on the numeric keypad; for 029A, this would be 68.
        # The numeric part of the code (ignoring leading zeroes); for 029A, this would be 29.
        complexity_sum += int(code[1:-1]) * min_buttons

    return complexity_sum

lookup = {}
for pair in directional_keypad:
    min_buttons = None
    seq = pair
    for step in range(PRE_OPTIMIZATION_LEVEL):
        if step > 0: seq = 'A' + seq
        seq = ''.join([directional_keypad[seq[j:j+2]][0] for j in range(len(seq) - 1)])

    # Record the best (shortest) button sequence possible.
    if not min_buttons: min_buttons = len(seq)
    min_buttons = min(min_buttons, len(seq))
    lookup[pair] = min_buttons

# Parse the door codes list.
with open('day21_input.txt') as f:
    door_codes = [line.rstrip('\n') for line in f]

# Find the fewest number of button presses you'll need to perform in order to cause the robot in front of the door
# to type each code. What is the sum of the complexities of the five codes on your list?
print('Part One: Sum of complexities of the five codes is {0}.'.format(complexity(2)))

# A quick life-form scan reveals the Historian is also trapped in a locked area of the ship.
# Due to a variety of hazards, robots are once again dispatched, forming another chain of remote control keypads
# managing robotic-arm-wielding robots.
#
# This time, many more robots are involved. In summary, there are the following keypads:
#
# One directional keypad that you are using.
# 25 directional keypads that robots are using.
# One numeric keypad (on a door) that a robot is using.
# The keypads form a chain, just like before: your directional keypad controls a robot which is typing on a
# directional keypad which controls a robot which is typing on a directional keypad... and so on, ending with
# the robot which is typing on the numeric keypad.
#
# The door codes are the same this time around; only the number of robots and directional keypads has changed.
#
# Find the fewest number of button presses you'll need to perform in order to cause the robot in front of the door
# to type each code. What is the sum of the complexities of the five codes on your list?
print('Part Two: Sum of complexities of the five codes is {0}.'.format(complexity(25)))