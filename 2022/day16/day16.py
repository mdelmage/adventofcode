#!/usr/bin/env python
# -*- coding: utf-8 -*-

STARTING_NODE = 'AA'

TIME_LIMIT_PART_ONE = 30
TIME_LIMIT_PART_TWO = 26

# Determine the path length of every indirect neighbor.
def find_paths(start):
    level = 0
    nodes_to_consider = [start]
    nodes_visited = set()
    paths = {}

    while len(nodes_to_consider) > 0:
        next_nodes_to_consider = []
        for n in nodes_to_consider:
            nodes_visited.add(n)
            paths[n] = level
            for nn in valves[n].neighbors:
                if valves[n].neighbors[nn] == 1 and nn not in nodes_visited: next_nodes_to_consider.append(nn)

        nodes_to_consider = next_nodes_to_consider
        level += 1

    return paths

class Valve:
    def __init__(self, name, flowrate):
        self.name = name
        self.flowrate = flowrate
        self.neighbors = {}

    def addNeighbor(self, name, distance=1):
        self.neighbors[name] = distance

    def update(self, neighbors):
        for n in neighbors:
            self.neighbors[n] = neighbors[n]


# Parse the valve flow rate file
with open('day16_input.txt') as f:
    valve_list = [line.rstrip('\n') for line in f]

remove_list = []
valve_names = []
valves = {}
for v in valve_list:
    # Remove sentence clutter and distill input down to a comma-separated list
    v = v.replace('Valve ', '')
    v = v.replace(' has flow rate=', ',')
    v = v.replace('; tunnels lead to', ',')
    v = v.replace('; tunnel leads to', '')
    v = v.replace('valves ', '')
    v = v.replace('valve ', ',')
    v = v.replace(' ', '')
    v = v.split(',')

    # Set up the valve, and link its direct neighbors
    name = v[0]
    flowrate = int(v[1])
    neighbors = v[2:]
    v = Valve(name, flowrate)
    valves[name] = v
    for n in neighbors:
        v.addNeighbor(n)

    # All of the valves begin closed. You start at valve AA, but it must be damaged
    # or jammed or something: its flow rate is 0, so there's no point in opening it.
    #
    # Based on this statement, we should remove the zero-flow valves from our problem.
    # Keep the starting valve, though.
    if flowrate > 0: 
        valve_names.append(name)
    elif name != STARTING_NODE:
        remove_list.append(name)

# Link all valves to each other. Indirect neighbors will have path length > 1.
for v in valves:
    valves[v].update(find_paths(v))

# Remove the "jammed" valves from both the main list and the neighbor links.
for r in remove_list:
    del valves[r]
    for v in valves:
        valves[v].neighbors.pop(r, None)

# Making your way through the tunnels like this, you could probably open many or all of the valves
# by the time 30 minutes have elapsed. However, you need to release as much pressure as possible,
# so you'll need to be methodical.
best_score = 0
scenarios = set()
scenarios.add((0, STARTING_NODE, tuple(), 0, 0))

# Exhaustive search of scenarios. Keep iterating until there are none left to consider.
while len(scenarios) > 0:
    next_scenarios = set()

    # Consider each place we could go next. Don't revisit previous nodes (valves we've opened)
    # and never return to the starting valve.
    for (minute, loc, valves_open, pressure_rate, pressure_total) in scenarios:
        possible_neighbors = [n for n in valves[loc].neighbors if n not in valves_open and n != STARTING_NODE]

        # Pre-caluclate our score, and check if it's the best so far.
        score = pressure_total + (pressure_rate * (TIME_LIMIT_PART_ONE - minute))
        best_score = max(best_score, score)

        # If we can go elsewhere, let's do it now -- except if we would exceed the time limit.
        for n in possible_neighbors:
            next_minute = minute + valves[loc].neighbors[n] + 1
            next_valves_open = tuple(sorted(valves_open + (n,)))
            next_pressure_rate = pressure_rate + valves[n].flowrate
            next_pressure_total = pressure_total + ((next_minute - minute) * pressure_rate)
            sc = (next_minute, n, next_valves_open, next_pressure_rate, next_pressure_total)
            if next_minute <= TIME_LIMIT_PART_ONE: next_scenarios.add(sc)
    scenarios = next_scenarios

# Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?
print('Part One: most pressure that can be released is {0}.'.format(best_score))

# You're worried that even with an optimal approach, the pressure released won't be enough.
# What if you got one of the elephants to help you?
best_score = 0
scenarios = set()
scenarios.add((0, (STARTING_NODE, None, None), (STARTING_NODE, None, None), tuple(), 0, 0))

# Set up again, but consider two positions (yourself and the elephant) during the search.
while len(scenarios) > 0:
    next_scenarios = set()

    for (minute, you, elephant, valves_open, pressure_rate, pressure_total) in scenarios:
        # Set up our working variables for this scenario. We'll modify some or all of them.
        next_minute = minute
        next_valves_open = valves_open
        next_pressure_rate = pressure_rate
        next_pressure_total = pressure_total

        loc_you = you[0]
        dest_you = you[1]
        minute_you = you[2]

        loc_elephant = elephant[0]
        dest_elephant = elephant[1]
        minute_elephant = elephant[2]

        # If we are just beginning, we won't have left the starting valve yet (and therefore won't have
        # an arrival minute. Don't calculate any next paths in that condition.
        if minute_you:
            if minute_you == minute_elephant:
                # You and the elephant both arrive at a valve on the same minute!
                # Jump in time to that minute and calculate the pressure relieved.
                next_pressure_total += ((minute_you - next_minute) * next_pressure_rate)
                next_minute = minute_you

                # Open the valve you arrived at.
                loc_you = dest_you
                dest_you = None
                minute_you = None
                next_valves_open = tuple(sorted(next_valves_open + (loc_you,)))
                next_pressure_rate += valves[loc_you].flowrate

                # Open the valve the elephant arrived at.
                loc_elephant = dest_elephant
                dest_elephant = None
                minute_elephant = None
                next_valves_open = tuple(sorted(next_valves_open + (loc_elephant,)))
                next_pressure_rate += valves[loc_elephant].flowrate
            elif minute_you < minute_elephant:
                # You arrived at a valve!
                # Jump in time to that minute and calculate the pressure relieved.
                # The elephant is still moving to its destination.
                next_pressure_total += ((minute_you - next_minute) * next_pressure_rate)
                next_minute = minute_you

                # Open the valve you arrived at.
                loc_you = dest_you
                dest_you = None
                minute_you = None
                next_valves_open = tuple(sorted(next_valves_open + (loc_you,)))
                next_pressure_rate += valves[loc_you].flowrate
            elif minute_elephant < minute_you:
                # The elephant arrived at a valve!
                # Jump in time to that minute and calculate the pressure relieved.
                # You are still moving to your destination.
                next_pressure_total += ((minute_elephant - next_minute) * next_pressure_rate)
                next_minute = minute_elephant

                # Open the valve the elephant arrived at.
                loc_elephant = dest_elephant
                dest_elephant = None
                minute_elephant = None
                next_valves_open = tuple(sorted(next_valves_open + (loc_elephant,)))
                next_pressure_rate += valves[loc_elephant].flowrate

        # Oops, we ran out of time, so give up on this path.
        if next_minute > TIME_LIMIT_PART_TWO:
            continue

        # Pre-caluclate our score, and check if it's the best so far.
        score = next_pressure_total + (next_pressure_rate * (26 - next_minute))
        best_score = max(best_score, score)

        # Further optimization (one needed for the program to complete in a reasonable amount of time):
        #
        # Calculate the best-case scenario from here -- if you and the elephant magically arrive at all the remaining
        # valves on minute+1 and open them on minute+2, what is your max score?
        # If that's less than something we've already calculated, drop it from the candidates.
        p = [n for n in valves[loc_you].neighbors if n not in next_valves_open and n != STARTING_NODE]
        remaining_flowrate = sum([valves[n].flowrate for n in p])
        if next_minute + 1 < TIME_LIMIT_PART_TWO:
            optimistic_score = score + remaining_flowrate * (TIME_LIMIT_PART_TWO - next_minute - 2)
            if optimistic_score < best_score:
                # We can't beat our score even under ideal conditions; bail out.
                continue

        # If we can go elsewhere, let's do it now -- except if we would exceed the time limit.
        if dest_you is None and dest_elephant is None:
            # Calculate new paths for both you and elephant.
            p = [n for n in valves[loc_you].neighbors if n not in next_valves_open and n != STARTING_NODE]
            possible_neighbors = [(n1, n2) for n1 in p for n2 in p if (n1 != n2) or (n1 == loc_you and n2 == loc_elephant)]
            for n_you, n_elephant in possible_neighbors:
                next_you = (loc_you, n_you, next_minute + valves[loc_you].neighbors[n_you] + 1)
                next_elephant = (loc_elephant, n_elephant, next_minute + valves[loc_elephant].neighbors[n_elephant] + 1)
                sc = (next_minute, next_you, next_elephant, next_valves_open, next_pressure_rate, next_pressure_total)
                if next_minute <= TIME_LIMIT_PART_TWO: next_scenarios.add(sc)
        elif dest_you is None:
            # Calculate a new path for yourself only. Elephant is still travelling.
            possible_neighbors = [n for n in valves[loc_you].neighbors if n not in next_valves_open and n != dest_elephant and n != STARTING_NODE]

            # Awkward situation where there are no more paths to consider, but elephant could still
            # reach a valve, open it, and add pressure relief to our score.
            # We have enough to forward-calculate that, so do it now.
            if len(possible_neighbors) == 0 and minute_elephant > next_minute and you[2] == next_minute:
                score = score + ((TIME_LIMIT_PART_TWO - minute_elephant) * valves[dest_elephant].flowrate)
                best_score = max(best_score, score)

            for n_you in possible_neighbors:
                next_you = (loc_you, n_you, next_minute + valves[loc_you].neighbors[n_you] + 1)
                next_elephant = elephant
                sc = (next_minute, next_you, next_elephant, next_valves_open, next_pressure_rate, next_pressure_total)
                if next_minute <= TIME_LIMIT_PART_TWO: next_scenarios.add(sc)
        elif dest_elephant is None:
            # Calculate a new path for the elephant only. You are still travelling.
            possible_neighbors = [n for n in valves[loc_elephant].neighbors if n not in next_valves_open and n != dest_you and n != STARTING_NODE]

            # Awkward situation where there are no more paths to consider, but elephant could still
            # reach a valve, open it, and add pressure relief to our score.
            # We have enough to forward-calculate that, so do it now.
            if len(possible_neighbors) == 0 and minute_you > next_minute and elephant[2] == next_minute:
                score = score + ((TIME_LIMIT_PART_TWO - minute_you) * valves[dest_you].flowrate)
                best_score = max(best_score, score)

            for n_elephant in possible_neighbors:
                next_you = you
                next_elephant = (loc_elephant, n_elephant, next_minute + valves[loc_elephant].neighbors[n_elephant] + 1)
                sc = (next_minute, next_you, next_elephant, next_valves_open, next_pressure_rate, next_pressure_total)
                if next_minute <= TIME_LIMIT_PART_TWO: next_scenarios.add(sc)
    scenarios = next_scenarios

# With you and an elephant working together for 26 minutes, what is the most pressure you could release?
print('Part Two: most pressure that can be released is {0}.'.format(best_score))
