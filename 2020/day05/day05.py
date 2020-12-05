#!/usr/bin/env python
# -*- coding: utf-8 -*-

FRONT_SECTION = 'F'
BACK_SECTION = 'B'
LEFT_SECTION = 'L'
RIGHT_SECTION = 'R'

# Parse the boarding passes and save each line
with open('day05_input.txt') as f:
    boarding_passes = [line.rstrip('\n') for line in f]

max_seat_id = 0
seat_ids = []
for p in boarding_passes:
    row = 0
    col = 0
    # The first 7 characters will either be F or B; these specify exactly one of
    # the 128 rows on the plane (numbered 0 through 127). Each letter tells you
    # which half of a region the given seat is in. Start with the whole list of
    # rows; the first letter indicates whether the seat is in the front (0 through 63)
    # or the back (64 through 127). The next letter indicates which half of that region
    # the seat is in, and so on until you're left with exactly one row.
    for i in range(7):
        row += ((p[6 - i] == BACK_SECTION) << i)

    # The last three characters will be either L or R; these specify exactly one of
    # the 8 columns of seats on the plane (numbered 0 through 7). The same process as
    # above proceeds again, this time with only three steps. L means to keep the
    # lower half, while R means to keep the upper half.
    for i in range(3):
        col += ((p[9 - i] == RIGHT_SECTION) << i)

    # Every seat also has a unique seat ID: multiply the row by 8, then add the column.
    seat_id = (8 * row) + col
    seat_ids.append(seat_id)
    if seat_id > max_seat_id:
        max_seat_id = seat_id

print 'Part One: highest seat ID was {0}.'.format(max_seat_id)

# It's a completely full flight, so your seat should be the only missing
# boarding pass in your list. However, there's a catch: some of the seats
# at the very front and back of the plane don't exist on this aircraft, so
# they'll be missing from your list as well.
last_seat_id = None
for seat in sorted(seat_ids):
    if last_seat_id:
        # Your seat wasn't at the very front or back, though; the seats with IDs
        # +1 and -1 from yours will be in your list.
        if seat != last_seat_id + 1:
            print 'Part Two: your seat ID is {0}.'.format(last_seat_id + 1)
    last_seat_id = seat