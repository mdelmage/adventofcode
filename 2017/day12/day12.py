#!/usr/bin/env python
# -*- coding: utf-8 -*-

def consolidate():
    for i in range(len(groups)):
        # Check to see if any group overlaps with any *other* group.
        not_i = range(len(groups))
        not_i.remove(i)
        for j in not_i:
            if len(groups[i] & groups[j]) > 0:
                # Got one. Pull it out of the list and merge it with the other group.
                groups[j] |= groups[i]
                groups.pop(i)
                return True
    return False

groups = []

# Parse the list of pipe connections, and save each line
with open('day12_input.txt') as f:
    pipes = [line.rstrip('\n').replace(' <-> ', ', ').split(',') for line in f]

# Start with each list of connections as a separate set
for p in pipes:
    g = set([int(n) for n in p])
    groups.append(g)

# Now, do an ugly O(N^2) reduction to the base set of groups.
while consolidate(): continue

for g in groups:
    if 0 in g: print 'Part One: {0} programs in the group that contains ID 0.'.format(len(g))
print 'Part Two: {0} groups in total.'.format(len(groups))