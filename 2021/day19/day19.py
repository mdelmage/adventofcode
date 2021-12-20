#!/usr/bin/env python
# -*- coding: utf-8 -*-

remap_axes = [
{0: 0, 1: 1, 2: 2},
{0: 0, 1: 2, 2: 1},
{0: 1, 1: 0, 2: 2},
{0: 1, 1: 2, 2: 0},
{0: 2, 1: 1, 2: 0},
{0: 2, 1: 0, 2: 1}]

remap_dirs = [
( 1,  1,  1),
( 1,  1, -1),
( 1, -1,  1),
( 1, -1 ,-1),
(-1,  1,  1),
(-1,  1, -1),
(-1, -1,  1),
(-1, -1, -1)]

def remap(coord, axis, dir):
	return (coord[axis[0]] * dir[0], coord[axis[1]] * dir[1], coord[axis[2]] * dir[2])

def manhattan_dist(c1, c2):
	return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])

def remap2(coord, source, target):
	(axis, dir, offset) = remap_guide[source, target]
	return (coord[axis[0]] * dir[0] + offset[0], coord[axis[1]] * dir[1] + offset[1], coord[axis[2]] * dir[2] + offset[2])

def generate(source, intermediate, target):
	(axis1, dir1, offset1) = remap_guide[source, intermediate]
	(axis2, dir2, offset2) = remap_guide[intermediate, target]
	offset = remap2(remap2((0, 0, 0), source, intermediate), intermediate, target)

	offseted = remap2(remap2((1,2,3), source, intermediate), intermediate, target)
	unoffseted = (offseted[0] - offset[0], offseted[1] - offset[1], offseted[2] - offset[2])
	axis = tuple([abs(n) - 1 for n in unoffseted])
	dir = tuple([1 if n > 0 else -1 for n in unoffseted])

	remap_guide[(source, target)] = (axis, dir, offset)

# Parse the scanners/beacons file
with open('day19_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

scan = {}
for line in lines:
	if 'scanner' in line:
		scanner_num = int(line.replace('--- scanner ', '').replace(' ---', ''))
		scan[scanner_num] = []
	elif ',' in line:
		(x, y, z) = [int(n) for n in line.split(',')]
		scan[scanner_num].append((x, y, z))

offset_dict = {}
for i in range(scanner_num + 1):
	for j in range(scanner_num + 1):
		if i != j:
			for a in remap_axes:
				for d in remap_dirs:
					s1_remap = [remap(coord, a, d) for coord in scan[j]]
					for s0 in scan[i]:
						for s1 in s1_remap:
							offset = (j, i, (a[0], a[1], a[2]), d, (s0[0] - s1[0], s0[1] - s1[1], s0[2] - s1[2]))
							offset_dict[offset] = offset_dict.get(offset, 0) + 1

remap_guide = {}
for offset in offset_dict:
	if offset_dict[offset] == 12:
		remap_guide[(offset[0], offset[1])] = (offset[2], offset[3], offset[4])

solved = {0: None}
unsolved = [i for i in range(1, scanner_num + 1)]
remap_guide[(0, 0)] = ((0, 1, 2), (1, 1, 1), (0, 0, 0))

while len(unsolved) > 0:
	for (source,target) in remap_guide:
		if source in unsolved and target in solved:
			if (source,0) in remap_guide:
				pass
			elif (target,0) in remap_guide:
				(axis, dirs, offset) = remap_guide[(source, target)]
				axis = {0: axis[0], 1: axis[1], 2: axis[2]}
				generate(source, target, 0)
				break
			solved[source] = None
			unsolved.remove(source)

beacon_set = set()
for i in range(scanner_num + 1):
	for beacon in scan[i]:
		beacon_set.add(remap2(beacon, i, 0))

print('Part One: there are {0} beacons in the full map.'.format(len(beacon_set)))

max_dist = 0
for i in range(scanner_num + 1):
	for j in range(scanner_num + 1):
		dist = manhattan_dist(remap_guide[(i, 0)][2], remap_guide[(j, 0)][2])
		if dist > max_dist: max_dist = dist
print('Part Two: the largest Manhattan distance between any two scanners is {0}.'.format(max_dist))