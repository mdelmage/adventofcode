#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "The locks are schematics that have the top row filled (#) and the bottom row empty (.);
# the keys have the top row empty and the bottom row filled. If you look closely, you'll see
# that each schematic is actually a set of columns of various heights, either extending downward
# from the top (for locks) or upward from the bottom (for keys)."
FILLED = '#'
EMPTY = '.'
FIRST_ROW_LOCK = FILLED * 5
FIRST_ROW_KEY = EMPTY * 5

def key_fits_lock(key, lock):
    for pin in range(5):
        if key[pin] + lock[pin] > 5: return False
    return True

# Parse the input.
with open('day25_input.txt') as f:
    locks_and_keys = [line.rstrip('\n') for line in f] + ['']


# "For locks, those are the pins themselves; you can convert the pins in schematics to a list of heights,
# one per column. For keys, the columns make up the shape of the key where it aligns with pins;
# those can also be converted to a list of heights."
locks = []
keys = []
while len(locks_and_keys) > 0:
    obj = [locks_and_keys.pop(0) for row in range(8)]
    if obj[0] == FIRST_ROW_LOCK:
        # For locks, start from the top and go down (rows increasing) until we find
        # the end of the pin, and then add that to the pins list.
        pins = []
        for col in range(5):
            for row in range(1, 7):
                if obj[row][col] == EMPTY:
                    pins.append(row - 1)
                    break
        locks.append(pins)
    else:
        # For keys, start from the bottom and go up (rows decreasing) until we find
        # the end of the key, and then add that to the teeth heights list.
        teeth = []
        for col in range(5):
            for row in range(5, -1, -1):
                if obj[row][col] == EMPTY:
                    teeth.append(5 - row)
                    break
        keys.append(teeth)

# Then, you can try every key with every lock.
fit_pairs = 0
for lock in locks:
    for key in keys:
        if key_fits_lock(key, lock): fit_pairs += 1

# Analyze your lock and key schematics. How many unique lock/key pairs fit together without overlapping in any column?
print('Part One: There are {0} unique lock/key pairs that fit without overlapping.'.format(fit_pairs))