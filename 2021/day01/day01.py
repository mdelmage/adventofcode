#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the sonar sweep report file
with open('day01_input.txt') as f:
	depth_reports = [int(line.rstrip('\n')) for line in f]

# The first order of business is to figure out how quickly the depth increases,
# just so you know what you're dealing with - you never know if the keys will
# get carried into deeper water by an ocean current or a fish or something.
#
# To do this, count the number of times a depth measurement increases from the previous measurement.
depth_increases = 0
i = 1
while i < len(depth_reports):
	if depth_reports[i] > depth_reports[i - 1]:
		depth_increases += 1
	i += 1

print('Part One: {0} measurements were larger than the previous measurement.'.format(depth_increases))

# Considering every single measurement isn't as useful as you expected: there's just too much noise in the data.
#
# Instead, consider sums of a three-measurement sliding window.
depth_increases = 0
i = 3
while i < len(depth_reports):
	if depth_reports[i - 0] + depth_reports[i - 1] + depth_reports[i - 2] > \
	   depth_reports[i - 1] + depth_reports[i - 2] + depth_reports[i - 3]:
		depth_increases += 1
	i += 1

print('Part Two: {0} measurements were larger than the previous measurement.'.format(depth_increases))