#!/usr/bin/env python
# -*- coding: utf-8 -*-

NEIGHBORS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BIG_RISK = 12345678
LOL_ITERATIONS = 10

def navigate(grid):
	# You start in the top left position, your destination is the bottom right position,
	# and you cannot move diagonally. The number at each position is its risk level;
	# to determine the total risk of an entire path, add up the risk levels of each position
	# you enter (that is, don't count the risk level of your starting position unless you
	# enter it; leaving it adds no risk to your total).
	#
	# Your goal is to find a path with the lowest total risk.
	grid_size = int(len(grid) ** 0.5)
	min_risk = {(0, 0): 0}
	for iteration in range(LOL_ITERATIONS):
		for i in range(2, grid_size + 1):
			for x in range(i):
				for y in range(i):
					if x == i - 1 or y == i - 1:
						if (x, y) not in min_risk: min_risk[(x, y)] = BIG_RISK
						for n in NEIGHBORS:
							if min_risk.get((x + n[0], y + n[1]), BIG_RISK) + grid.get((x, y), BIG_RISK) < min_risk[(x, y)]:
								min_risk[(x, y)] = min_risk.get((x + n[0], y + n[1]), BIG_RISK) + grid.get((x, y), BIG_RISK)
	return (min_risk[(grid_size - 1, grid_size - 1)])

# Parse the risk level map file
with open('day15_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

# Generate the risk lookup table (dict).
risk = {}
for y in range(len(lines)):
	for x in range(len(lines)):
		risk[(x, y)] = int(lines[y][x])

print('Part One: Total risk of the safest path is {0}.'.format(navigate(risk)))

# The entire cave is actually five times larger in both dimensions than you thought;
# the area you originally scanned is just one tile in a 5x5 tile area that forms the full map.
# Your original map tile repeats to the right and downward; each time the tile repeats
# to the right or downward, all of its risk levels are 1 higher than the tile immediately
# up or left of it. However, risk levels above 9 wrap back around to 1.
big_grid = {}
grid_size = int(len(risk) ** 0.5)
for (x, y) in risk:
	for i in range(5):
		for j in range(5):
			new_risk = risk[(x, y)] + i + j
			if new_risk > 9:
				new_risk = (new_risk + 1) % 10
			big_grid[(x + (grid_size * i), y + (grid_size * j))] = new_risk

risk = big_grid

print('Part Two: Total risk of the safest path is {0}.'.format(navigate(risk)))
