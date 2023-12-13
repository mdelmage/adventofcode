#!/usr/bin/env python
# -*- coding: utf-8 -*-

UNKNOWN     = '?'
OPERATIONAL = '.'
DAMAGED     = '#'

# Parse the spring damage record.
with open('day12_input.txt') as f:
    damage = [line.rstrip('\n') for line in f]

matches = 0
for springs, groups in [d.split() for d in damage]:
    unknowns = len([c for c in springs if c == UNKNOWN])
    groups = [int(n) for n in groups.split(',')]
    for n in range(2 ** unknowns):
        s = springs
        replacements = ('0' * unknowns + bin(n)[2:])[-unknowns:].replace('1', OPERATIONAL).replace('0', DAMAGED)
        for r in range(unknowns):
            ch = s.find(UNKNOWN)
            s = s[:ch] + replacements[r] + s[ch + 1:]

        # Count the continuous groups of damaged springs
        damaged = []
        while len(s) > 0:
            while len(s) > 0 and s[0] == OPERATIONAL: s = s[1:]
            d = 0
            while len(s) > 0 and s[0] == DAMAGED:
                s = s[1:]
                d += 1
            if d > 0: damaged.append(d)

        if damaged == groups: matches += 1

# For each row, count all of the different arrangements of operational and broken springs
# that meet the given criteria. What is the sum of those counts?
print('Part One: Sum of possible spring arrangements is {0}.'.format(matches))