#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Digit:
	def __init__(self, segments):
		self.segments = segments

	def length(self):
		return len(self.segments)

	def __sub__(self, d):
		segments = [n for n in self.segments]
		for segment in d.segments:
			if segment in segments:
				segments.remove(segment)
		return Digit(segments)

	def __eq__(self, d):
		if len(self.segments) != len(d.segments):
			return False

		for segment in d.segments:
			if segment not in self.segments:
				return False
		return True

	def __and__(self, d):
		segments = []
		for segment in d.segments:
			if segment in self.segments:
				segments.append(segment)
		return Digit(segments)

	def remap(self, mapping):
		remapped_segments = []
		for i in range(len(self.segments)):
			remapped_segments.append(mapping[self.segments[i]])
		self.segments = remapped_segments

def digits_with_length(length):
	matches = []
	for p in patterns:
		if len(p) == length:
			matches.append(Digit(list(p)))
	return matches

def physical_digits():
	digits = {}
	digits[0] = Digit(['t', 'u', 'v', 'x', 'y', 'z'])
	digits[1] = Digit(['v', 'y'])
	digits[2] = Digit(['t', 'v', 'w', 'x', 'z'])
	digits[3] = Digit(['t', 'v', 'w', 'y', 'z'])
	digits[4] = Digit(['u', 'v', 'w', 'y'])
	digits[5] = Digit(['t', 'u', 'w', 'y', 'z'])
	digits[6] = Digit(['t', 'u', 'w', 'x', 'y', 'z'])
	digits[7] = Digit(['t', 'v', 'y'])
	digits[8] = Digit(['t', 'u', 'v', 'w', 'x', 'y', 'z'])
	digits[9] = Digit(['t', 'u', 'v', 'w', 'y', 'z'])
	return digits

# Parse the LED segments file
with open('day08_input.txt') as f:
	entries =  [line.rstrip('\n') for line in f]

# Because the digits 1, 4, 7, and 8 each use a unique number of segments,
# you should be able to tell which combinations of signals correspond to those digits.
unique_numbers = 0
for i in range(len(entries)):
	line = entries[i].split(' | ')
	for digit in line[1].split():
		if len(digit) in [2, 3, 4, 7]:
			unique_numbers += 1
print('Part One: digits 1, 4, 7 or 8 appeared {0} times.'.format(unique_numbers))

digits = physical_digits()

output_sum = 0
for i in range(len(entries)):
	# Using this information, you should be able to work out which combination of signal wires
	# corresponds to each of the ten digits. Then, you can decode the four digit output value.

	# The scrambled segments use letters a-g, and we are trying to find
	# how they map to numeric digits, so let's use a different set of letters
	# to refer to the physical segments: t-z.
	#  tttt
	# u    v
	# u    v
	#  wwww
	# x    y
	# x    y
	#  zzzz
	#
	# Start by building representations of the physical segments that will be lit
	# for each digit. We'll map these segments to signal wires later.
	digits = physical_digits()
	mapping = {}

	# Split the input into patterns and digits
	patterns = entries[i].split(' | ')[0].split()
	unknown_digits = entries[i].split(' | ')[1].split()

	# There are four digits with unique numbers of segments lit up:
	# 1 (two segments)
	# 4 (four segments)
	# 7 (three segments)
	# 8 (seven segments)
	one = digits_with_length(2)[0]
	four = digits_with_length(4)[0]
	seven = digits_with_length(3)[0]
	eight = digits_with_length(7)[0]

	# Digits 7 and 1 have unique lengths and differ only by the top LED segment (t),
	# so we can figure out its mapping right away.
	mapping['t'] = (seven - one).segments[0]

	# Digits 0, 6 and 9 have the same number of lit segments (six), but only 6
	# does not use both of the segments that 1 does. Therefore we can determine
	# the mapping for LED segments (v) and (y) by isolating digit 6, which will
	# share segment (y) with 1, and then the other segment from 1 must be (v).
	zero_six_and_nine = digits_with_length(6)
	for d in zero_six_and_nine:
		if len((one & d).segments) < 2:
			six = d
			mapping['v'] = (one - six).segments[0]
			mapping['y'] = (one & six).segments[0]
			break

	# Now we need to determine which of the other digits is 0 and which is 9.
	zero_six_and_nine.remove(six)
	if len((zero_six_and_nine[0] & four).segments) == 4:
		nine = zero_six_and_nine[0]
		zero = zero_six_and_nine[1]
	else:
		zero = zero_six_and_nine[0]
		nine = zero_six_and_nine[1]

	# Now we've identified the digits 0, 1, 4, 7, 8, 9 and the physical LED
	# segments (t), (v), and (y). We can then use simple operations on these
	# digits to identify the remaining LED segments: (u), (w), (x), and (z).
	mapping['u'] = ((zero & four) - one).segments[0]
	mapping['w'] = (eight - zero).segments[0]
	mapping['x'] = (eight - nine).segments[0]
	mapping['z'] = (nine - seven - four).segments[0]

	# Now we have our full mapping for all seven LED segments.
	# Remap the physical segments to the logical (aka input wires).
	for d in digits:
		digits[d].remap(mapping)

	# Now match each digit to an 0-9 ordinal and build the sum.
	local_sum = 0
	for unknown_digit in unknown_digits:
		u = Digit(list(unknown_digit))
		for d in digits:
			if u == digits[d]:
				local_sum = (10 * local_sum) + d
	output_sum += local_sum

print('Part Two: Sum of all output values is {0}.'.format(output_sum))