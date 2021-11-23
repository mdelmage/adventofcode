#!/usr/bin/env python
# -*- coding: utf-8 -*-

STEP_COUNT = 377
INSERTION_COUNT_A = 2017
INSERTION_COUNT_B = 50000000

buffer = [0]
cur_pos = 0
insertion_val = 1

# This spinlock's algorithm is simple but efficient, quickly consuming everything in its path.
# It starts with a circular buffer containing only the value 0, which it marks as the current position.
# It then steps forward through the circular buffer some number of steps (your puzzle input) before
# inserting the first new value, 1, after the value it stopped on. The inserted value becomes
# the current position. Then, it steps forward from there the same number of steps, and wherever it stops,
# inserts after it the second new value, 2, and uses that as the new current position again.
while insertion_val <= INSERTION_COUNT_A:
	insertion_point = ((cur_pos + STEP_COUNT) % len(buffer)) + 1
	buffer.insert(insertion_point, insertion_val)

	if insertion_val == INSERTION_COUNT_A:
		print 'Part One: Value after {0} is {1}.'.format(insertion_val, buffer[(insertion_point + 1) % len(buffer)])

	insertion_val += 1
	cur_pos = insertion_point

cur_pos = 0
insertion_val = 1
target_value = 0

# The good news is that you have improved calculations for how to stop the spinlock.
# They indicate that you actually need to identify the value after 0 in the current state of the circular buffer.
#
# The bad news is that while you were determining this, the spinlock has just finished inserting
# its fifty millionth value (50000000).
while insertion_val <= INSERTION_COUNT_B:
	insertion_point = ((cur_pos + STEP_COUNT) % insertion_val) + 1

	# Don't actually perform the insert, just track when we're placing things next to 0 (which is always at index 0)
	if insertion_point == 1:
		target_value = insertion_val

	insertion_val += 1
	cur_pos = insertion_point

print 'Part Two: Value after 0 is {0}.'.format(target_value)