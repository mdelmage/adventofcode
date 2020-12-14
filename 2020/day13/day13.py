#!/usr/bin/env python
# -*- coding: utf-8 -*-

OPTIMIZATION_LEVEL = 3

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
divisor_list = []
for i in range(len(bus_lines)):
    if bus_lines[i] > 0:
        divisor_list.append((i, bus_lines[i]))

# Pull out the largest 3 bus lines and their indices
top_divisors = sorted(bus_lines, reverse=True)[:OPTIMIZATION_LEVEL]
periodicity_checklist = []
for divisor in divisor_list:
    if divisor[1] in top_divisors:
        periodicity_checklist.append(divisor)

# Somewhat-naive optimization: take the highest few bus lines (divisors) and determine
# the periodicity of the times when they meet the arrival requirements.
n = 0
periodicity_matches = []
while len(periodicity_matches) < 2:
    n += 1
    match = True
    for (departure_offset, bus) in periodicity_checklist:
        if (n % bus) != bus - departure_offset:
            match = False
    if match:
        periodicity_matches.append(n)

initial_value = periodicity_matches[0]
periodicity = periodicity_matches[1] - periodicity_matches[0]

# Brute-force the departure times, but using the somewhat-optimized increment value
# we found earlier by checking the periodicity of the highest few bus lines.
n = initial_value
while True:
    n += periodicity
    match = True
    for (i, bus) in divisor_list:
        if ((n + i) % bus) != 0:
            match = False
            break
    if match: 
        print 'Part Two: Earliest departure time is {0}.'.format(n)
        break