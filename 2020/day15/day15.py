#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Given your starting numbers, what will be the 2020th number spoken?
PART_ONE_TURNS = 2020

# Impressed, the Elves issue you a challenge: determine the 30000000th number spoken.
PART_TWO_TURNS = 30000000

# Parse the starting numbers and save each line
with open('day15_input.txt') as f:
    games_list = [line.rstrip('\n') for line in f]
    games = []
    for numbers in games_list:
        games.append([int(x) for x in numbers.split(',')])

for starting_numbers in games:
    turn = 1
    spoken_numbers = {}

    # In this game, the players take turns saying numbers.
    # They begin by taking turns reading from a list of starting numbers.
    for n in starting_numbers:
        spoken_numbers[n] = (turn, None)
        last_spoken_number = n
        turn += 1

    while True:
        # Then, each turn consists of considering the most recently spoken number:
        (last_spoken_turn, prev_spoken_turn) = spoken_numbers[last_spoken_number]

        # If that was the first time the number has been spoken, the current player says 0.
        # Otherwise, the number had been spoken before; the current player announces
        # how many turns apart the number is from when it was previously spoken.
        if prev_spoken_turn:
            say = last_spoken_turn - prev_spoken_turn
        else:
            say = 0

        # Update the record of the previous two turns this number was spoken.
        # Was the crux of this problem to only save the previous two turns?
        # Hard to say.
        (last_spoken_turn, prev_spoken_turn) = spoken_numbers.get(say, (None, None))
        spoken_numbers[say] = (turn, last_spoken_turn)
        last_spoken_number = say

        if turn == PART_ONE_TURNS:
            print 'Part One: the {0}th number spoken is {1}.'.format(turn, say)
        if turn == PART_TWO_TURNS:
            print 'Part Two: the {0}th number spoken is {1}.'.format(turn, say)
            # (The game ends when the Elves get sick of playing or dinner is ready,
            # whichever comes first.)
            break

        turn += 1