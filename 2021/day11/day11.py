#!/usr/bin/env python
# -*- coding: utf-8 -*-

NEIGHBORS = [(-1, -1),
             (-1,  0),
             (-1,  1),
             ( 0, -1),
             ( 0,  1),
             ( 1, -1),
             ( 1,  0),
             ( 1,  1)]

FLASH_ENERGY = 10
ITERATIONS = 100

def increase_energy(x, y):
	dumbos[(x, y)] += 1
	if dumbos[(x, y)] == FLASH_ENERGY:
		for n in NEIGHBORS:
			if (x + n[0], y + n[1]) in dumbos:
				increase_energy(x + n[0], y + n[1])

def step():
	global flashes
	synchronized = True
	grid_size = int(len(dumbos) ** 0.5)

	# During a single step, the following occurs:
	#
	# First, the energy level of each octopus increases by 1.
	#
	# Then, any octopus with an energy level greater than 9 flashes.
	#
	# This increases the energy level of all adjacent octopuses by 1,
	# including octopuses that are diagonally adjacent. If this causes 
	# n octopus to have an energy level greater than 9, it also flashes.
	# This process continues as long as new octopuses keep having their
	# energy level increased beyond 9. (An octopus can only flash at most
	# once per step.)
	#
	# Finally, any octopus that flashed during this step has its energy
	# level set to 0, as it used all of its energy to flash.
	for x in range(grid_size):
		for y in range(grid_size):
			increase_energy(x, y)

	for x in range(grid_size):
		for y in range(grid_size):
			if dumbos[(x, y)] >= FLASH_ENERGY:
				flashes += 1
				dumbos[(x, y)] = 0
			else:
				synchronized = False
	return synchronized

# Parse the dumbo octopi energy file
with open('day11_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

dumbos = {}
flashes = 0
for y in range(len(lines)):
	for x in range(len(lines[y])):
		dumbos[(x, y)] = int(lines[y][x])

# If you can calculate the exact moments when the octopuses will all flash
# simultaneously, you should be able to navigate through the cavern.
# What is the first step during which all octopuses flash?
i = 0
synchronized = False
while not synchronized:
	synchronized = step()
	if i == 100:
		# Given the starting energy levels of the dumbo octopuses in your cavern,
		# simulate 100 steps. How many total flashes are there after 100 steps?
		print('Part One: There were {0} total flashes after {1} steps.'.format(flashes, ITERATIONS))
	i += 1
print('Part Two: All dumbo octopi flashed on step {0}.'.format(i))