#!/usr/bin/env python
# -*- coding: utf-8 -*-

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_visible(g, loc):
    initial_loc = loc
    height = g[loc]

    # A tree is visible if all of the other trees between it and an edge of the grid are shorter than it.
    # Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.
    for d in DIRECTIONS:
        # Start at the initial location and move in one direction until
        # we hit either an edge or a tree of equal/higher height.
        loc = initial_loc

        while loc in g:
            loc = (loc[0] + d[0], loc[1] + d[1])
            if loc not in g:
                # We hit an edge and can still see the tree. Visible!
                return True

            if g[loc] >= height:
                # Oops, we ran into a tall tree. We can stop going this way now.
                break

    # Finished the whole search and never got to an edge. Tree is not visible.
    return False

def scenic_score(g, loc):
    initial_loc = loc
    height = g[loc]
    score = 1

    # To measure the viewing distance from a given tree, look up, down, left, and right from that tree;
    # stop if you reach an edge or at the first tree that is the same height or taller than the tree
    # under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)
    for d in DIRECTIONS:
        # Start at the initial location and move in one direction until
        # we hit either an edge or a tree of equal/higher height.
        loc = initial_loc
        trees_visible = 0

        while True:
            loc = (loc[0] + d[0], loc[1] + d[1])
            if loc not in g:
                # We hit an edge. We can stop going this way now.
                break

            # We're still on the map, so we can see this tree. Bump up the count.
            trees_visible += 1

            if g[loc] >= height:
                # Oops, we ran into a tall tree (and can see it), but can't go any further.
                break

        # A tree's scenic score is found by multiplying together its viewing distance
        # in each of the four directions.
        score *= trees_visible

    return score

# Parse the heightmap file
with open('day08_input.txt') as f:
    heightmap = [line.rstrip('\n') for line in f]
    grid_size = len(heightmap)

# Convert the plaintext heightmap into a hashable map
m = {}
for row in range(grid_size):
    for col in range(grid_size):
        m[(col, row)] = int(heightmap[row][col])

visible_trees = 0
best_scenic_score = 0
for row in range(grid_size):
    for col in range(grid_size):
        loc = (col, row)

        # Survey visible trees for Part One.
        if is_visible(m, loc): visible_trees += 1

        # Survey scenic scores for Part Two.
        best_scenic_score = max(best_scenic_score, scenic_score(m, loc))

print('Part One: {0} trees are visible from outside the grid.'.format(visible_trees))
print('Part Two: the highest scenic score is {0}.'.format(best_scenic_score))
