#!/usr/bin/env python
# -*- coding: utf-8 -*-

INITIAL_CYCLE_VALUE = 6
SUBSEQUENT_CYCLE_VALUE = 8

PART_ONE_ITERATIONS = 80
PART_TWO_ITERATIONS = 256

def simulate(fish, iterations):
	for i in range(iterations):
		next_generation = []
		l = 0
		while l < len(fish):
			# Each day, a 0 becomes a 6 and adds a new 8 to the end of the list,
			# while each other number decreases by 1 if it was present at the start of the day.
			if fish[l] == 0:
				fish[l] = INITIAL_CYCLE_VALUE
				next_generation.append(SUBSEQUENT_CYCLE_VALUE)
			else:
				fish[l] -= 1
			l += 1
		fish += next_generation

	return fish

# Parse the lanternfish population file, making two copies
with open('day06_input.txt') as f:
	lanternfish_part1 =  [int(n) for n in [line.rstrip('\n').split(',') for line in f][0]]
	lanternfish_part2 =  [n for n in lanternfish_part1]

def print_state():
	output_str = ''
	for l in lanternfish:
		output_str += '{0},'.format(l)
	print(output_str)

# Although you know nothing about this specific species of lanternfish,
# you make some guesses about their attributes. Surely, each lanternfish
# creates a new lanternfish once every 7 days.
#
# However, this process isn't necessarily synchronized between every
# lanternfish - one lanternfish might have 2 days left until it creates
# another lanternfish, while another might have 4. So, you can model
# each fish as a single number that represents the number of days until
# it creates a new lanternfish.
#
# Furthermore, you reason, a new lanternfish would surely need slightly
# longer before it's capable of producing more lanternfish: two more days
# for its first cycle.
lanternfish_part1 = simulate(lanternfish_part1, PART_ONE_ITERATIONS)
print('Part One: There are {0} lanternfish after {1} days.'.format(len(lanternfish_part1), PART_ONE_ITERATIONS))

# Suppose the lanternfish live forever and have unlimited food and space.
# Would they take over the entire ocean?

# But hey, 256 iterations is way too many.
# Let's precalculate how many lanternfish a single fish would be responsible
# for creating during half of that number of iterations (128), and then run our
# simulation for 128 iterations only. Then we'll look at the internal timer
# for each fish and determine how many fish it will create in 128 more iterations.
precalculated_lanternfish = {}
for starting_num in range(9):
	precalculated_lanternfish[starting_num] = len(simulate([starting_num], PART_TWO_ITERATIONS // 2))

# Run the simulation to the halfway point
lanternfish_part2 = simulate(lanternfish_part2, PART_TWO_ITERATIONS // 2)

# Add up the total lanternfish count at the full simulation length.
# We will lose the internal timer counts for each specific fish.
big_sum = 0
for l in range(len(lanternfish_part2)):
	big_sum += precalculated_lanternfish[lanternfish_part2[l]]
print('Part Two: There are {0} lanternfish after {1} days.'.format(big_sum, PART_TWO_ITERATIONS))