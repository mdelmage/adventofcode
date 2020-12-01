#!/usr/bin/env python
# -*- coding: utf-8 -*-

TARGET_SUM = 2020

# ...the Elves in accounting just need you to fix your expense report
# (your puzzle input); apparently, something isn't quite adding up.
#
# Specifically, they need you to find the two entries that sum to 2020
# and then multiply those two numbers together.

def find_two_entries(l):
    # Part One naïve solution: brute-force the list with itself, O(N^2).
    for n1 in l:
        for n2 in l:
            if n1 + n2 == TARGET_SUM:
                print 'Part One:'
                print '{0} + {1} = {2}'.format(n1, n2, n1 + n2)
                print '{0} * {1} = {2}'.format(n1, n2, n1 * n2)
                print ''
                return

# The Elves in accounting are thankful for your help; one of them even
# offers you a starfish coin they had left over from a past vacation.
# They offer you a second one if you can find three numbers in your
# expense report that meet the same criteria.

def find_three_entries(l):
    # Part Two naïve solution: brute-force the list with itself twice, O(N^3).
    for n1 in l:
        for n2 in l:
            for n3 in l:
                if n1 + n2 + n3 == TARGET_SUM:
                    print 'Part Two:'
                    print '{0} + {1} + {2} = {3}'.format(n1, n2, n3, n1 + n2 + n3)
                    print '{0} * {1} * {2} = {3}'.format(n1, n2, n3, n1 * n2 * n3)
                    print ''
                    return


# Parse the expense report and save each line as an integer
with open('day01_input.txt') as f:
    expense_report = [int(line.rstrip('\n')) for line in f]

find_two_entries(expense_report)
find_three_entries(expense_report)