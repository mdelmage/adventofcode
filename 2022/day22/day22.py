#!/usr/bin/env python
# -*- coding: utf-8 -*-

TILE_NOTHING = ' '
TILE_SPACE   = '.'
TILE_WALL    = '#'

UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
FACING_RIGHT = 0
FACING_DOWN  = 1
FACING_LEFT  = 2
FACING_UP    = 3

# Implement the above with a wrappable list. It's ordered so that the next index
# is 90 degrees rightward, and the previous index is 90 degrees leftward.
DIRECTIONS = [RIGHT, DOWN, LEFT, UP]

# There are four kinds of transformations when going between faces.
# "Transpose" means swap X and Y.
# "Invert" means (cube_size - cube_pos) for cube_pos on that axis.
MAP_TRANSPOSE = 0
MAP_TRANSPOSE_AND_INVERT_BOTH = 1
MAP_INVERT_X = 2
MAP_INVERT_Y = 3

# By inspection: these are the face transformations for the Day 22 example input.
#
# Generally, if we are staying on a left/right or up/down line,
# the transform will be an inversion of one of the axes.
#
# If we are moving between left/right and up/down, we'll need to
# transpose (and possibly also invert both axes).
transforms = {}

# Stated pair-wise:
transforms[(1,    FACING_UP)] = (2,  FACING_DOWN, MAP_INVERT_X)
transforms[(2,    FACING_UP)] = (1,  FACING_DOWN, MAP_INVERT_X)

transforms[(1, FACING_RIGHT)] = (6,  FACING_LEFT, MAP_INVERT_Y)
transforms[(6, FACING_RIGHT)] = (1,  FACING_LEFT, MAP_INVERT_Y)

transforms[(2,  FACING_DOWN)] = (5,    FACING_UP, MAP_INVERT_X)
transforms[(5,  FACING_DOWN)] = (2,    FACING_UP, MAP_INVERT_X)

transforms[(1,  FACING_LEFT)] = (3,  FACING_DOWN, MAP_TRANSPOSE)
transforms[(3,    FACING_UP)] = (1, FACING_RIGHT, MAP_TRANSPOSE)

transforms[(2,  FACING_LEFT)] = (6,    FACING_UP, MAP_TRANSPOSE_AND_INVERT_BOTH)
transforms[(6,  FACING_DOWN)] = (2, FACING_RIGHT, MAP_TRANSPOSE_AND_INVERT_BOTH)

transforms[(5,  FACING_LEFT)] = (3,    FACING_UP, MAP_TRANSPOSE_AND_INVERT_BOTH)
transforms[(3,  FACING_DOWN)] = (5, FACING_RIGHT, MAP_TRANSPOSE_AND_INVERT_BOTH)

transforms[(6,    FACING_UP)] = (4,  FACING_LEFT, MAP_TRANSPOSE_AND_INVERT_BOTH)
transforms[(4, FACING_RIGHT)] = (6,  FACING_DOWN, MAP_TRANSPOSE_AND_INVERT_BOTH)

# By inspection: these are the face transformations for my Day 22 input.
# They will only work on inputs with the same exterior shape.
transforms = {}

# Stated pair-wise:
transforms[(3, FACING_RIGHT)] = (2,    FACING_UP, MAP_TRANSPOSE)
transforms[(2,  FACING_DOWN)] = (3,  FACING_LEFT, MAP_TRANSPOSE)

transforms[(6, FACING_RIGHT)] = (5,    FACING_UP, MAP_TRANSPOSE)
transforms[(5,  FACING_DOWN)] = (6,  FACING_LEFT, MAP_TRANSPOSE)

transforms[(3,  FACING_LEFT)] = (4,  FACING_DOWN, MAP_TRANSPOSE)
transforms[(4,    FACING_UP)] = (3, FACING_RIGHT, MAP_TRANSPOSE)

transforms[(6,  FACING_LEFT)] = (1,  FACING_DOWN, MAP_TRANSPOSE)
transforms[(1,    FACING_UP)] = (6, FACING_RIGHT, MAP_TRANSPOSE)

transforms[(1,  FACING_LEFT)] = (4, FACING_RIGHT, MAP_INVERT_Y)
transforms[(4,  FACING_LEFT)] = (1, FACING_RIGHT, MAP_INVERT_Y)

transforms[(2,    FACING_UP)] = (6,    FACING_UP, MAP_INVERT_Y)
transforms[(6,  FACING_DOWN)] = (2,  FACING_DOWN, MAP_INVERT_Y)

transforms[(2, FACING_RIGHT)] = (5,  FACING_LEFT, MAP_INVERT_Y)
transforms[(5, FACING_RIGHT)] = (2,  FACING_LEFT, MAP_INVERT_Y)


def password(cube_wrapping):
    # You begin the path in the leftmost open tile of the top row of tiles.
    pos = face_roots[1]
    i_pos = 0

    # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
    # Initially, you are facing to the right (from the perspective of how the map is drawn).
    facing = 0

    while i_pos < len(instructions):
        # A letter indicates whether to turn 90 degrees clockwise (R) or counterclockwise (L).
        # Turning happens in-place; it does not change your current tile.
        if instructions[i_pos] == 'L':
            # turn left
            facing = (facing - 1) % len(DIRECTIONS)
            i_pos += 1
        elif instructions[i_pos] == 'R':
            # turn right
            facing = (facing + 1) % len(DIRECTIONS)
            i_pos += 1
        else:
            # A number indicates the number of tiles to move in the direction you are facing.
            # If you run into a wall, you stop moving forward and continue with the next instruction.
            length = 0
            while i_pos < len(instructions) and not instructions[i_pos].isalpha():
                length = (10 * length) + int(instructions[i_pos])
                i_pos += 1
            for i in range(length):
                next_pos = (pos[0] + DIRECTIONS[facing][0], pos[1] + DIRECTIONS[facing][1])
                next_facing = facing
                if next_pos not in board:
                    if not cube_wrapping:
                        # Simple wrapping (Part 1) instead of cube wrapping.
                        # The dumb way to do this is to back up until we fall off the *other*
                        # edge of the board, then advance one tile to get back on.
                        next_pos = pos
                        while next_pos in board:
                            next_pos = (next_pos[0] - DIRECTIONS[facing][0], next_pos[1] - DIRECTIONS[facing][1])
                        next_pos = (next_pos[0] + DIRECTIONS[facing][0], next_pos[1] + DIRECTIONS[facing][1])
                    else:
                        # Cube wrapping (Part 2).
                        # We need to figure out what our new global position and facing is.
                        # Break this up into a few transforms:

                        # 1. Figure out the new face and facing, from the transforms lookup.
                        face_num = faces[pos]
                        face_root = face_roots[face_num]
                        (next_face, next_facing, transform) = transforms[(face_num, facing)]

                        # 2. Figure out the local position on the new face.
                        face_pos = (pos[0] - face_root[0], pos[1] - face_root[1])
                        if transform == MAP_TRANSPOSE:
                            face_pos = (face_pos[1], face_pos[0])
                        elif transform == MAP_INVERT_X:
                            face_pos = (cube_size - 1 - face_pos[0], face_pos[1])
                        elif transform == MAP_INVERT_Y:
                            face_pos = (face_pos[0], cube_size - 1 - face_pos[1])
                        elif transform == MAP_TRANSPOSE_AND_INVERT_BOTH:
                            face_pos = (cube_size - 1 - face_pos[1], cube_size - 1 - face_pos[0])

                        # 3. Figure out the global position, based on where the face is located.
                        next_pos = (face_pos[0] + face_roots[next_face][0], face_pos[1] + face_roots[next_face][1])

                if board[next_pos] == TILE_SPACE:
                    # The way is clear; advance!
                    pos = next_pos
                    facing = next_facing
                elif board[next_pos] == TILE_WALL:
                    # Hit a wall; stop!
                    break

    # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
    return (1000 * (pos[1] + 1)) + (4 * (pos[0] + 1)) + facing

# Parse the board map file
with open('day22_input.txt') as f:
    board_map = [line.rstrip('\n')for line in f]

board = {}
max_col = 0
max_row = len(board_map)

# The first half of the monkeys' notes is a map of the board.
# It is comprised of a set of open tiles (on which you can move,
# drawn .) and solid walls (tiles which you cannot enter, drawn #).
for row in range(len(board_map) - 1):
    for col in range(len(board_map[row])):
        tile = board_map[row][col]
        if tile != TILE_NOTHING:
            board[(col, row)] = tile
            max_col = max(max_col, col)

# The second half is a description of the path you must follow.
# It consists of alternating numbers and letters.
instructions = board_map[len(board_map) - 1]

# Determine the size of the cube's edges.
# We could do this with math.sqrt, but let's be dumb
# (and avoid importing math).
cube_size = 1
while cube_size * cube_size * 6 != len(board):
    cube_size += 1

# Find, and number, each cube face (1-indexed).
# We'll create two different lookups: the face number for a given position,
# and the location of the face root (upper left position) for a given face number.
faces_found = 0
faces = {}
face_roots = {}
for y in range(((max_row) + 1) // cube_size):
    for x in range((max_col + 1) // cube_size):
        if (x * cube_size, y * cube_size) in board:
            # Found a new face; mark the root.
            faces_found += 1
            face_root = (x * cube_size, y * cube_size)
            face_roots[faces_found] = face_root

            # Now map each position in the face.
            # There's probably a smarter way to do this, but having
            # a direct lookup makes the routing code easier to read.
            for row in range(cube_size):
                for col in range(cube_size):
                    pos = (x * cube_size + col, y * cube_size + row)
                    faces[pos] = faces_found

# Follow the path given in the monkeys' notes. What is the final password?
print('Part One: final password is {0}.'.format(password(cube_wrapping=False)))

# Fold the map into a cube, then follow the path given in the monkeys' notes.
# What is the final password?
print('Part Two: final password is {0}.'.format(password(cube_wrapping=True)))
