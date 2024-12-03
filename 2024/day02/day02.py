#!/usr/bin/env python
# -*- coding: utf-8 -*-

def is_safe(report):
    # Flip decreasing reports to increasing reports by inverting them.
    if report[1] < report[0]:
        report = [-1 * level for level in report]

    # The Red-Nosed reactor safety systems can only tolerate levels that are either
    # gradually increasing or gradually decreasing. So, a report only counts as safe
    # if both of the following are true:
    #
    # The levels are either all increasing or all decreasing.
    # Any two adjacent levels differ by at least one and at most three.
    for l in range(len(report) - 1):
        if report[l + 1] - report[l] not in [1, 2, 3]:
            return False

    return True

def is_safe_damped(report):
    # The Problem Dampener is a reactor-mounted module that lets the reactor
    # safety systems tolerate a single bad level in what would otherwise be a safe report.
    # It's like the bad level never happened!
    #
    # Now, the same rules apply as before, except if removing a single level from an unsafe report
    # would make it safe, the report instead counts as safe.
    for removed in range(len(report)):
        new_report = report[:removed] + report[removed + 1:]
        if is_safe(new_report): return True

    return False

# Parse the levels/reports list.
with open('day02_input.txt') as f:
    # The unusual data (your puzzle input) consists of many reports, one report per line.
    # Each report is a list of numbers called levels that are separated by spaces.
    reports = [[int(l) for l in line.rstrip('\n').split()] for line in f]

# Analyze the unusual data from the engineers. How many reports are safe?
safe_reports = sum([is_safe(report) for report in reports])
print('Part One: {0} reports are safe.'.format(safe_reports))

# Update your analysis by handling situations where the Problem Dampener
# can remove a single level from unsafe reports. How many reports are now safe?
safe_reports = sum([is_safe_damped(report) for report in reports])
print('Part Two: {0} reports are safe.'.format(safe_reports))