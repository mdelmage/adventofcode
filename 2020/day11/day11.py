#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The seat layout fits neatly on a grid.
# Each position is either floor (.), an empty seat (L), or an occupied seat (#).
FLOOR         = '.'
SEAT_EMPTY    = 'L'
SEAT_OCCUPIED = '#'

# All decisions are based on the number of occupied seats adjacent to a given seat
# (one of the eight positions immediately up, down, left, right, or diagonal from the seat).
NEIGHBORS = [( 0,  1),
             ( 0, -1),
             ( 1,  0),
             ( 1,  1),
             ( 1, -1),
             (-1,  0),
             (-1,  1),
             (-1, -1)]

def occupied_neighbors(x, y, line_of_sight=False):
    neighbor_count = 0
    for n in NEIGHBORS:
        nx = (x + n[0], y + n[1])

        # [Part Two]
        # People don't just care about adjacent seats - they care about the first seat
        # they can see in each of those eight directions!
        # 
        # Now, instead of considering just the eight immediately adjacent seats, consider
        # the first seat in each of those eight directions.
        while line_of_sight and nx in grid and grid[nx] == FLOOR:
            nx = (nx[0]+n[0],nx[1]+n[1])

        neighbor_count += (grid.get(nx, FLOOR) == SEAT_OCCUPIED)
    return neighbor_count

def update_grid(leave_seat_threshold, part_two=False):
    global grid

    updates = 0
    new_grid = {}
    for (x, y) in grid:
        # Otherwise, the seat's state does not change.
        # (set this default condition right away)
        new_grid[(x, y)] = grid[(x, y)]

        if grid[(x, y)] != FLOOR:
            # All decisions are based on the number of occupied seats adjacent to a given seat
            # (one of the eight positions immediately up, down, left, right, or diagonal from the seat).
            neighbor_count = occupied_neighbors(x, y, part_two)

            # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            if grid[(x, y)] == SEAT_EMPTY and neighbor_count == 0:
                new_grid[(x, y)] = SEAT_OCCUPIED
                updates += 1
            # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
            elif grid[(x, y)] == SEAT_OCCUPIED and neighbor_count >= leave_seat_threshold:
                new_grid[(x, y)] = SEAT_EMPTY
                updates += 1

    # Grid is updated all at once, based on our scan
    grid = new_grid
    return updates

grid = {}

# Parse the seat map and save each line
with open('day11_input.txt') as f:
    y = 0
    seatmap = [line.rstrip('\n') for line in f]
    for line in seatmap:
        for x in range(len(line)):
            grid[(x, y)] = line[x]
        y += 1

original_grid = grid

while update_grid(4) > 0:
    continue

occupied = [x for x in grid if grid[x] == SEAT_OCCUPIED]
print 'Part One: Steady state has {0} occupied seats.'.format(len(occupied))

# Recover the original grid
grid = original_grid

while update_grid(5, True) > 0:
    continue

occupied = [x for x in grid if grid[x] == SEAT_OCCUPIED]
print 'Part Two: Steady state has {0} occupied seats.'.format(len(occupied))