#!/usr/bin/env python
# -*- coding: utf-8 -*-

def generate_bit_histogram(numbers):
	bit_len = len(numbers[0])

	# Zero-initialize the dictionary to make life easier
	bit_freq = {}
	for i in range(bit_len):
		bit_freq[(i, '0')] = 0
		bit_freq[(i, '1')] = 0

	for number in numbers:
		for bit_num in range(bit_len):
			bit_val = number[bit_num]
			bit_freq[(bit_num, bit_val)] += 1
	return bit_freq

# Parse the diagnostic report file
with open('day03_input.txt') as f:
	diag = [line.rstrip('\n') for line in f]

bit_freq = generate_bit_histogram(diag)
bit_len = len(diag[0])

epsilon = 0
gamma = 0
for bit_num in range(bit_len):
	epsilon <<= 1
	gamma <<= 1
	if bit_freq[(bit_num, '0')] <= bit_freq[(bit_num, '1')]:
		# Each bit in the gamma rate can be determined by finding the most common bit
		# in the corresponding position of all numbers in the diagnostic report.
		gamma += 1
	else:
		# The epsilon rate is calculated in a similar way; rather than use the
		# most common bit, the least common bit from each position is used.
		epsilon += 1

print('Part One: Submarine power consumption is {0}.'.format(epsilon * gamma))

# Both the oxygen generator rating and the CO2 scrubber rating are values that
# can be found in your diagnostic report - finding them is the tricky part.
# Both values are located using a similar process that involves filtering out
# values until only one remains. Before searching for either rating value,
# start with the full list of binary numbers from your diagnostic report
# and consider just the first bit of those numbers. Then:
#
# Keep only numbers selected by the bit criteria for the type of rating value
# for which you are searching. Discard numbers which do not match the bit criteria.
#
# If you only have one number left, stop; this is the rating value for which you are searching.
#
# Otherwise, repeat the process, considering the next bit to the right.
oxygen_numbers = [i for i in diag]
bit_num = 0
while len(oxygen_numbers) > 1:
	bit_freq = generate_bit_histogram(oxygen_numbers)
	new_numbers = []
	# To find oxygen generator rating, determine the most common value (0 or 1)
	# in the current bit position, and keep only numbers with that bit in that position.
	# If 0 and 1 are equally common, keep values with a 1 in the position being considered.
	if bit_freq[(bit_num, '0')] <= bit_freq[(bit_num, '1')]:
		bit = '1'
	else:
		bit = '0'

	for number in oxygen_numbers:
		if number[bit_num] == bit:
			new_numbers.append(number)
	oxygen_numbers = new_numbers
	bit_num += 1

# Convert binary string to integer
oxygen_rating = int(oxygen_numbers[0], 2)

co2_numbers = [i for i in diag]
bit_num = 0
while len(co2_numbers) > 1:
	bit_freq = generate_bit_histogram(co2_numbers)
	new_numbers = []
	# To find CO2 scrubber rating, determine the least common value (0 or 1) in the current
	# bit position, and keep only numbers with that bit in that position. If 0 and 1 are
	# equally common, keep values with a 0 in the position being considered.
	if bit_freq[(bit_num, '0')] > bit_freq[(bit_num, '1')]:
		bit = '1'
	else:
		bit = '0'

	for number in co2_numbers:
		if number[bit_num] == bit:
			new_numbers.append(number)
	co2_numbers = new_numbers
	bit_num += 1

# Convert binary string to integer
co2_rating = int(co2_numbers[0], 2)

# Next, you should verify the life support rating, which can be determined
# by multiplying the oxygen generator rating by the CO2 scrubber rating.
print('Part Two: Life support rating of the submarine is {0}.'.format(oxygen_rating * co2_rating))