#!/usr/bin/env python
# -*- coding: utf-8 -*-

def construct_towel(design):
    global lookup

    if design in lookup:
        return lookup[design]

    valid_counts = 0
    next_level = set()
    for p in perm_counts:
        if p == design:
            valid_counts += 1
        elif design[:len(p)] == p:
            next_level.add(design[len(p):])

    for subdesign in next_level:
        valid_counts += construct_towel(subdesign)

    if design not in lookup: lookup[design] = valid_counts
    return valid_counts

def naive_permutations(towel):
    perm_count = 0
    perms = [towel]
    while len(perms) > 0:
        perms_next = []
        for perm in perms:
            for pat in [p for p in patterns if p != towel]:
                if perm == pat:
                    perm_count += 1
                elif perm[:len(pat)] == pat:
                    perms_next.append(perm[len(pat):])
        perms = perms_next
    return max(1, perm_count)


# Parse the input.
with open('day19_input.txt') as f:
    towels_and_designs = [line.rstrip('\n') for line in f]
    patterns = towels_and_designs[0].split(', ')
    designs = towels_and_designs[2:]


perm_counts = {}
for p in patterns:
    perm_counts[p] = naive_permutations(p)

lookup = {}
possible_designs = 0
possible_permutations = 0
for d in designs:
    permutations = construct_towel(d)
    if permutations > 0:
        possible_designs += 1
        possible_permutations += permutations

# To get into the onsen as soon as possible, consult your list of towel patterns and desired designs carefully.
# How many designs are possible?
print('Part One: The number of possible designs is {0}.'.format(possible_designs))

print('Part Two: The number of possible ways to make the towels is {0}.'.format(possible_permutations))
