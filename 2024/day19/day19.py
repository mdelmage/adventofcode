#!/usr/bin/env python
# -*- coding: utf-8 -*-

def construct_towel(design):
    combos = [design]
    while len(combos) > 0:
        combos_next = []
        for c in combos:
            for p in patterns:
                if c == p:
                    return True
                if c[:len(p)] == p:
                    combos_next.append(c[len(p):])
        combos = combos_next
    return False

def duplicate_pattern(pattern):
    combos = [pattern]
    while len(combos) > 0:
        combos_next = []
        for c in combos:
            for p in [p for p in patterns if p != pattern]:
                if c == p:
                    return True
                if c[:len(p)] == p:
                    combos_next.append(c[len(p):])
        combos = combos_next
    return False


# Parse the input.
with open('day19_input.txt') as f:
    towels_and_designs = [line.rstrip('\n') for line in f]
    patterns = towels_and_designs[0].split(', ')
    designs = towels_and_designs[2:]

unique_patterns = []
for p in patterns:
    if not duplicate_pattern(p): unique_patterns.append(p)
patterns = unique_patterns

possible_designs = 0
for d in designs:
    if construct_towel(d): possible_designs += 1

# To get into the onsen as soon as possible, consult your list of towel patterns and desired designs carefully.
# How many designs are possible?
print('Part One: The number of possible designs is {0}.'.format(possible_designs))
