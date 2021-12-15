#!/usr/bin/env python
# -*- coding: utf-8 -*-

ITERATIONS_PART_ONE = 10
ITERATIONS_PART_TWO = 40

def string_to_dict(s):
	element_count = {}
	for ch in s:
		element_count[ch] = element_count.get(ch, 0) + 1
	return element_count

def score_a_string(s):
	return score_a_dict(string_to_dict(s))

def score_a_dict(d):
	# Sort the dictionary, subtract the least-common value from the most-common, and
	# return the difference to the caller.
	sorted_element_count = sorted(d.items(), reverse=True, key=lambda item: item[1])
	return sorted_element_count[0][1] - sorted_element_count[-1][1]

def generate_polymer(seed, iterations):
	polymer = seed
	for i in range(iterations):
		new_polymer = ''
		for j in range(len(polymer) - 1):
			# For each pair in the polymer, generate the new chain.
			new_polymer += polymer[j] + pairs[polymer[j] + polymer[j + 1]]

		# Add the last element back to the end of the polymer.
		polymer = new_polymer + polymer[j + 1]
	return polymer

# Parse the polymer formula instructions file
with open('day14_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

# The first line is the polymer template - this is the starting point of the process.
seed = lines[0]

# The following section defines the pair insertion rules.
# A rule like AB -> C means that when elements A and B are immediately adjacent,
# element C should be inserted between them. These insertions all happen simultaneously.
pairs = {}
for i in range(2, len(lines)):
	(x, y) = lines[i].split(' -> ')
	pairs[x] = y

# Apply 10 steps of pair insertion to the polymer template and find the most and least
# common elements in the result. What do you get if you take the quantity of the most
# common element and subtract the quantity of the least common element?
polymer = generate_polymer(seed, ITERATIONS_PART_ONE)
print('Part One: Most common element minus least common, after {0} iterations, is {1}.'.format(ITERATIONS_PART_ONE, score_a_string(polymer)))

# The resulting polymer isn't nearly strong enough to reinforce the submarine.
# You'll need to run more steps of the pair insertion process; a total of 40 steps should do it.
#
# However, things get out of hand really quickly as far as the length of the polymer.
# We'll never be able to generate the deterministic, ordered polymer chain, but we can do
# a trick: take each pair rule, generate a full polymer for half of the iterations, and then
# save the aggregate element counts. Then, we generate a full polymer for half of the iterations,
# and use the previously generated data to calculate the aggregate counts for the full run.

# Generate aggregate data for each pair insertion rule.
halfway_counts = {}
for pair in pairs:
	halfway_counts[pair] = string_to_dict(generate_polymer(pair, ITERATIONS_PART_TWO // 2))

# Start with the seed from the input file and generate a full polymer, but only halfway.
polymer = generate_polymer(seed, ITERATIONS_PART_TWO // 2)

# Now use the data from the pair insertion rules (the aggregate halfway data) to get us
# the rest of the way there.
full_counts = {}
for i in range(len(polymer) - 1):
	pair = polymer[i] + polymer[i + 1]
	for element in halfway_counts[pair]:
		full_counts[element] = full_counts.get(element, 0) + halfway_counts[pair][element]

# Small Correction 1: We've double-counted elements for each seed. Remove those.
for i in range(len(seed) - 1):
	counts = halfway_counts[seed[i] + seed[i + 1]]
	for element in counts:
		full_counts[element] -= counts[element]

# Small Correction 2: We need to add back the elements from the original seed.
for element in seed:
	full_counts[element] += 1

print('Part Two: Most common element minus least common, after {0} iterations, is {1}.'.format(ITERATIONS_PART_TWO, score_a_dict(full_counts)))