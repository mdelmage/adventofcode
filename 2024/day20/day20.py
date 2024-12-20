#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The map consists of track (.) - including the start (S) and end (E) positions
# (both of which also count as track) - and walls (#).
TRACK = '.'
START = 'S'
END   = 'E'
WALL  = '#'

NEIGHBORS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan_dist(src, dest):
    return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

def count_cheats(cheat_len, cheat_threshold):
    savings = 0
    for cheat_step in range(len(path)):
        cheat_src = path[cheat_step]
        for col in range(cheat_src[0] - cheat_len, cheat_src[0] + cheat_len + 1):
            for row in range(cheat_src[1] - cheat_len, cheat_src[1] + cheat_len + 1):
                cheat_dest = (col, row)
                if cheat_dest != cheat_src and racetrack.get(cheat_dest, WALL) != WALL and manhattan_dist(cheat_src, cheat_dest) <= cheat_len:
                    steps_saved = path.index(cheat_dest) - path.index(cheat_src) - manhattan_dist(cheat_src, cheat_dest)
                    if steps_saved >= cheat_threshold:
                        savings += 1
    return savings

# Parse the racetrack map.
with open('day20_input.txt') as f:
    r = [line.rstrip('\n') for line in f]
    racetrack = {}
    for row in range(len(r)):
        for col in range(len(r[0])):
            if r[row][col] == START: pos_start = (col, row)
            if r[row][col] == END: pos_end = (col, row)
            racetrack[(col, row)] = r[row][col]

path = [pos_start]
while pos_end not in path:
    pos = path[-1]
    for p in [(pos[0] + n[0], pos[1] + n[1]) for n in NEIGHBORS]:
        if racetrack.get(p, WALL) in [TRACK, END] and p not in path: path.append(p)

# You aren't sure what the conditions of the racetrack will be like, so to give yourself as many options as possible,
# you'll need a list of the best cheats. How many cheats would save you at least 100 picoseconds?
print('Part One: There are {0} length-2 cheats that would save at least 100 picoseconds.'.format(count_cheats(2, 100)))

# The programs seem perplexed by your list of cheats. Apparently, the two-picosecond cheating rule was deprecated
# several milliseconds ago! The latest version of the cheating rule permits a single cheat that instead lasts
# at most 20 picoseconds.
#
# Find the best cheats using the updated cheating rules. How many cheats would save you at least 100 picoseconds?
print('Part Two: There are {0} length-20 cheats that would save at least 100 picoseconds.'.format(count_cheats(20, 100)))