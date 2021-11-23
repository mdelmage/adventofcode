#!/usr/bin/env python
# -*- coding: utf-8 -*-

FACTOR_A = 16807
FACTOR_B = 48271
DIVISOR = 2147483647
PAIR_COUNT_PART_ONE = 40000000
PAIR_COUNT_PART_TWO = 5000000

# Parse the initial values file
with open('day15_input.txt') as f:
    initial_values = [line.rstrip('\n').split(' starts with ') for line in f]

val_a = int(initial_values[0][1])
val_b = int(initial_values[1][1])

i = 0
matches = 0
while i < PAIR_COUNT_PART_ONE:
	# The generators both work on the same principle. To create its next value, a generator
	# will take the previous value it produced, multiply it by a factor (generator A uses 16807;
	# generator B uses 48271), and then keep the remainder of dividing that resulting product
	# by 2147483647. That final remainder is the value it produces next.
	val_a = ((val_a * FACTOR_A) % DIVISOR)
	val_b = ((val_b * FACTOR_B) % DIVISOR)
	i += 1
	if (val_a & 0xffff) == (val_b & 0xffff): matches += 1

print 'Part One: {0} matches in the first {1} pairs.'.format(matches, i)

# In the interest of trying to align a little better, the generators get more picky
# about the numbers they actually give to the judge.
#
# They still generate values in the same way, but now they only hand a value
# to the judge when it meets their criteria:
#
# Generator A looks for values that are multiples of 4.
# Generator B looks for values that are multiples of 8.
# Each generator functions completely independently: they both go through values
# entirely on their own, only occasionally handing an acceptable value to the judge,
# and otherwise working through the same sequence of values as before until they find one.
val_a = int(initial_values[0][1])
val_b = int(initial_values[1][1])

i = 0
matches = 0
while i < PAIR_COUNT_PART_TWO:
	val_a = ((val_a * FACTOR_A) % DIVISOR)
	while ((val_a % 4) > 0):
		val_a = ((val_a * FACTOR_A) % DIVISOR)

	val_b = ((val_b * FACTOR_B) % DIVISOR)
	while ((val_b % 8) > 0):
		val_b = ((val_b * FACTOR_B) % DIVISOR)

	i += 1
	if (val_a & 0xffff) == (val_b & 0xffff): matches += 1

print 'Part Two: {0} matches in the first {1} pairs.'.format(matches, i)