#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the almanac
with open('day05_input.txt') as f:
    # This almanac is a big jumbled mess. Parse it semi-manually.
    # Note that we don't care about the actual names of the mappings, such as 'seed->soil'.
    # We only need to give them an index, so we can process them in order.
    almanac = [line.rstrip('\n') for line in f]
    maps = {}
    line = 0

    # The almanac starts by listing which seeds need to be planted.
    seeds = [int(n) for n in almanac[line].split('seeds: ')[1].split()]
    line += 3

    # The rest of the almanac contains a list of maps which describe how to convert numbers
    # from a source category into numbers in a destination category.
    map_count = 0
    while line < len(almanac):
        maps[map_count] = []
        while line < len(almanac) and len(almanac[line]) > 0:
            # Rather than list every source number and its corresponding destination number one by one,
            # the maps describe entire ranges of numbers that can be converted. Each line within a map
            # contains three numbers: the destination range start, the source range start, and the range length.
            maps[map_count].append([int(n) for n in almanac[line].split()])
            line += 1
        line += 2
        map_count += 1

# Arbitrarily large number -- yeah, I know
lowest_location = 10 ** 100

# The gardener and his team want to get started as soon as possible, so they'd like to know the
# closest location that needs a seed. Using these maps, find the lowest location number that corresponds
# to any of the initial seeds.
for s in seeds:
    value = s
    # Start at the lowest map (seed->soil) and work forwards to the highest (humidity->location).
    for m in range(map_count):
        # Each line within a map contains three numbers: the destination range start,
        # the source range start, and the range length.
        for (dest, src, length) in maps[m]:
            if value >= src and value < src + length:
                # Found a valid mapping range for this value; apply the offset
                value += dest - src
                break
    lowest_location = min(lowest_location, value)

print('Part One: Lowest location that corresponds to a seed is {0}.'.format(lowest_location))

# It's too computationally expensive, for complex puzzle inputs with large seed ranges, to do an
# exhaustive check of all seeds to see which the lowest resulting location is.
#
# So instead, let's work backwards.
#
# Let's start with location=0 and then check to see if the seed required to produce it
# is somewhere in our valid seed ranges. If not, we'll check location=1, and then location=2,
# and so on, and keep incrementing until we find a valid seed. That's the lowest possible
# location number for our puzzle input.
location = -1
done = False
while not done:
    location += 1
    value = location
    # Start at the highest map (location->humidity) and work backwards to the lowest (soil->seed).
    for m in range(map_count - 1, -1, -1):
        # We're going backwards, so the position of src and dest must be swapped also.
        for (src, dest, length) in maps[m]:
            if value >= src and value < src + length:
                # Found a valid mapping range for this value; apply the offset
                value += dest - src
                break

    # Everyone will starve if you only plant such a small number of seeds.
    # Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.
    #
    # The values on the initial seeds: line come in pairs. Within each pair,
    # the first value is the start of the range and the second value is the length of the range.
    for s in range(len(seeds) // 2):
        start = seeds[2 * s]
        length = seeds[2 * s + 1]
        if value >= start and value < start + length:
            # The calculated seed is somewhere in our valid seed ranges! All done!
            done = True

print('Part Two: Lowest location that corresponds to a seed is {0}.'.format(location))