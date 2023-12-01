#!/usr/bin/env python
# -*- coding: utf-8 -*-

# On each line, the calibration value can be found by combining the first digit and the last digit
# (in that order) to form a single two-digit number.
def calibration_value(line):
    first_digit = None
    last_digit = None
    for c in line:
        if c.isdigit():
            if not first_digit: first_digit = int(c)
            last_digit = int(c)

    return (10 * first_digit) + last_digit

# Parse the calibration document
with open('day01_input.txt') as f:
    calibrations = [line.rstrip('\n') for line in f]

# The newly-improved calibration document consists of lines of text;
# each line originally contained a specific calibration value that the Elves now need to recover.
calibration_sum = 0
for cal in calibrations:
    calibration_sum += calibration_value(cal)

# Consider your entire calibration document. What is the sum of all of the calibration values?
print('Part One: Sum of all the calibration values is {0}.'.format(calibration_sum))

# Your calculation isn't quite right. It looks like some of the digits are actually spelled out
# with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".
digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

# Equipped with this new information, you now need to find the real first and last digit on each line.
calibration_sum = 0
for cal in calibrations:
    # One thing left ambiguous in the puzzle description is the evaluation strategy for overlapping words.
    # For example, does eightwo count as '8 and 2', or just '8'?
    # By trial-and-error, it seems that '8 and 2' is the correct answer.
    parsed_cal = ''
    for i in range(len(cal)):
        if cal[i].isdigit():
            # String digit; send it through
            parsed_cal += cal[i]
        else:
            # Check for a written digit, send any matches through
            for j in range(len(digits)):
                d = digits[j]
                if cal[i:i+len(d)] == d: parsed_cal += str(j + 1)
    cal = parsed_cal
    calibration_sum += calibration_value(cal)

# What is the sum of all of the calibration values?
print('Part Two: Sum of all the calibration values is {0}.'.format(calibration_sum))
