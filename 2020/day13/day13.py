#!/usr/bin/env python
# -*- coding: utf-8 -*-

def find_periodicity(n, step, buses):
    # Using the initial value and step amount, scan for two matches
    # that satisfy all the buses in the list.

    # The first match describes the earliest time the buses meet our requirements.
    match = False
    while not match:
        match = True
        for (bus, offset) in buses:
            if ((n + offset) % bus) != 0:
                match = False
                break
        if match: initial_match = n
        n += step

    # The second match describes the periodicity of the times that meet our requirements.
    # Our inputs are all prime numbers, so we could just say that the periodicity is just
    # the product of the inputs, but the more general solution requires us to allow for
    # inputs that share a common factor.
    match = False
    while not match:
        match = True
        for (bus, offset) in buses:
            if ((n + offset) % bus) != 0:
                match = False
                break
        if match: periodicity = n - initial_match
        n += step

    return (initial_match, periodicity)

# Parse the shuttle bus notes and save each line
with open('day13_input.txt') as f:
    earliest_departure_time = int(f.readline())
    schedule = f.readline().rstrip('\n').split(',')
    
    # Filter out any out-of-service bus lines
    bus_lines = []
    for b in schedule:
        if b == 'x':
            bus_lines.append(-1)
        else:
            bus_lines.append(int(b))

best_departure_time = 100000000
best_departure_bus = None
best_departure_wait_time = None

# To save time once you arrive, your goal is to figure out the earliest bus
# you can take to the airport. (There will be exactly one such bus.)
for b in [x for x in bus_lines if x > 0]:
    departure_time = earliest_departure_time + b - (earliest_departure_time % b)
    if departure_time < best_departure_time:
        best_departure_time = departure_time
        best_departure_bus = b
        best_departure_wait_time = departure_time - earliest_departure_time

# What is the ID of the earliest bus you can take to the airport
# multiplied by the number of minutes you'll need to wait for that bus?
print 'Part One: Bus ID {0} times wait time {1} = {2}.'.format(best_departure_bus,
                                                               best_departure_wait_time,
                                                               best_departure_bus * best_departure_wait_time)



# entries that show x must be out of service, so you decide to ignore them.
buses_in_service = []
for i in range(len(bus_lines)):
    if bus_lines[i] > 0:
        buses_in_service.append((bus_lines[i], i))

# Optimize the problem by considering an ever-growing list of buses.
# Once we understand the initial values and periodicity of their matches,
# we can add more buses to the list without incurring much penalty, by
# skipping all the time slots that did not meet earlier bounds.
#
# As we consider more buses, the step value will grow, making our search faster.
(n, step) = (0, 1)
for i in range(len(buses_in_service)):
    (n, step) = find_periodicity(n, step, buses_in_service[:i + 1])

print 'Part Two: Earliest departure time is {0}.'.format(n)