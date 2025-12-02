#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For a string of given length l, return a list of substring lengths
# that need to be checked for repeats.
def substring_lengths(s):
    lengths = []
    current_length = 1
    # Only check up to half the string length; you can't have repeats
    # if a substring is longer than half.
    while current_length <= len(s) / 2:
        if len(s) % current_length == 0: lengths.append(current_length)
        current_length += 1
    return lengths

# Deconstruct a given string into substring tokens of length l
# and return them as a list.
def tokenize(s, l):
    tokens = []
    while s != '':
        tokens.append(s[:l])
        s = s[l:]
    return tokens

# For a given list of tokens, return True if they are all the same.
# Return False otherwise.
def identical(tokens):
    token = tokens[0]
    while len(tokens) > 0:
        popped = tokens.pop()
        if popped != token: return False
    return True

# Determine if an ID is invalid by checking if it has repeating substrings.
def invalid(id, substring_lengths):
    for l in substring_lengths:
        if identical(tokenize(str(id), l)): return True
    return False

# Parse the product ID ranges
with open('day02_input.txt') as f:
    product_id_ranges = [line.rstrip('\n').split(',') for line in f][0]

invalid_id_sum_part_one = 0
invalid_id_sum_part_two = 0
for r in product_id_ranges:
    # The ranges are separated by commas (,); each range gives its first ID
    # and last ID separated by a dash (-).
    first, last = [int(n) for n in r.split('-')]
    for id in range(first, last + 1):
        id_str = str(id)
        # Since the young Elf was just doing silly patterns, you can find the
        # invalid IDs by looking for any ID which is made only of some sequence
        # of digits repeated twice.
        if len(id_str) % 2 == 0 and invalid(id, [len(id_str) // 2]):
            invalid_id_sum_part_one += id

        # Now, an ID is invalid if it is made only of some sequence of digits
        # repeated at least twice.
        if invalid(id, substring_lengths(id_str)):
            invalid_id_sum_part_two += id

# What do you get if you add up all of the invalid IDs?
print('Part One: The sum of invalid IDs is {0}.'.format(invalid_id_sum_part_one))

# What do you get if you add up all of the invalid IDs using these new rules?
print('Part Two: The sum of invalid IDs is {0}.'.format(invalid_id_sum_part_two))