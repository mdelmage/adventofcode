#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the rucksack inventories file
with open('day03_input.txt') as f:
    rucksacks = [line.rstrip('\n') for line in f]


# To help prioritize item rearrangement, every item type can be converted to a priority:
#
# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.
def priority(item):
    if item.islower():
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27


priorities = 0
for r in rucksacks:
    # A given rucksack always has the same number of items in each of its two compartments,
    # so the first half of the characters represent items in the first compartment,
    # while the second half of the characters represent items in the second compartment.
    halfway = int(len(r) / 2)
    compartment_one = set([*r[:halfway]])
    compartment_two = set([*r[halfway:]])

    # Find the item type that appears in both compartments of each rucksack.
    # What is the sum of the priorities of those item types?
    priorities += priority((compartment_one & compartment_two).pop())

print('Part One: sum of priorities is {0}.'.format(priorities))

# For safety, the Elves are divided into groups of three. Every Elf carries a badge
# that identifies their group.
priorities = 0
for group in range(int(len(rucksacks) / 3)):
    elf1 = set([*rucksacks[3 * group]])
    elf2 = set([*rucksacks[3 * group + 1]])
    elf3 = set([*rucksacks[3 * group + 2]])

    # For efficiency, within each group of three Elves, the badge is the only item type
    # carried by all three Elves.
    #
    # Additionally, nobody wrote down which item type corresponds to each group's badges.
    # The only way to tell which item type is the right one is by finding the one item type
    # that is common between all three Elves in each group.
    badge = elf1 & elf2 & elf3

    # Find the item type that corresponds to the badges of each three-Elf group.
    # What is the sum of the priorities of those item types?
    priorities += priority(badge.pop())

print('Part Two: sum of priorities is {0}.'.format(priorities))
