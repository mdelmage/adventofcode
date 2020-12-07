#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

TARGET_BAG = 'shiny gold'

def can_contain(target_bag, source_bag):
    if target_bag == source_bag: return True
    if len(bag_rules[source_bag]) == 0: return False

    # Any success on inner bags is success for the whole bag
    for inner_bag in bag_rules[source_bag]:
        if can_contain(target_bag, inner_bag.color): return True

    return False

def count_bags(bag):
    # Count ourselves as the first bag
    count = 1

    # Count the size of each inner bag, and how many of them we need
    for inner_bag in bag_rules[bag]:
        count += (inner_bag.quantity * count_bags(inner_bag.color))

    return count

# Parse the luggage regulations declarations and save each line
with open('day07_input.txt') as f:
    regulations = [line.rstrip('\n') for line in f]

bag_rules = {}
for r in regulations:
    if 'no other bags' in r:
        bag_rules[r.split(' bags contain')[0]] = []
    else:
        # Ugly, but effective, tokenization
        processed_rule = (r + ' ').replace('contain ', '').replace(',', '').replace('.', '').replace(' bags ', ',').replace(' bag ', ',')[:-1].split(',')
        inner_bags = []
        for i in range(1, len(processed_rule)):
            inner_bag = namedtuple('inner_bag', 'quantity color')
            inner_bag.quantity = int(processed_rule[i][:processed_rule[i].find(' ')])
            inner_bag.color = processed_rule[i][processed_rule[i].find(' ') + 1:]
            inner_bags.append(inner_bag)
        bag_rules[processed_rule[0]] = inner_bags

contain_count = 0
for bag in (b for b in bag_rules if b != TARGET_BAG):
    contain_count += can_contain(TARGET_BAG, bag)

print 'Part One: {0} different bag colors can contain a {1} bag.'.format(contain_count, TARGET_BAG)
print 'Part Two: a single {0} bag must contain {1} other bags.'.format(TARGET_BAG, count_bags(TARGET_BAG) - 1)