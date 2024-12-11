#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the line of stones note.
with open('day11_input.txt') as f:
    stones = [int(n) for n in [line.rstrip('\n') for line in f][0].split()]

# Consider the arrangement of stones in front of you.
# How many stones will you have after blinking 25 times?
for blink in range(25):
    stones_next = []
    for stone in stones:
        stones_str = str(stone)
        # Sometimes, the number engraved on a stone changes. Other times, a stone might split in two,
        # causing all the other stones to shift over a bit to make room in their perfectly straight line.
        #
        # As you observe them for a while, you find that the stones have a consistent behavior.
        # Every time you blink, the stones each simultaneously change according to the first applicable rule
        # in this list:
        #
        # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        if stone == 0:
            stones_next.append(1)
        # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
        # The left half of the digits are engraved on the new left stone, and the right half of the digits
        # are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become
        # stones 10 and 0.)
        elif len(stones_str) % 2 == 0:
            stones_next.append(int(stones_str[:len(stones_str)//2]))
            stones_next.append(int(stones_str[len(stones_str)//2:]))
        # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
        else:
            stones_next.append(2024 * stone)

    stones = stones_next

print('Part One: After 25 blinks there are {0} stones.'.format(len(stones)))