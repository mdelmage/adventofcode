#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Each change of 1 step in horizontal position of a single crab costs 1 fuel.
def calculate_fuel_linear(alignment_point):
	total_fuel_burned = 0
	for i in range(len(crabs)):
		total_fuel_burned += abs(crabs[i] - alignment_point)
	return total_fuel_burned

# As it turns out, crab submarine engines don't burn fuel at a constant rate.
# Instead, each change of 1 step in horizontal position costs 1 more unit of fuel
# than the last: the first step costs 1, the second step costs 2, the third step
# costs 3, and so on.
def calculate_fuel_nonlinear(alignment_point):
	total_fuel_burned = 0
	for i in range(len(crabs)):
		local_fuel_burned = 0
		for j in range(abs(crabs[i] - alignment_point)):
			local_fuel_burned += j + 1
		total_fuel_burned += local_fuel_burned
	return total_fuel_burned

# Parse the crab submarine positions file
with open('day07_input.txt') as f:
	crabs =  [int(n) for n in [line.rstrip('\n').split(',') for line in f][0]]

# Crab submarines have limited fuel, so you need to find a way to make
# all of their horizontal positions match while requiring them to spend
# as little fuel as possible.

# For linear fuel cost, that's just the median.
crabs.sort()
median = crabs[len(crabs) // 2]
print('Part One: Total fuel burned was {0}.'.format(calculate_fuel_linear(median)))

# For nonlinear fuel cost, let's just brute-force it.
best_fuel = float('inf')
for loc in range(min(crabs), max(crabs) + 1):
	fuel_burned = calculate_fuel_nonlinear(loc)
	if fuel_burned < best_fuel:
		best_fuel = fuel_burned
print('Part Two: Total fuel burned was {0}.'.format(best_fuel))