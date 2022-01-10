#!/usr/bin/env python
# -*- coding: utf-8 -*-

MODEL_NUMBER_LENGTH = 14

def execute(position, digit, prev_value):
	w = digit
	z = prev_value
	(div, add1, add2) = params[position]

	# By inspection: this is the distilled logic of the MONAD program.
	# For each digit in the model number, it runs a fixed set of math operations,
	# differing only by a divisor value and arguments to two sums.
	#
	# Retrieve those from the saved params structure.
	x = z % 26
	z //= div
	x += add1
	x = 0 if x == w else 1
	z *= (25 * x) + 1
	z += (w + add2) * x

	# Return the value in Register Z to the next stage of the program.
	return z

hits = 0
def model_number(r, number=0, depth=1, prev_value=0):
	global hits
	# By inspection: some operations have the possibility to divide the passed-in value
	# by 26. If the passed-in value is larger than 26^n by this stage, we won't be able
	# to reduce it to zero before we run out of digits to process.
	#
	# So if the running total is greater than 26^n, bail out.
	if prev_value > 26 ** (MODEL_NUMBER_LENGTH - depth + 1):
		return

	# Add another digit to our candidate number. Check the result.
	for digit in r:
		next_value = execute(depth, digit, prev_value)
		candidate_number = number * 10 + digit
		if depth == MODEL_NUMBER_LENGTH and next_value == 0:
			# Done! Bail out.
			return(candidate_number)
		else:
			# Recursive search to find the next digit, in the order given by the range (r).
			result = model_number(r, candidate_number, depth + 1, next_value)
			if result: return result

	return None

# Parse the MONAD program file
with open('day24_input.txt') as f:
	program = [line.rstrip('\n') for line in f]

sub = 0
line = 0
params = {}
while line < len(program):
	sub += 1
	# By inspection: the program is a chained math problem, with three variables for each
	# model number digit: a divisor and two sums.
	#
	# Save these parameters to inject into the calculations.
	div = int(program[line + 4].split()[2])
	add1 = int(program[line + 5].split()[2])
	add2 = int(program[line + 15].split()[2])
	params[sub] = [div, add1, add2]
	line += 18

decreasing_range = range(9, 0, -1)
increasing_range = range(1, 10)
print('Part One: Largest submarine model number accepted by MONAD is {0}.'.format(model_number(decreasing_range)))
print('Part Two: Smallest submarine model number accepted by MONAD is {0}.'.format(model_number(increasing_range)))