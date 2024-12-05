#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This word search allows words to be horizontal, vertical, diagonal,
# written backwards, or even overlapping other words.
SEARCHES = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

BLANK_CHARACTER = '.'

def search_ahead(row, col, method):
    i = method[0]
    j = method[1]
    search = word_search.get((col + i*0, row + j*0), BLANK_CHARACTER) \
           + word_search.get((col + i*1, row + j*1), BLANK_CHARACTER) \
           + word_search.get((col + i*2, row + j*2), BLANK_CHARACTER) \
           + word_search.get((col + i*3, row + j*3), BLANK_CHARACTER)

    # She only has to find one word: XMAS.
    return search == 'XMAS'

def search_diagonals(row, col):
    if word_search[(col, row)] != 'A':
        return False

    # Find out if we have diagonal(s) that say 'MAS' in either direction.
    sw_ne = set()
    nw_se = set()
    sw_ne.add(word_search.get((col - 1, row + 1), BLANK_CHARACTER))
    sw_ne.add(word_search.get((col + 1, row - 1), BLANK_CHARACTER))
    nw_se.add(word_search.get((col + 1, row + 1), BLANK_CHARACTER))
    nw_se.add(word_search.get((col - 1, row - 1), BLANK_CHARACTER))

    # If both diagonals say 'MAS', we have a match.
    return (sw_ne == set({'S', 'M'}) and nw_se == set({'S', 'M'}))

# Parse the word search.
with open('day04_input.txt') as f:
    w = [line.rstrip('\n') for line in f]

    # Convert the list to a dict for easier processing.
    word_search = {}
    for row in range(len(w)):
        for col in range(len(w[0])):
            word_search[(col, row)] = w[row][col]

# Take a look at the little Elf's word search. How many times does XMAS appear?
matches = 0
for row in range(len(w)):
    for col in range(len(w[0])):
        for method in SEARCHES:
            if search_ahead(row, col, method): matches += 1

print('Part One: XMAS appears {0} times in the word search.'.format(matches))

# The Elf looks quizzically at you. Did you misunderstand the assignment?
#
# Looking for the instructions, you flip over the word search to find that
# this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're
# supposed to find two MAS in the shape of an X.
#
# Flip the word search from the instructions back over to the word search side
# and try again. How many times does an X-MAS appear?
matches = 0
for row in range(len(w)):
    for col in range(len(w[0])):
        if search_diagonals(row, col): matches += 1

print('Part Two: XMAS appears {0} times in the word search.'.format(matches))