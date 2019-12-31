#!/usr/bin/python
# coding: utf-8

GRID_SIZE = 5

TILE_BUG   = '#'
TILE_EMPTY = '.'

grid = {}
history = set()

def print_grid():
    for y in range(GRID_SIZE):
        grid_str = ""
        for x in range(GRID_SIZE):
            grid_str += grid[(x, y)]
        print grid_str
    print ""

def biodiversity_score():
    score = 0
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if TILE_BUG == grid[(x, y)]: score += pow(2, (y * GRID_SIZE) + x)
    return score

def neighbors(x, y):
    score = 0
    for n in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + n[0], y + n[1])
            if neighbor not in grid: continue
            if TILE_BUG == grid[neighbor]:
                score += 1
    return score

def iterate():
    global grid
    next_gen_grid = {}
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            neighbor_count = neighbors(x, y)
            if TILE_BUG == grid[(x, y)] and 1 != neighbor_count:
                next_gen_grid[(x, y)] = TILE_EMPTY
            elif TILE_EMPTY == grid[(x, y)] and neighbor_count in [1, 2]:
                next_gen_grid[(x, y)] = TILE_BUG
            else:
                next_gen_grid[(x, y)] = grid[(x, y)]
    grid = next_gen_grid
                

# Open input file
with open("day24.txt", "r") as f:
    y = 0
    for line in f:
        for x in range(GRID_SIZE):
            grid[(x, y)] = line[x]
        y += 1

    history.add(biodiversity_score())
    print_grid()

    gen = 0
    while True:
        iterate()
        biodiversity = biodiversity_score()
        if biodiversity in history:
            print "Duplicate biodiversity rating in Generation {0}: {1}".format(gen, biodiversity)
            print_grid()
            break
        history.add(biodiversity)
        gen += 1
