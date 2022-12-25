#!/usr/bin/env python
# -*- coding: utf-8 -*-

def mix(file, rounds, decryption_key=1):
    coords = []
    for line in range(len(file)):
        coords.append((line, decryption_key * int(file[line])))

        # Mark which line the zero was on, for later reference.
        if int(file[line]) == 0:
            zero_marker = (line, 0)

    for round in range(rounds):
        for line in range(len(file)):
            # Kind of a clumsy way of remembering the initial ordering of the input
            # file: use a (line number, value) pairing.
            # Go through the file to find the value on the line number we want.
            for value in coords:
                if value[0] == line:
                    n = value
                    break

            if n[1] > 0:
                # Going right; line up on the right neighbor and wrap as necessary.
                right_neighbor = coords[(coords.index(n) + 1) % len(coords)]
                coords.pop(coords.index(n))
                right_neighbor_idx = coords.index(right_neighbor)
                insertion_idx = (right_neighbor_idx + n[1]) % len(coords)
            elif n[1] < 0:
                # Going left; line up on the left neighbor and wrap as necessary.
                # The math is a little different (off by one vs. going right).
                left_neighbor = coords[(coords.index(n) - 1) % len(coords)]
                coords.pop(coords.index(n))
                left_neighbor_idx = coords.index(left_neighbor)
                insertion_idx = (left_neighbor_idx + n[1] + 1) % len(coords)
            else:
                # Got a zero; do nothing.
                continue

            coords.insert(insertion_idx, n)

    # Then, the grove coordinates can be found by looking at the 1000th, 2000th,
    # and 3000th numbers after the value 0, wrapping around the list as necessary.
    grove = 0
    zero_marker = coords.index(zero_marker)
    grove += coords[(zero_marker + 1000) % len(coords)][1]
    grove += coords[(zero_marker + 2000) % len(coords)][1]
    grove += coords[(zero_marker + 3000) % len(coords)][1]
    return grove

# Parse the encrypted file
with open('day20_input.txt') as f:
    numbers = [line.rstrip('\n')for line in f]

# Mix your encrypted file exactly once. What is the sum of the three numbers
# that form the grove coordinates?
print('Part One: Grove coordinates are {0}.'.format(mix(numbers, 1)))

# The grove coordinate values seem nonsensical. While you ponder the mysteries
# of Elf encryption, you suddenly remember the rest of the decryption routine
# you overheard back at camp.
#
# First, you need to apply the decryption key, 811589153. Multiply each number
# by the decryption key before you begin; this will produce the actual list of
# numbers to mix.
# Second, you need to mix the list of numbers ten times.
print('Part Two: Grove coordinates are {0}.'.format(mix(numbers, 10, decryption_key=811589153)))
