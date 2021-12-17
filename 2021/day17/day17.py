#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Artificially cap how fast we can launch our probe.
# Select this value carefully, or else we might lose valid
# shot selections.
MAX_Y_VELOCITY = 1000

def tick(pos, vel):
	# On each step, these changes occur in the following order:
	#
	# The probe's x position increases by its x velocity.
	# The probe's y position increases by its y velocity.
	pos = (pos[0] + vel[0], pos[1] + vel[1])

	# Due to drag, the probe's x velocity changes by 1 toward the value 0;
	# that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0,
	# or does not change if it is already 0.
	if vel[0] > 0:
		vel = (vel[0] - 1, vel[1])
	elif vel[0] < 0:
		vel = (vel[0] + 1, vel[1])

	# Due to gravity, the probe's y velocity decreases by 1.
	vel = (vel[0], vel[1] - 1)

	return (pos, vel)

# Parse the transmission packets file
with open('day17_input.txt') as f:
	for line in f:
		(x, y) = line.split('target area: x=')[1:][0].split(', y=')
		(x_min, x_max) = [int(n) for n in x.split('..')]
		(y_min, y_max) = [int(n) for n in y.split('..')]


# Find the initial velocity that causes the probe to reach the highest y position
# and still eventually be within the target area after any step. What is the highest
# y position it reaches on this trajectory?
apogee_max = 0
apogee_max_y_vel = 0

# Only consider Y velocity. No need to care about X yet.
for initial_y_vel in range(MAX_Y_VELOCITY):
	pos = (0, 0)
	vel = (0, initial_y_vel)
	apogee = 0

	while pos[1] >= y_min:
		(pos, vel) = tick(pos, vel)
		apogee = max(apogee, pos[1])
		if pos[1] >= y_min and pos[1] <= y_max:
			# Match!
			if apogee > apogee_max:
				apogee_max = apogee
				apogee_max_y_vel = initial_y_vel

print('Part One: best apogee was {0}.'.format(apogee_max))

# Maybe a fancy trick shot isn't the best idea; after all, you only have one probe,
# so you had better not miss.
#
# To get the best idea of what your options are for launching the probe, you need to find
# every initial velocity that causes the probe to eventually be within the target area after any step.
hits = set()

# Cut down the range of test values by being a little clever:

# Any X velocity too low will never hit the target.
if x_min < 0:
	search_x_min = x_min
else:
	search_x_min = 0

# Any X velocity that puts us past the target area after only one tick, is too high.
if x_max < 0:
	search_x_max = 0
else:
	search_x_max = x_max

# Any Y velocity that puts us past the target area after only one tick, is too low.
# Any Y velocity higher than the one that helped us in Part One, is too high.
search_y_min = y_min
search_y_max = apogee_max_y_vel

for initial_x_vel in range(search_x_min, search_x_max + 1):
	for initial_y_vel in range(search_y_min, search_y_max + 1):
		pos = (0, 0)
		vel = (initial_x_vel, initial_y_vel)

		while pos[1] >= y_min:
			(pos, vel) = tick(pos, vel)
			if pos[0] >= x_min and pos[0] <= x_max and pos[1] >= y_min and pos[1] <= y_max:
				# Match!
				hits.add((initial_x_vel, initial_y_vel))

print('Part Two: there were {0} distinct initial velocity values that landed in the target area.'.format(len(hits)))