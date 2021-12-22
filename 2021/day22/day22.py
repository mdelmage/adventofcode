#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Cuboid:
	def __init__(self, limits):
		self.x_min = limits[0]
		self.x_max = limits[1]
		self.y_min = limits[2]
		self.y_max = limits[3]
		self.z_min = limits[4]
		self.z_max = limits[5]

	def __str__(self):
		if self.x_min > self.x_max or self.y_min > self.y_max or self.z_min > self.z_max:
			return '<invalid>'
		else:
			return '({0}..{1}, {2}..{3}, {4}..{5})'.format(self.x_min,
				                                           self.x_max,
				                                           self.y_min,
				                                           self.y_max,
			    	                                       self.z_min,
			        	                                   self.z_max)

	def __eq__(self, c):
		return self.x_min == c.x_min and \
		       self.x_max == c.x_max and \
		       self.y_min == c.y_min and \
		       self.y_max == c.y_max and \
		       self.z_min == c.z_min and \
		       self.z_max == c.z_max

	def __and__(self, c):
		# Return the intersection of two cuboids.
		x_min = max(self.x_min, c.x_min)
		x_max = min(self.x_max, c.x_max)
		y_min = max(self.y_min, c.y_min)
		y_max = min(self.y_max, c.y_max)
		z_min = max(self.z_min, c.z_min)
		z_max = min(self.z_max, c.z_max)
		return Cuboid([x_min, x_max, y_min, y_max, z_min, z_max])

	def __or__(self, c):
		# Return the bounding box of the union of two cuboids.
		# This will likely not have the same size or shape as the union itself,
		# unless there is a matching and adjacent face on each cube.
		# Otherwise, the union of two cuboids is not a cuboid.
		x_min = min(self.x_min, c.x_min)
		x_max = max(self.x_max, c.x_max)
		y_min = min(self.y_min, c.y_min)
		y_max = max(self.y_max, c.y_max)
		z_min = min(self.z_min, c.z_min)
		z_max = max(self.z_max, c.z_max)
		return Cuboid([x_min, x_max, y_min, y_max, z_min, z_max])

	def __sub__(self, c):
		# If there's no intersection between the two cuboids, the subtraction is simply
		# the original shape.
		if (self & c).size() == 0:
			return [self]

		# Bound the subtraction to within our own cuboid.
		# We don't care about any dimensions that the subtracting shape extends past us.
		c = Cuboid([c.x_min, c.x_max, c.y_min, c.y_max, c.z_min, c.z_max])
		if c.x_min < self.x_min: c.x_min = self.x_min
		if c.x_max > self.x_max: c.x_max = self.x_max
		if c.y_min < self.y_min: c.y_min = self.y_min
		if c.y_max > self.y_max: c.y_max = self.y_max
		if c.z_min < self.z_min: c.z_min = self.z_min
		if c.z_max > self.z_max: c.z_max = self.z_max

		# Now generate a sorted list of the critical dimensions:
		# the boundaries of each cuboid axis.
		x = [self.x_min, self.x_max, c.x_min, c.x_max]
		y = [self.y_min, self.y_max, c.y_min, c.y_max]
		z = [self.z_min, self.z_max, c.z_min, c.z_max]

		x.sort()
		y.sort()
		z.sort()

		# We'll generate three slices on each axis, cutting ourselves up
		# into 27 pieces.
		x = [[x[0], x[1] - 1], [x[1], x[2]], [x[2] + 1, x[3]]]
		y = [[y[0], y[1] - 1], [y[1], y[2]], [y[2] + 1, y[3]]]
		z = [[z[0], z[1] - 1], [z[1], z[2]], [z[2] + 1, z[3]]]

		# Go through each of the 27 pieces and extract all the valid sub-cuboids
		# that aren't the subtracting shape itself.
		subcuboids = []
		for (x_min, x_max) in x:
			for (y_min, y_max) in y:
				for (z_min, z_max) in z:
					subcuboid = Cuboid([x_min, x_max, y_min, y_max, z_min, z_max])
					if subcuboid.size() > 0 and subcuboid != c:
						subcuboids.append(subcuboid)

		return subcuboids

	def size(self):
		if self.x_min > self.x_max or self.y_min > self.y_max or self.z_min > self.z_max:
			# Invalid shape!
			return 0
		else:
			return (self.x_max - self.x_min + 1) * (self.y_max - self.y_min + 1) * (self.z_max - self.z_min + 1)

def run(limit):
	cuboids = []
	for i in range(len(instructions)):
		(new_cuboid, line) = instructions[i]

		if limit:
			# Execute the reboot steps. Afterward, considering only cubes in the region
			# x=-50..50,y=-50..50,z=-50..50, how many cubes are on?
			new_cuboid = new_cuboid & Cuboid([-50, 50, -50, 50, -50, 50])

		new_cuboids = []
		for existing_cuboid in cuboids:
			# Whether we're turing cubes off or on, the first step is to turn off
			# any cubes that are contained within the cuboid of the current instruction.
			# If we're turning cubes on, we don't want any overlapping regions between
			# the existing cuboids and the one we're adding to the list.
			new_cuboids += existing_cuboid - new_cuboid

		if 'on' in line:
			# We've cleared a space -- it is safe to add the new cuboid
			new_cuboids.append(new_cuboid)

		cuboids = new_cuboids

	return sum([c.size() for c in cuboids])

# Parse the reboot steps file
with open('day22_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

instructions = []
for line in lines:
	subline = line[line.find(' ') + 1:]
	subline = subline.replace('x', '')
	subline = subline.replace('y', '')
	subline = subline.replace('z', '')
	subline = subline.replace('=', '')
	subline = subline.replace('..', ',')
	instructions.append([Cuboid([int(n) for n in subline.split(',')]), line])

print('Part One: {0} cubes were on after performing a limited reboot.'.format(run(limit=True)))
print('Part Two: {0} cubes were on after rebooting.'.format(run(limit=False)))