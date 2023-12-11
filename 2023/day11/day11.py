#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The researcher has collected a bunch of data and compiled the data into a single
# giant image (your puzzle input). The image includes empty space (.) and galaxies (#).
TILE_EMPTY = '.'
TILE_GALAXY = '#'

# Expanding-galaxy-aware version of the Manhattan Distance.
# If there are expanding rows or columns between the points,
# add a (configurable) amount of distance to allow for expansion.
def expanding_galaxy_manhattan_dist(pos1, pos2, expansion):
    # Determine the range of rows and columns we're working with.
    min_col = min(pos1[0], pos2[0])
    max_col = max(pos1[0], pos2[0])
    min_row = min(pos1[1], pos2[1])
    max_row = max(pos1[1], pos2[1])

    # Now find out how many rows and columns are expanding between the two galaxies.
    expansion_cols = len([c for c in blank_cols if c > min_col and c < max_col])
    expansion_rows = len([r for r in blank_rows if r > min_row and r < max_row])

    # Return the Manhattan Distance, plus the expansion values.
    # Note that the parameter is given in the post-expansion size, so we must subtract one
    # to account for the original row/column.
    return max_col - min_col + max_row - min_row + (expansion - 1) * (expansion_rows + expansion_cols)

# Parse the giant image.
with open('day11_input.txt') as f:
    image = [line.rstrip('\n') for line in f]

size = len(image)

# Due to something involving gravitational effects, only some space expands.
# In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.
blank_rows = []
blank_cols = []
for i in range(size):
    blank_row = True
    blank_col = True
    for j in range(size):
        if image[i][j] != TILE_EMPTY: blank_row = False
        if image[j][i] != TILE_EMPTY: blank_col = False
    if blank_row: blank_rows.append(i)
    if blank_col: blank_cols.append(i)

# The researcher is trying to figure out the sum of the lengths of the shortest path between
# every pair of galaxies. However, there's a catch: the universe expanded in the time it took
# the light from those galaxies to reach the observatory.
galaxies = []
for row in range(len(image)):
    for col in range(len(image[0])):
        if image[row][col] == TILE_GALAXY: galaxies.append((col, row))

# Equipped with this expanded universe, the shortest path between every pair of galaxies can be found.
# Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path
# between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time.
# (The shortest path between two galaxies is allowed to pass through another galaxy.)
galaxy_dist_expansion_part_one = 0
galaxy_dist_expansion_part_two = 0
for g in set([frozenset((x, y)) for x in galaxies for y in galaxies if x != y]):
    g = set(g)
    g1 = g.pop()
    g2 = g.pop()
    galaxy_dist_expansion_part_one += expanding_galaxy_manhattan_dist(g1, g2, 2)

    # The galaxies are much older (and thus much farther apart) than the researcher initially estimated.
    #
    # Now, instead of the expansion you did before, make each empty row or column one million times larger.
    # That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be
    # replaced with 1000000 empty columns.
    galaxy_dist_expansion_part_two += expanding_galaxy_manhattan_dist(g1, g2, 1000000)

# Expand the universe, then find the length of the shortest path between every pair of galaxies.
# What is the sum of these lengths?
print('Part One: Sum of galaxy pair distances with expansion=2 is {0}.'.format(galaxy_dist_expansion_part_one))

# Starting with the same initial image, expand the universe according to these new rules,
# then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
print('Part Two: Sum of galaxy pair distances with expansion=1000000 is {0}.'.format(galaxy_dist_expansion_part_two))