#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the initialization sequence.
with open('day15_input.txt') as f:
    seq = [f.read().rstrip('\n').split(',')][0]

# The book goes on to describe a series of 256 boxes numbered 0 through 255.
# The boxes are arranged in a line starting from the point where light enters
# the facility. The boxes have holes that allow light to pass from one box
# to the next all the way down the line.
boxes = {}
for b in range(256):
    boxes[b] = []

results = 0
for s in seq:
    # To run the HASH algorithm on a string, start with a current value of 0.
    # Then, for each character in the string starting from the beginning:
    value = 0
    for ch in s:
        # Each step begins with a sequence of letters that indicate the label of the lens
        # on which the step operates. The result of running the HASH algorithm on the label
        # indicates the correct box for that step.
        if ch in ['=', '-']: box = value

        # Determine the ASCII code for the current character of the string.
        # Increase the current value by the ASCII code you just determined.
        # Set the current value to itself multiplied by 17.
        # Set the current value to the remainder of dividing itself by 256.
        value += ord(ch)
        value *= 17
        value %= 256

    # To verify that your HASH algorithm is working, the book offers the sum of the result
    # of running the HASH algorithm on each step in the initialization sequence.
    results += value

    # Figure out if we're assigning ('=') or removing ('-').
    if '=' in s:
        s = s.split('=')
    else:
        s = [s[:-1], '-']

    (label, value) = s
    if value == '-':
        # If the operation character is a dash (-), go to the relevant box and remove the lens
        # with the given label if it is present in the box. Then, move any remaining lenses
        # as far forward in the box as they can go without changing their order, filling any
        # space made by removing the indicated lens. (If no lens in that box has the given label,
        # nothing happens.)
        for i in range(len(boxes[box])):
            if boxes[box][i][0] == label:
                del boxes[box][i]
                break
    else:
        # If the operation character is an equals sign (=), it will be followed by a number
        # indicating the focal length of the lens that needs to go into the relevant box; be sure
        # to use the label maker to mark the lens with the label given in the beginning of the step
        # so you can find it later.
        done = False
        value = int(value)
        for i in range(len(boxes[box])):
            if boxes[box][i][0] == label:
                del boxes[box][i]
                boxes[box].insert(i, (label, value))
                done = True
                break
        if not done: boxes[box].append((label, value))

# Run the HASH algorithm on each step in the initialization sequence.
# What is the sum of the results?
print('Part One: Sum of the HASH algorithm results is {0}.'.format(results))

# To confirm that all of the lenses are installed correctly, add up the focusing power
# of all of the lenses. The focusing power of a single lens is the result of multiplying together:
#
# One plus the box number of the lens in question.
# The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
# The focal length of the lens.
focusing_power = 0
for box in range(256):
    for lens in range(len(boxes[box])):
        focal_length = boxes[box][lens][1]
        focusing_power += (box + 1) * (lens + 1) * focal_length

# With the help of an over-enthusiastic reindeer in a hard hat, follow the initialization sequence.
# What is the focusing power of the resulting lens configuration?
print('Part Two: The focusing power of the lens configuration is {0}.'.format(focusing_power))