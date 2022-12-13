#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from functools import cmp_to_key

# Map result codes to expected Python custom comparator values.
RESULT_IN_ORDER = -1
RESULT_NOT_IN_ORDER = 1
RESULT_EQUAL = 0

def compare(left, right, level=0):
    if isinstance(left, int) and isinstance(right, int):
        # If both values are integers, the lower integer should come first.
        # If the left integer is lower than the right integer, the inputs are in the right order.
        # If the left integer is higher than the right integer, the inputs are not in the right order.
        # Otherwise, the inputs are the same integer; continue checking the next part of the input.
        if left < right:
            return RESULT_IN_ORDER
        elif left > right:
            return RESULT_NOT_IN_ORDER
        else:
            return RESULT_EQUAL
    elif isinstance(left, list) and isinstance(right, list):
        # If both values are lists, compare the first value of each list, then the second value,
        # and so on. If the left list runs out of items first, the inputs are in the right order.
        # If the right list runs out of items first, the inputs are not in the right order.
        # If the lists are the same length and no comparison makes a decision about the order,
        # continue checking the next part of the input.
        for i in range(len(left)):
            if i < len(right):
                result = compare(left[i], right[i], level + 1)
                if result != RESULT_EQUAL: return result
            else:
                # If the right list runs out of items first, the inputs are not in the right order.
                return RESULT_NOT_IN_ORDER

        if len(left) < len(right):
            # If the left list runs out of items first, the inputs are in the right order.
            return RESULT_IN_ORDER
        else:
            # If the lists are the same length and no comparison makes a decision about the order,
            # continue checking the next part of the input.
            return RESULT_EQUAL
    elif isinstance(left, list):
        # If exactly one value is an integer, convert the integer to a list which contains
        # that integer as its only value, then retry the comparison.
        return compare(left, [right], level + 1)
    else:
        return compare([left], right, level + 1)

# Parse the packet pairs file
with open('day13_input.txt') as f:
    pairs = [''] + [line.rstrip('\n') for line in f]

sum_in_order = 0
packets = []
for i in range(len(pairs) // 3):
    left = ast.literal_eval(pairs[3 * i + 1])
    right = ast.literal_eval(pairs[3 * i + 2])

    packets.append(left)
    packets.append(right)

    # Determine which pairs of packets are already in the right order.
    # What is the sum of the indices of those pairs?
    if compare(left, right) == RESULT_IN_ORDER:
        sum_in_order += i + 1

print('Part One: sum of in-order packet pair indices is {0}.'.format(sum_in_order))

# The distress signal protocol also requires that you include two additional divider packets:
#
# [[2]]
# [[6]]
packets.append([[2]])
packets.append([[6]])

# Organize all of the packets into the correct order.
# What is the decoder key for the distress signal?
packets = sorted(packets, key=cmp_to_key(compare))
for i in range(len(packets)):
    # Afterward, locate the divider packets. To find the decoder key for this distress signal,
    # you need to determine the indices of the two divider packets and multiply them together.
    if packets[i] == [[2]]: packet_one_position = i + 1
    if packets[i] == [[6]]: packet_two_position = i + 1

print('Part Two: distress signal decoder key is {0}.'.format(packet_one_position * packet_two_position))
