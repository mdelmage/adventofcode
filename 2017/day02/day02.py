#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the spreadsheet and save each line
with open('day02_input.txt') as f:
    rows = [line.rstrip('\n').split() for line in f]

checksum = 0
divsum = 0
for row in rows:
    # For each row, determine the difference between the largest value and the smallest value;
    # the checksum is the sum of all of these differences.
    r = [int(c) for c in row]
    checksum += max(r) - min(r)

    # It sounds like the goal is to find the only two numbers in each row where one
    # evenly divides the other - that is, where the result of the division operation
    # is a whole number. They would like you to find those numbers on each line,
    # divide them, and add up each line's result.
    for i in range(len(r)):
        for j in range(len(r)):
            if i != j and r[j] != 0 and r[i] % r[j] == 0:
                divsum += r[i] / r[j]

print 'Part One: checksum=%d' % checksum
print 'Part Two: divsum=%d' % divsum