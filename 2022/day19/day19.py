#!/usr/bin/env python
# -*- coding: utf-8 -*-

OPTIMIZATION_THRESHOLD = 2500

# The elephants are starting to look hungry, so you shouldn't take too long; you need
# to figure out which blueprint would maximize the number of opened geodes after 24 minutes
# by figuring out which robots to build and when to build them.
DEPTH_A = 24

# While you were choosing the best blueprint, the elephants found some food on their own,
# so you're not in as much of a hurry; you figure you probably have 32 minutes before
# the wind changes direction again and you'll need to get out of range of the erupting volcano.
DEPTH_B = 32

class GeologyResources:
    def __init__(self, ore, clay, obsidian, geodes):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geodes = geodes

    def __add__(self, g):
        return GeologyResources(self.ore + g.ore, self.clay + g.clay, self.obsidian + g.obsidian, self.geodes + g.geodes)

    def __sub__(self, g):
        return GeologyResources(self.ore - g.ore, self.clay - g.clay, self.obsidian - g.obsidian, self.geodes - g.geodes)

    def __ge__(self, g):
        return self.ore >= g.ore and self.clay >= g.clay and self.obsidian >= g.obsidian and self.geodes >= g.geodes

    def __hash__(self):
        return hash((self.ore, self.clay, self.obsidian, self.geodes))


def optimize(scenarios):
    max_geodes = max([inventory.geodes for inventory, robots in scenarios])

    # For smaller sets, do an exhaustive check (O(N^2)) to remove scenarios that are
    # objectively worse than others in the set (another scenario has equal or more of
    # both inventory and robots).
    #
    # This cuts the search space down immensely, but is too inefficient for larger sets.
    if len(scenarios) < OPTIMIZATION_THRESHOLD:
        prunelist = set()
        for s1 in scenarios:
            for s2 in scenarios:
                if s1 != s2 and s1[0] >= s2[0] and s1[1] >= s2[1]:
                    prunelist.add(s2)

        scenarios = set([s for s in scenarios if s not in prunelist])

    # Based on the rate at which you can purchase geode robots, if you are
    # more than two geodes behind, you will not be able to catch up, so
    # eliminate those scenarios.
    scenarios = set([(i, r) for i, r in scenarios if i.geodes >= max_geodes - 2])

    return scenarios

def generate(b, target_depth):
    minute = 0
    scenarios = set()
    scenarios.add((GeologyResources(0, 0, 0, 0), GeologyResources(1, 0, 0, 0)))

    # Advance minute-by-minute and figure out all the possible ways that we can
    # purchase (or not purchase) robots, and determine the best possible result.
    #
    # There are 4 possible purchases and a "do nothing" option, so we have
    # a ceiling of 5^N results. So reducing the amount of possible results
    # for each minute is critical. First, we check our inventory and don't purchase
    # a robot if we can't afford it; next, we prune any results that have fallen
    # behind the leaders by a certain amount (see the optimize() function).
    #
    # Also, do a small optimization by not simulating the last minute until
    # we're all done, and then run a quick "do nothing" scenario to get the
    # final results. This is because buying a robot in the last minute won't
    # produce anything, so we don't need to consider those scenarios.
    while minute < target_depth - 1:
        possible_next_scenarios = set()
        for i, r in scenarios:
            for cost, gain in b:
                inventory = i
                robots = r

                # If we can afford it, buy another robot.
                # Note that we snuck in the "do nothing" scenario by adding
                # a transaction above, that costs nothing and produces nothing.
                if inventory >= cost:
                    inventory -= cost

                    # Collect minerals
                    inventory += robots

                    # Potentially new robot is now ready
                    robots += gain

                    # Add this configuration to the next iteration
                    possible_next_scenarios.add((inventory, robots))

        scenarios = optimize(possible_next_scenarios)
        minute += 1

    # Now simulate the last minute
    scenarios = [(i + r, r) for i, r in scenarios]

    return max([inventory.geodes for inventory, robots in scenarios])

# Parse the blueprints file
with open('day19_input.txt') as f:
    blueprints = [line.rstrip('\n')for line in f]

blues = {}
for b in blueprints:
    # Strip off all the sentence structure and distill the inputs/outputs for each blueprint
    b = b.replace('Blueprint ', '')
    b = b.replace(': Each ore robot costs ', ',')
    b = b.replace('. Each clay robot costs ', ',')
    b = b.replace('. Each obsidian robot costs ', ',')
    b = b.replace('. Each geode robot costs ', ',')
    b = b.replace(' ore', '')
    b = b.replace(' clay', '')
    b = b.replace(' obsidian', '')
    b = b.replace(' and ', '/')
    b = b.replace('.', '')
    b = b.split(',')
    blueprint_num = int(b[0])
    blues[blueprint_num] = []
    blues[blueprint_num].append((GeologyResources(0, 0, 0, 0), GeologyResources(0, 0, 0, 0)))
    blues[blueprint_num].append((GeologyResources(int(b[1]), 0, 0, 0), GeologyResources(1, 0, 0, 0)))
    blues[blueprint_num].append((GeologyResources(int(b[2]), 0, 0, 0), GeologyResources(0, 1, 0, 0)))
    blues[blueprint_num].append((GeologyResources(int(b[3].split('/')[0]), int(b[3].split('/')[1]), 0, 0), GeologyResources(0, 0, 1, 0)))
    blues[blueprint_num].append((GeologyResources(int(b[4].split('/')[0]), 0, int(b[4].split('/')[1]), 0), GeologyResources(0, 0, 0, 1)))


# Determine the quality level of each blueprint using the largest number of geodes
# it could produce in 24 minutes. What do you get if you add up the quality level
# of all of the blueprints in your list?
quality_level = 0
for i in range(len(blues)):
    geodes = generate(blues[i + 1], DEPTH_A)
    # Determine the quality level of each blueprint by multiplying that blueprint's
    # ID number with the largest number of geodes that can be opened in 24 minutes
    # using that blueprint.
    quality_level += ((i + 1) * geodes)

print('Part One: quality level is {0}.'.format(quality_level))

# Don't worry about quality levels; instead, just determine the largest number
# of geodes you could open using each of the first three blueprints. What do you get
# if you multiply these numbers together?
geodes_product = 1
for i in range(3):
    geodes = generate(blues[i + 1], DEPTH_B)
    geodes_product *= geodes

print('Part Two: product of geodes is {0}.'.format(geodes_product))
