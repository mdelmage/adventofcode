#!/usr/bin/env python
# -*- coding: utf-8 -*-

def valid_update(update):
    prev_pages = set()
    for page in update:
        for (comes_before, comes_after) in rules:
            if page == comes_before and comes_after in prev_pages: return False
        prev_pages.add(page)

    return True

# Parse the safety manual page ordering rules and update pages.
with open('day05_input.txt') as f:
    safety_manual = [line.rstrip('\n') for line in f]
    divider = safety_manual.index('')
    rules = safety_manual[:divider]
    rules = ([[int(n) for n in rule.split('|')] for rule in rules])
    updates = safety_manual[divider + 1:]
    updates = ([[int(n) for n in update.split(',')] for update in updates])

# Determine which updates are already in the correct order.
# What do you get if you add up the middle page number from those correctly-ordered updates?
sum_middle_pages = 0
for update in updates:
    if valid_update(update): sum_middle_pages += update[len(update) // 2]

print('Part One: Sum of middle pages of correctly-ordered updates is {0}.'.format(sum_middle_pages))