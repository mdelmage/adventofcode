#!/usr/bin/env python
# -*- coding: utf-8 -*-

# You note down the patterns of ash (.) and rocks (#) that you see as you walk
# (your puzzle input); perhaps by carefully analyzing these patterns, you can
# figure out where the mirrors are!
ASH = '.'
ROCKS = '#'

# Transpose a column to a row.
# Return a string representing the nth column, read from top to bottom.
def to_col(p, n):
    t = ''
    for row in range(len(p)):
        t += p[row][n]
    return t

# Return the set of all row numbers where there are horizontal reflections.
# Use 1-indexed (aka "plain English") row numbers.
def horizontal_reflections(p):
    reflections = set()
    rows = len(p)
    for r in range(rows - 1):
        low = r
        high = r + 1
        match = True

        # Run all the way to the nearest edge, and bail out if we don't match.
        while match and low >= 0 and high < rows:
            if p[low] != p[high]: match = False
            low -= 1
            high += 1

        # Got all the way to an edge! We have a reflection.
        if match: reflections.add(r + 1)
    return reflections

# Return the set of all column numbers where there are vertical reflections.
# Use 1-indexed (aka "plain English") column numbers.
def vertical_reflections(p):
    reflections = set()
    cols = len(p[0])
    for c in range(cols - 1):
        low = c
        high = c + 1
        match = True

        # Run all the way to the nearest edge, and bail out if we don't match.
        while match and low >= 0 and high < cols:
            if to_col(p, low) != to_col(p, high): match = False
            low -= 1
            high += 1

        # Got all the way to an edge! We have a reflection.
        if match: reflections.add(c + 1)
    return reflections

def summary(p):
    # To summarize your pattern notes, add up the number of columns to the left of each
    # vertical line of reflection; to that, also add 100 multiplied by the number of rows
    # above each horizontal line of reflection.
    s = vertical_reflections(p)
    s |= set([100 * n for n in horizontal_reflections(p)])
    return s

# Parse the ash and rock patterns.
with open('day13_input.txt') as f:
    patterns = [line.rstrip('\n') for line in f]

    # Split each pattern by empty lines.
    g = [[]]
    for p in patterns:
        if len(p) > 0:
            g[-1].append(p)
        else:
            g.append([])
    patterns = g

# Find the line of reflection in each of the patterns in your notes.
# What number do you get after summarizing all of your notes?
score = sum([summary(p).pop() for p in patterns])
print('Part One: Summary of all patterns is {0}.'.format(score))

score = 0
for p in patterns:
    original_score = summary(p).pop()
    new_score = original_score

    # Go through every "pixel" in the pattern.
    # This comprehension makes it easier to break out of than the traditional nested-for loop.
    for (row, col) in [(row, col) for row in range(len(p)) for col in range(len(p[0]))]:

        # Swap out the current item to see if it's a smudge.
        # Remember it so we can swap it back afterwards.
        old_ch = p[row][col]
        if old_ch == ROCKS:
            new_ch = ASH
        else:
            new_ch = ROCKS
        p[row] = p[row][:col] + new_ch + p[row][col + 1:]

        # Get a summary of this new, modified pattern.
        # It could have a few different outcomes:
        #
        # 1. A new reflection and the existing reflection;
        # 2. A new reflection only;
        # 3. The existing reflection only;
        # 4. No reflections.
        s = summary(p)
        if len(s) == 2:
            # Two reflections! One is guaranteed to be the new one.
            # Find out which it is by subtracting the old one from the set.
            # Then save that score.
            new_score = (s - set([original_score])).pop()
        elif len(s) == 1:
            # One reflection! Could be the original, or a new one.
            # Save the score for later.
            new_score = s.pop()

        if new_score == original_score:
            # No new score, so no new reflection. Swap back!
            p[row] = p[row][:col] + old_ch + p[row][col + 1:]
        else:
            # Different score; we've found the new reflection! Bail out.
            score += new_score
            break

# In each pattern, fix the smudge and find the different line of reflection.
# What number do you get after summarizing the new reflection line in each pattern in your notes?
print('Part Two: Summary of all new reflections is {0}.'.format(score))