#!/usr/bin/env python
# -*- coding: utf-8 -*-

HASH_LEN = 16
GRID_SIZE = 128
USED      = 'u'
TRAVERSED = 't'

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

def mark_region(coord):
    global disk

    # A region is a group of used squares that are all adjacent, not including diagonals.
    # Every used square is in exactly one region: lone used squares form their own isolated regions,
    # while several adjacent squares all count as a single region.
    disk[coord] = TRAVERSED
    for c in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        neighbor = (coord[0] + c[0], coord[1] + c[1])
        if neighbor in disk and disk[neighbor] == USED:
            mark_region(neighbor)

def remove_region():
    global disk

    remove_list = []
    for coord in disk:
        if disk[coord] == TRAVERSED:
            remove_list.append(coord)

    for coord in remove_list:
        del disk[coord]

# Parse the key file
with open('day14_input.txt') as f:
    key = [line.rstrip('\n') for line in f][0]

# key = 'flqrgnkx'

# The hash inputs are a key string (your puzzle input), a dash, and a number
# from 0 to 127 corresponding to the row.
disk = {}
for row in range(GRID_SIZE):
    # The output of a knot hash is traditionally represented by 32 hexadecimal digits;
    # each of these digits correspond to 4 bits, for a total of 4 * 32 = 128 bits.
    row_hash = knot_hash('{0}-{1}'.format(key, row))

    # Now mark the used squares bitmap for each hexadecimal bit that's set in the hash.
    for i in range(len(row_hash)):
        val = int(row_hash[i], 16)
        binary_string = '{0:04b}'.format(val)
        for digit in range(4):
            if binary_string[digit] == '1': disk[(row, (i * 4) + digit)] = USED

print 'Part One: {0} squares are used.'.format(len(disk))

# Mark, count, and remove regions one by one.
regions = 0
while len(disk) > 0:
    regions += 1
    mark_region(list(disk.keys())[0])
    remove_region()

print 'Part Two: {0} regions are present.'.format(regions)