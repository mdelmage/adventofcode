#!/usr/bin/python
# coding: utf-8

GRID_SIZE = 5

TILE_BUG       = '#'
TILE_EMPTY     = '.'
TILE_RECURSION = '?'

levels = [0]
grid = {}

SPECIAL_TILES = { (1, 2): [(1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 0, 3), (1, 0, 4)],
                  (3, 2): [(1, 4, 0), (1, 4, 1), (1, 4, 2), (1, 4, 3), (1, 4, 4)],
                  (2, 1): [(1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0)],
                  (2, 3): [(1, 0, 4), (1, 1, 4), (1, 2, 4), (1, 3, 4), (1, 4, 4)],

                  (0, 0): [(-1, 1, 2), (-1, 2, 1)],
                  (0, 4): [(-1, 1, 2), (-1, 2, 3)],
                  (4, 0): [(-1, 2, 1), (-1, 3, 2)],
                  (4, 4): [(-1, 3, 2), (-1, 2, 3)],

                  (0, 1): [(-1, 1, 2)],
                  (0, 2): [(-1, 1, 2)],
                  (0, 3): [(-1, 1, 2)],

                  (4, 1): [(-1, 3, 2)],
                  (4, 2): [(-1, 3, 2)],
                  (4, 3): [(-1, 3, 2)],

                  (1, 0): [(-1, 2, 1)],
                  (2, 0): [(-1, 2, 1)],
                  (3, 0): [(-1, 2, 1)],

                  (1, 4): [(-1, 2, 3)],
                  (2, 4): [(-1, 2, 3)],
                  (3, 4): [(-1, 2, 3)]}

C = (GRID_SIZE / 2)

def print_grids():
    for level in sorted(levels):
        print "Level {0}".format(level)
        for y in range(GRID_SIZE):
            grid_str = ""
            for x in range(GRID_SIZE):
                grid_str += grid[(level, x, y)]
            print grid_str
        print ""

def neighbors(level, x, y):
    score = 0
    potential_neighbors = [(level, x - 1, y), (level, x + 1, y), (level, x, y - 1), (level, x, y + 1)]

    if (x, y) in SPECIAL_TILES:
        for s in SPECIAL_TILES[(x, y)]:
            potential_neighbors += [(level + s[0], s[1], s[2])]

    for n in potential_neighbors:
        if n not in grid: continue
        if TILE_BUG == grid[n]:
            score += 1
    return score

def iterate():
    global grid
    next_gen_grid = {}
    for level in sorted(levels + [sorted(levels)[0] - 1] + [sorted(levels)[len(levels) - 1] + 1]):
        if (level, 0, 0) not in grid:
            levels.append(level)
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    grid[(level, x, y)] = TILE_EMPTY
                    next_gen_grid[(level, x, y)] = TILE_EMPTY

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if (C, C) == (x, y):
                    next_gen_grid[(level, x, y)] = TILE_RECURSION
                    continue
                neighbor_count = neighbors(level, x, y)
                if TILE_BUG == grid[(level, x, y)] and 1 != neighbor_count:
                    next_gen_grid[(level, x, y)] = TILE_EMPTY
                elif TILE_EMPTY == grid[(level, x, y)] and neighbor_count in [1, 2]:
                    next_gen_grid[(level, x, y)] = TILE_BUG
                else:
                    next_gen_grid[(level, x, y)] = grid[(level, x, y)]
    grid = next_gen_grid
                
# Open input file
with open("day24.txt", "r") as f:
    y = 0
    for line in f:
        for x in range(GRID_SIZE):
            grid[(0, x, y)] = line[x]
        y += 1

    print_grids()

    for i in range(200):
        iterate()
    print_grids()

    population = 0
    for cell in grid:
        if TILE_BUG == grid[cell]: population += 1
    print "Total population after {0} generations: {1}".format(i + 1, population)