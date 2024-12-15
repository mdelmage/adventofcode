#!/usr/bin/env python
# -*- coding: utf-8 -*-

# As the robot (@) attempts to move, if there are any boxes (O) in the way,
# the robot will also attempt to push those boxes. However, if this action would cause the robot
# or a box to move into a wall (#), nothing moves instead, including the robot.
ROBOT = '@'
BOX   = 'O'
WALL  = '#'
SPACE = '.'

# The rest of the document describes the moves (^ for up, v for down, < for left, > for right)
# that the robot will attempt to make, in order.
UP    = '^'
DOWN  = 'v'
LEFT  = '<'
RIGHT = '>'

# To get the wider warehouse's map, start with your original map and, for each tile,
# make the following changes:
#
# If the tile is #, the new map contains ## instead.
# If the tile is O, the new map contains [] instead.
# If the tile is ., the new map contains .. instead.
# If the tile is @, the new map contains @. instead.
BOX_LEFT  = '['
BOX_RIGHT = ']'

FIRST_CHAR = {
    WALL: WALL,
    BOX: BOX_LEFT,
    SPACE: SPACE,
    ROBOT: ROBOT
}

SECOND_CHAR = {
    WALL: WALL,
    BOX: BOX_RIGHT,
    SPACE: SPACE,
    ROBOT: SPACE
}

MOVE_TO_VEL = {
    UP    : ( 0, -1),
    DOWN  : ( 0,  1),
    LEFT  : (-1,  0),
    RIGHT : ( 1,  0)
}

def vertical_push_group(warehouse, pos, vel):
    push_group = {}
    row = pos[1]
    if warehouse[pos] == BOX_LEFT:
        push_group[row] = [pos[0], pos[0] + 1]
    elif warehouse[pos] == BOX_RIGHT:
        push_group[row] = [pos[0] - 1, pos[0]]

    while True:
        row += vel
        push_group[row] = set()
        for col in push_group[row - vel]:
            if warehouse[(col, row)] == WALL: return {}
            if warehouse[(col, row)] == BOX_LEFT:
                push_group[row] |= set([col, col + 1])
            elif warehouse[(col, row)] == BOX_RIGHT:
                push_group[row] |= set([col - 1, col])

        # This row was all empty spaces, no boxes or walls.
        # This represents a complete push group, except for
        # the empty row (which we'll delete).
        if len(push_group[row]) == 0:
            del push_group[row]
            return push_group

def move_robot(warehouse, pos, vel):
    move_success = False
    intended_pos = (pos[0] + vel[0], pos[1] + vel[1])

    if warehouse[intended_pos] == SPACE:
        # Direct move into an unoccupied space.
        move_success = True
    elif warehouse[intended_pos] == BOX:
        # Single-wide box (or a stack of boxes).
        push = intended_pos
        while(warehouse[push] == BOX):
            push = (push[0] + vel[0], push[1] + vel[1])

        if warehouse[push] != WALL:
            # We have room to push the box (or stack of boxes).
            # Just move the robot into the first box's space, and
            # move a box into the free space at the end.
            #
            # This works for single or multiple boxes.
            warehouse[push] = BOX
            move_success = True
    elif warehouse[intended_pos] in [BOX_LEFT, BOX_RIGHT]:
        # Double-wide box (or stack of boxes).
        if vel[1] == 0:
            # Push horizontally. Easier, because there's no 2D effects to worry about.
            push = intended_pos
            while(warehouse[push] in [BOX_LEFT, BOX_RIGHT]):
                push = (push[0] + vel[0], push[1] + vel[1])

            if warehouse[push] != WALL:
                # We have room to push the box (or stack of boxes).
                # Move each box half individually.
                col_start = push[0]
                col_end = intended_pos[0] + vel[0]
                for col in range(col_start, col_end - vel[0], -vel[0]):
                    warehouse[(col, pos[1])] = warehouse[(col - vel[0]), pos[1]]
                move_success = True
        else:
            # Push vertically. Harder, because there's potential 2D stacking effects.
            # Calculate the push group, which could span across multiple rows.
            p = vertical_push_group(warehouse, intended_pos, vel[1])
            if len(p) > 0:
                # We have room to push the box (or stack of boxes).
                rows = list(map(lambda x: x[0], p.items()))

                # Move the boxes, starting from the destination end first and working backwards
                # to the robot end. This way we don't overwrite boxes by pushing them forwards.
                if vel[1] < 0:
                    rows = sorted(rows)
                else:
                    rows = sorted(rows, reverse=True)
                for row in rows:
                    for col in p[row]:
                        warehouse[(col, row + vel[1])] = warehouse[(col, row)]
                        warehouse[(col, row)] = SPACE
                move_success = True

    if move_success:
        warehouse[pos] = SPACE
        warehouse[intended_pos] = ROBOT
        pos = intended_pos

    return warehouse, pos

def score(warehouse):
    # The lanternfish use their own custom Goods Positioning System (GPS for short) to track
    # the locations of the boxes.
    gps_score = 0
    for col, row in warehouse:
        if warehouse[(col, row)] in [BOX, BOX_LEFT]:
            # The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map
            # plus its distance from the left edge of the map. (This process does not stop at wall tiles;
            # measure all the way to the edges of the map.)
            gps_score += (100 * row) + col
    return gps_score

# Parse the map of the warehouse and list of movements.
with open('day15_input.txt') as f:
    i = [line.rstrip('\n') for line in f]
    divider = i.index('')
    warehouse_list = i[:divider]
    moves = i[divider+1:]
    warehouse_part_one = {}
    warehouse_part_two = {}
    for row in range(len(warehouse_list)):
        for col in range(len(warehouse_list[0])):
            warehouse_part_one[(col, row)] = warehouse_list[row][col]
            if warehouse_part_one[(col, row)] == ROBOT: pos_part_one = (col, row)

            warehouse_part_two[(2*col, row)] = FIRST_CHAR[warehouse_list[row][col]]
            warehouse_part_two[(2*col + 1, row)] = SECOND_CHAR[warehouse_list[row][col]]
            if warehouse_part_two[(2*col, row)] == ROBOT: pos_part_two = (2*col, row)

    # The moves form a single giant sequence; they are broken into multiple lines just to make copy-pasting easier.
    # Newlines within the move sequence should be ignored.)
    moves_str = ''
    for m in moves:
        moves_str += m
    moves = moves_str

for move in moves:
    vel = MOVE_TO_VEL[move]
    warehouse_part_one, pos_part_one = move_robot(warehouse_part_one, pos_part_one, vel)
    warehouse_part_two, pos_part_two = move_robot(warehouse_part_two, pos_part_two, vel)

# Predict the motion of the robot and boxes in the warehouse.
# After the robot is finished moving, what is the sum of all boxes' GPS coordinates?
print('Part One: The sum of all boxes\' GPS coordinates is {0}.'.format(score(warehouse_part_one)))

# Predict the motion of the robot and boxes in this new, scaled-up warehouse.
# What is the sum of all boxes' final GPS coordinates?
print('Part Two: The sum of all double-wide boxes\' GPS coordinates is {0}.'.format(score(warehouse_part_two)))