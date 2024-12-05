#!/usr/bin/env python
# -*- coding: utf-8 -*-

def rule_violation(update):
    prev_pages = set()
    for page in update:
        # Safety protocols clearly indicate that new pages for the safety manuals must be printed
        # in a very specific order. The notation X|Y means that if both page number X and page number Y
        # are to be produced as part of an update, page number X must be printed at some point before page number Y.
        for (before, after) in rules:
            if page == before and after in prev_pages: return (before, after)
        prev_pages.add(page)

    # This update is in the correct order and complies with all rules.
    return None

# For a given update list and page numbers, return a list with those pages swapped.
def swap(update, page1, page2):
    return [page1 if page==page2 else page2 if page==page1 else page for page in update]

def fix_update(update):
    # While the Elves get to work printing the correctly-ordered updates,
    # you have a little time to fix the rest of them.
    #
    # For each of the incorrectly-ordered updates, use the page ordering rules
    # to put the page numbers in the right order.
    while True:
        try:
            # Find the first rule violation and swap those pages.
            # Re-run the check against all rules, because the swap may have caused
            # a rule that was already passing, to subsequently fail.
            (page1, page2) = rule_violation(update)
            update = swap(update, page1, page2)
        except:
            # No rules violations were found; we're done!
            return update

# Parse the safety manual page ordering rules and update pages.
with open('day05_input.txt') as f:
    safety_manual = [line.rstrip('\n') for line in f]
    divider = safety_manual.index('')
    rules = safety_manual[:divider]
    rules = ([[int(n) for n in rule.split('|')] for rule in rules])
    updates = safety_manual[divider + 1:]
    updates = ([[int(n) for n in update.split(',')] for update in updates])

sum_correct_middle_pages = 0
sum_incorrect_middle_pages = 0
for update in updates:
    if rule_violation(update):
        # Find the updates which are not in the correct order.
        # What do you get if you add up the middle page numbers after correctly ordering just those updates?
        update = fix_update(update)
        sum_incorrect_middle_pages += update[len(update) // 2]
    else:
        # Determine which updates are already in the correct order.
        # What do you get if you add up the middle page number from those correctly-ordered updates?
        sum_correct_middle_pages += update[len(update) // 2]

print('Part One: Sum of middle pages of correctly-ordered updates is {0}.'.format(sum_correct_middle_pages))
print('Part Two: Sum of middle pages of incorrectly-ordered updates is {0}.'.format(sum_incorrect_middle_pages))