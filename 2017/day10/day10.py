#!/usr/bin/env python
# -*- coding: utf-8 -*-

HASH_LEN = 16

def knot_hash_round(cur_pos, skip_size, knot_list, lengths):
    # Then, for each length:
    #
    # Reverse the order of that length of elements in the list, starting with the element at the current position.
    # Move the current position forward by that length plus the skip size.
    # Increase the skip size by one.
    #
    # The list is circular; if the current position and the length try to reverse elements beyond the end of the list,
    # the operation reverses using as many extra elements as it needs from the front of the list. If the current
    # position moves past the end of the list, it wraps around to the front.
    for length in lengths:
        # Unroll the list so we don't have to worry about wrapping
        knot_list = knot_list[cur_pos:] + knot_list[:cur_pos]

        # Reverse the sub-list
        knot_list = knot_list[:length][::-1] + knot_list[length:]

        # Re-roll the list by moving the last elements to the front
        knot_list = knot_list[-cur_pos:] + knot_list[:-cur_pos]

        cur_pos = (cur_pos + length + skip_size) % len(knot_list)
        skip_size += 1

    return (cur_pos, skip_size, knot_list)

def knot_hash(s):
    # ...begin with a list of numbers from 0 to 255, a current position which begins at 0
    #(the first element in the list), a skip size (which starts at 0), and a sequence
    # of lengths (your puzzle input). 
    knot_list = [i for i in range(256)]
    cur_pos = 0
    skip_size = 0

    # Once you have determined the sequence of lengths to use, add the following lengths
    # to the end of the sequence: 17, 31, 73, 47, 23.
    lengths = [ord(ch) for ch in s] + [17, 31, 73, 47, 23]

    # Run a total of 64 rounds, using the same length sequence in each round.
    # The current position and skip size should be preserved between rounds.
    for i in range(64):
        (cur_pos, skip_size, knot_list) = knot_hash_round(cur_pos, skip_size, knot_list, lengths)

    # Once the rounds are complete, you will be left with the numbers from 0 to 255 in some order,
    # called the sparse hash. Your next task is to reduce these to a list of only 16 numbers called
    # the dense hash. To do this, use numeric bitwise XOR to combine each consecutive block of 16 numbers
    # in the sparse hash (there are 16 such blocks in a list of 256 numbers).
    dense_hash = ''
    for i in range(len(knot_list) / HASH_LEN):
        xor = 0
        for j in range(HASH_LEN):
            xor ^= knot_list[(HASH_LEN * i) + j]
        dense_hash += '{:02x}'.format(xor)
    return dense_hash

# Parse the skip list and save each value
with open('day10_input.txt') as f:
    lengths = [int(s) for s in [line.rstrip('\n').split(',') for line in f][0]]

# ...begin with a list of numbers from 0 to 255, a current position which begins at 0
#(the first element in the list), a skip size (which starts at 0), and a sequence
# of lengths (your puzzle input). 
knot_list = [i for i in range(256)]
cur_pos = 0
skip_size = 0

(cur_pos, skip_size, knot_list) = knot_hash_round(cur_pos, skip_size, knot_list, lengths)

print 'Part One: product of first two numbers in the list is {0}.'.format(knot_list[0] * knot_list[1])

# From now on, your input should be taken not as a list of numbers, but as a string of bytes instead.
# Unless otherwise specified, convert characters to bytes using their ASCII codes.
with open('day10_input.txt') as f:
    lengths = [line.rstrip('\n') for line in f][0]

# knot_hash('')
# knot_hash('AoC 2017')
# knot_hash('1,2,3')
# knot_hash('1,2,4')

print 'Part Two: Knot Hash is {0}.'.format(knot_hash(lengths))