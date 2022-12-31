#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The scan shows Elves # and empty ground .;
# outside your scan, more empty ground extends a long way in every direction.
ELF = '#'

# The scan is oriented so that north is up; orthogonal directions are written N (north),
# S (south), W (west), and E (east), while diagonal directions are written NE, NW, SE, SW.
NORTH = ( 0, -1)
SOUTH = ( 0,  1)
WEST  = (-1,  0)
EAST  = ( 1,  0)

NORTHWEST = (-1, -1)
NORTHEAST = ( 1, -1)
SOUTHWEST = (-1,  1)
SOUTHEAST = ( 1,  1)

ALL = [NORTH, SOUTH, WEST, EAST, NORTHWEST, NORTHEAST, SOUTHWEST, SOUTHEAST]

# Otherwise, the Elf looks in each of four directions in the following order
# and proposes moving one step in the first valid direction:
#
# If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
# If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
# If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
# If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
proposals = [(NORTH, [NORTH, NORTHEAST, NORTHWEST]),
             (SOUTH, [SOUTH, SOUTHEAST, SOUTHWEST]),
             (WEST,  [WEST, NORTHWEST, SOUTHWEST]),
             (EAST,  [EAST, NORTHEAST, SOUTHEAST])]

def count_empty_tiles(e):
    empty_tiles = 0

    # Determine the bounding box for the Elves.
    # Use reasonably large initial values as dummies.
    x_min = 100000000
    x_max = -100000000
    y_min = 100000000
    y_max = -100000000

    for pos in e:
        x_min = min(x_min, pos[0])
        x_max = max(x_max, pos[0])
        y_min = min(y_min, pos[1])
        y_max = max(y_max, pos[1])

    # Now scour the bounding box for empty tiles. Count them.
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            if (x, y) not in e:
                empty_tiles += 1

    return empty_tiles

def neighbor_count(elves, elf, neighbor_list):
    neighbor_count = 0
    for n in neighbor_list:
        if (elf[0] + n[0], elf[1] + n[1]) in elves:
            neighbor_count += 1
    return neighbor_count

# Parse the grove scan file
with open('day23_input.txt') as f:
    grove = [line.rstrip('\n')for line in f]

elves = {}
for y in range(len(grove)):
    for x in range(len(grove[y])):
        if grove[y][x] == ELF:
            elves[(x, y)] = 1

round = 0
while True:
    round += 1
    proposed_elves = {}

    # During the first half of each round, each Elf considers the eight positions adjacent
    # to themself. If no other Elves are in one of those eight positions, the Elf does not
    # do anything during this round. Otherwise, the Elf looks in each of four directions
    # in the following order and proposes moving one step in the first valid direction...
    for elf in elves:
        if neighbor_count(elves, elf, ALL) == 0:
            pass
        else:
            for direction, neighbors in proposals:
                if neighbor_count(elves, elf, neighbors) == 0:
                    elf = (elf[0] + direction[0], elf[1] + direction[1])
                    break

        # Add our proposal, which might be "do not move".
        proposed_elves[elf] = proposed_elves.get(elf, 0) + 1

    # After each Elf has had a chance to propose a move, the second half of the round can begin.
    # Simultaneously, each Elf moves to their proposed destination tile if they were the only
    # Elf to propose moving to that position. If two or more Elves propose moving to the same
    # position, none of those Elves move.
    next_elves = {}
    for elf in elves:
        next_elf = elf
        if neighbor_count(elves, elf, ALL) == 0:
            pass
        else:
            for direction, neighbors in proposals:
                if neighbor_count(elves, elf, neighbors) == 0:
                    next_elf = (elf[0] + direction[0], elf[1] + direction[1])
                    break

        if proposed_elves[next_elf] == 1:
            # No collision; execute the proposal!
            next_elves[next_elf] = 1
        else:
            # Collision; remain in place!
            next_elves[elf] = 1

    if round == 10:
        # Simulate the Elves' process and find the smallest rectangle that contains the Elves
        # after 10 rounds. How many empty ground tiles does that rectangle contain?
        print('Part One: empty ground tiles in the bounding box is {0}.'.format(count_empty_tiles(elves)))
    elif elves == next_elves:
        # It seems you're on the right track. Finish simulating the process and
        # figure out where the Elves need to go. How many rounds did you save them?
        #
        # Figure out where the Elves need to go. What is the number of the first round where no Elf moves?
        print('Part Two: first round where no Elf moved was {0}.'.format(round))
        break

    elves = next_elves

    # Finally, at the end of the round, the first direction the Elves considered
    # is moved to the end of the list of directions.
    proposals.append(proposals.pop(0))
