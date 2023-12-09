#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the OASIS report file
with open('day09_input.txt') as f:
    report = [[int(n) for n in line.rstrip('\n').split()] for line in f]

# To best protect the oasis, your environmental report should include a prediction of the next value
# in each history. To do this, start by making a new sequence from the difference at each step of your history.
# If that sequence is not all zeroes, repeat this process, using the sequence you just generated as the
# input sequence. Once all of the values in your latest sequence are zeroes, you can extrapolate what the next
# value of the original history should be.
extrapolation_sum_a = 0
extrapolation_sum_b = 0
for history in report:
    seq = [history]
    # This doesn't strictly check against "all zeroes", but it works for our input.
    while sum(seq[-1]) != 0:
        # Use a list comprehension to fill out the next sequence.
        seq.append([seq[-1][n + 1] - seq[-1][n] for n in range(len(seq[-1]) - 1)])

    # Now roll back up to the original history, adding new values to each sequence on either end.
    for n in range(len(seq) - 1, 0, -1):
        l = len(seq[n])
        prev_l = len(seq[n - 1])
        seq[n - 1].append(seq[n][l - 1] + seq[n - 1][prev_l - 1])
        seq[n - 1].insert(0, seq[n - 1][0] - seq[n][0])

    # The values we're after are the first and last ones on the original history.
    extrapolation_sum_a += seq[0][-1]
    extrapolation_sum_b += seq[0][0]

# Analyze your OASIS report and extrapolate the next value for each history.
# What is the sum of these extrapolated values?
print('Part One: Total sum of next values is {0}.'.format(extrapolation_sum_a))

# Analyze your OASIS report again, this time extrapolating the previous value for each history.
# What is the sum of these extrapolated values?
print('Part Two: Total sum of prev values is {0}.'.format(extrapolation_sum_b))