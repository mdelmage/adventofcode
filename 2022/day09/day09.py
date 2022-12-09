#!/usr/bin/env python
# -*- coding: utf-8 -*-

DIRECTIONS = {'U': ( 0, -1),
              'D': ( 0,  1),
              'L': (-1,  0),
              'R': ( 1,  0)}

# (diagonally adjacent and even overlapping both count as touching)
TOUCHING = [[0, 0], [0, 1], [1, 0], [1, 1]]

TWO_STEPS_AWAY = [[0, 2], [2, 0]]

def move(head, tail):
    separation = [abs(head[0] - tail[0]), abs(head[1] - tail[1])]
    if separation in TOUCHING:
        # Already touching; no need to do anything
        pass
    elif separation in TWO_STEPS_AWAY:
        # If the head is ever two steps directly up, down, left, or right from the tail,
        # the tail must also move one step in that direction so it remains close enough.
        tail = (int((head[0] + tail[0]) / 2), int((head[1] + tail[1])/2))
    else:
        # Otherwise, if the head and tail aren't touching and aren't in the same row
        # or column, the tail always moves one step diagonally to keep up.
        yank = (max(-1, min(1, head[0] - tail[0])), max(-1, min(1, head[1] - tail[1])))
        tail = (tail[0] + yank[0], tail[1] + yank[1])

    return tail

def track_rope_tail(moves, rope_len):
    rope = [(0, 0) for i in range(rope_len)]

    tail_history = set()

    for (direction, distance) in moves:
        d = DIRECTIONS[direction]
        for count in range(int(distance)):
            rope[0] = (rope[0][0] + d[0], rope[0][1] + d[1])

            for i in range(1, rope_len):
                rope[i] = move(rope[i - 1], rope[i])
                separation = [abs(rope[i - 1][0] - rope[i][0]), abs(rope[i - 1][1] - rope[i][1])]

            # After simulating the rope, you can count up all of the positions
            # the tail visited at least once.
            tail_history.add(rope[rope_len - 1])

    return len(tail_history)

# Parse the motions list file
with open('day09_input.txt') as f:
    moves = [line.rstrip('\n').split(' ') for line in f]

print('Part One: tail of the short rope visited {0} positions.'.format(track_rope_tail(moves, 2)))
print('Part Two: tail of the long rope visited {0} positions.'.format(track_rope_tail(moves, 10)))
