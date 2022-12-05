#!/usr/bin/env python
# -*- coding: utf-8 -*-

def fully_contained(range1, range2):
    # Returns True if range2 is a strict subset of range1
    return(range1[0] <= range2[0] and range1[1] >= range2[1])

def ranges_overlap(range1, range2):
    # Returns True if range1 and range2 overlap at all
    return(range1[1] >= range2[0] and range2[1] >= range1[0])

# Parse the section assignment pairings file
with open('day04_input.txt') as f:
    pairings = [line.rstrip('\n').split(',') for line in f]

# Some of the pairs have noticed that one of their assignments fully contains the other.
# For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6.
# In pairs where one assignment fully contains the other, one Elf in the pair would be
# exclusively cleaning sections their partner will already be cleaning, so these seem like
# the most in need of reconsideration.
overlaps = 0
for (elf1, elf2) in pairings:
    range1 = [int(i) for i in elf1.split('-')]
    range2 = [int(i) for i in elf2.split('-')]
    # In how many assignment pairs does one range fully contain the other?
    if fully_contained(range1, range2) or fully_contained(range2, range1):
        overlaps += 1

print('Part One: {0} assignment pairs have full overlaps.'.format(overlaps))

# It seems like there is still quite a bit of duplicate work planned.
# Instead, the Elves would like to know the number of pairs that overlap at all.
overlaps = 0
for (elf1, elf2) in pairings:
    range1 = [int(i) for i in elf1.split('-')]
    range2 = [int(i) for i in elf2.split('-')]
    # In how many assignment pairs do the ranges overlap?
    if ranges_overlap(range1, range2):
        overlaps += 1

print('Part Two: {0} assignment pairs have any kind of overlap.'.format(overlaps))
