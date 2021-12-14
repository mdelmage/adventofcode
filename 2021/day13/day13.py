#!/usr/bin/env python
# -*- coding: utf-8 -*-

def print_grid(x, y):
	for row in range(y + 1):
		str = ''
		for col in range(x + 1):
			str += paper.get((col, row), ' ')
		print(str)
	print('')

def fold_horizontal(column):
	# Each instruction indicates a line on the transparent paper
	# and wants you to fold the paper up (for horizontal y=... lines)
	# or left (for vertical x=... lines).
	global paper
	new_paper = {}
	for (x, y) in paper:
		if x > column:
			new_paper[((2 * column) - x, y)] = '█'
		else:
			new_paper[(x, y)] = '█'

	paper = new_paper
	return column - 1

def fold_vertical(row):
	# Each instruction indicates a line on the transparent paper
	# and wants you to fold the paper up (for horizontal y=... lines)
	# or left (for vertical x=... lines).
	global paper
	new_paper = {}
	for (x, y) in paper:
		if y > row:
			new_paper[(x, (2 * row) - y)] = '█'
		else:
			new_paper[(x, y)] = '█'

	paper = new_paper
	return row - 1

# Parse the transparent paper file
with open('day13_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

folds = []
paper = {}
max_x = 0
max_y = 0
part_one_complete = False
for line in lines:
	if ',' in line:
		(x, y) = [int(n) for n in line.split(',')]
		paper[(x, y)] = '█'
		if x > max_x: max_x = x
		if y > max_y: max_y = y
	elif 'fold' in line:
		instruction = line[11:].split('=')
		folds.append((instruction[0], int(instruction[1])))

# Finish folding the transparent paper according to the instructions.
# The manual says the code is always eight capital letters.
for (axis, value) in folds:
	if axis == 'y': max_y = fold_vertical(value)
	elif axis == 'x': max_x = fold_horizontal(value)
	if not part_one_complete:
		print('Part One: {0} dots are visible after completing the first fold instruction.'.format(len(paper)))
		part_one_complete = True

print('Part Two: activation code is')
print_grid(max_x, max_y)