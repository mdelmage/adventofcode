#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

PREAMBLE_LENGTH = 25

# Parse the eXchange-Masking Addition System (XMAS) stream and save each line
with open('day09_input.txt') as f:
    xmas_stream = []
    for line in f:
        xmas_stream.append(int(line))

for i in range(PREAMBLE_LENGTH, len(xmas_stream)):
    # The first step of attacking the weakness in the XMAS data is to find the first number in the list
    # (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first
    # number that does not have this property?
    lookback = xmas_stream[max(0, i - PREAMBLE_LENGTH):i]
    lookback_combinations = list(itertools.combinations(lookback, 2))
    valid = False
    for paired_sum in [c1+c2 for (c1, c2) in lookback_combinations]:
        if xmas_stream[i] == paired_sum:
            valid = True
            break
    if not valid:
        invalid_entry = xmas_stream[i]
        break

print 'Part One: {0} was not valid.'.format(invalid_entry)

# The final step in breaking the XMAS encryption relies on the invalid number you just found:
# you must find a contiguous set of at least two numbers in your list which sum to the
# invalid number from step 1.
for i in range(len(xmas_stream)):
    running_sum = 0
    for j in range(i, len(xmas_stream)):
        sub_stream = xmas_stream[i:j]
        if sum(sub_stream) == invalid_entry and len(sub_stream) > 1:
            print 'Part Two: Sum of min/max of contiguous invalid entries is {0}.'.format(min(xmas_stream[i:j]) + max(xmas_stream[i:j]))