#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the race records paper
with open('day06_input.txt') as f:
    races = [line.rstrip('\n') for line in f]

times = [int(n) for n in races[0].split('Time: ')[1].split()]
records = [int(n) for n in races[1].split('Distance: ')[1].split()]

score = 1
for race in range(len(times)):
    time = times[race]
    record = records[race]
    # Your toy boat has a starting speed of zero millimeters per millisecond.
    # For each whole millisecond you spend at the beginning of the race holding down the button,
    # the boat's speed increases by one millimeter per millisecond.

    # To see how much margin of error you have, determine the number of ways you can beat the record in each race.
    winning_strategies = 0
    for hold in range(1, time):
        distance = (time - hold) * hold
        if distance > record: winning_strategies += 1

    # Determine the number of ways you could beat the record in each race.
    # What do you get if you multiply these numbers together?
    score *= winning_strategies

print('Part One: Product of all the ways to beat the records in each race is {0}.'.format(score))

# As the race is about to start, you realize the piece of paper with race times and record distances
# you got earlier actually just has very bad kerning. There's really only one race - ignore the spaces
# between the numbers on each line.
time = int(races[0].replace(' ', '').split('Time:')[1])
record = int(races[1].replace(' ', '').split('Distance:')[1])

# How many ways can you beat the record in this one much longer race?
winning_strategies = 0
for hold in range(1, time):
    distance = (time - hold) * hold
    if distance > record: winning_strategies += 1

print('Part Two: Sum of all the ways to beat the records in the race is {0}.'.format(winning_strategies))