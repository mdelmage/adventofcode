#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the customs declarations and save each line
with open('day06_input.txt') as f:
    customs = [line.rstrip('\n') for line in f]

# Pad our file with a blank line so that we get the last group processed.
customs += ['']

answer_set = set()
answer_dict = dict()
cohort_size = 0

answer_sum = 0
cohort_sum = 0

for line in customs:
    if len(line) == 0:
        # For each group, count the number of questions to which anyone answered "yes".
        answer_sum += len(answer_set)

        # As you finish the last group's customs declaration, you notice that you misread
        # one word in the instructions:
        #
        # You don't need to identify the questions to which anyone answered "yes"; you need
        # to identify the questions to which everyone answered "yes"!
        for c in answer_dict:
            if answer_dict[c] == cohort_size: cohort_sum += 1

        answer_set = set()
        answer_dict = dict()
        cohort_size = 0
    else:
        cohort_size += 1
        for c in line:
            # Populate the set and dict with answers
            answer_set.add(c)
            answer_dict[c] = answer_dict.get(c, 0) + 1

print 'Part One: sum of group answers is {0}.'.format(answer_sum)
print 'Part Two: sum of cohort agreement is {0}.'.format(cohort_sum)