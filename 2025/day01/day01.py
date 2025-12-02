#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the attached document of rotation sequences
with open('day01_input.txt') as f:
    rotations = [line.rstrip('\n') for line in f]

# The dial starts by pointing at 50.
dial = 50

password_part_one = 0
password_part_two = 0
for r in rotations:
    dial_start = dial
    # A rotation starts with an L or R which indicates whether the rotation should be to the left
    # (toward lower numbers) or to the right (toward higher numbers). Then, the rotation has a
    # distance value which indicates how many clicks the dial should be rotated in that direction.
    direction = r[0]
    distance = int(r[1:])

    # You remember from the training seminar that "method 0x434C49434B" means you're actually supposed
    # to count the number of times any click causes the dial to point at 0, regardless of whether it
    # happens during a rotation or at the end of one.
    password_part_two += (distance // 100)
    distance %= 100

    for i in range(distance):
        if (direction == 'L'):
            dial -= 1
        else:
            dial += 1

        # Because the dial is a circle, turning the dial left from 0 one click makes it point at 99.
        # Similarly, turning the dial right from 99 one click makes it point at 0.
        dial %= 100
        if dial == 0: password_part_two += 1

    # The actual password is the number of times the dial is left pointing at 0 after any rotation
    # in the sequence.
    if dial == 0: password_part_one += 1

# Analyze the rotations in your attached document. What's the actual password to open the door?
print('Part One: The password is {0}.'.format(password_part_one))

# Using password method 0x434C49434B, what is the password to open the door?
print('Part Two: The password is {0}.'.format(password_part_two))