#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the device outputs map
with open('day11_input.txt') as f:
    devices = [line.rstrip('\n').split(': ') for line in f]

paths = {}
for source, dest in devices:
    paths[source] = []
    for d in dest.split():
        paths[source].append(d)


tours = [{('you', True, True): 1}]
while len(tours[-1]) > 0:
    #print(len(tours))
    next_step = {}
    # For each tour of length N, determine our destinations at N+1 and
    # whether they include the required stops ('dac' and 'fft').
    for (source, visited_dac, visited_fft) in tours[-1]:
        if source == 'out': continue
        for dest in paths[source]:
            count = next_step.get((dest, visited_dac, visited_fft), 0) + tours[-1][(source, visited_dac, visited_fft)]
            visited_dac_new = visited_dac | (dest == 'dac')
            visited_fft_new = visited_fft | (dest == 'fft')
            #print(source, visited_dac, visited_fft, dest, ': ', count)
            next_step[(dest, visited_dac_new, visited_fft_new)] = count
    tours.append(next_step)
    #print(len(tours), next_step)
    #print(tours)

total_tours = 0
for i in range(len(tours)):
    #print(tours[i].get(('out', True, True), 0))
    total_tours += tours[i].get(('out', True, True), 0)
    #print(i, len(tours[i]))

print(total_tours)

tours = [{('svr', False, False): 1}]
while len(tours[-1]) > 0:
    #print(len(tours))
    next_step = {}
    # For each tour of length N, determine our destinations at N+1 and
    # whether they include the required stops ('dac' and 'fft').
    for (source, visited_dac, visited_fft) in tours[-1]:
        if source == 'out': continue
        for dest in paths[source]:
            count = next_step.get((dest, visited_dac, visited_fft), 0) + tours[-1][(source, visited_dac, visited_fft)]
            visited_dac_new = visited_dac | (dest == 'dac')
            visited_fft_new = visited_fft | (dest == 'fft')
            #print(source, visited_dac, visited_fft, dest, ': ', count)
            next_step[(dest, visited_dac_new, visited_fft_new)] = count
    tours.append(next_step)
    #print(len(tours), next_step)
    #print(tours)

total_tours = 0
for i in range(len(tours)):
    #print(i, tours[i].get(('out', True, True), 0))
    total_tours += tours[i].get(('out', True, True), 0)
    #print(i, len(tours[i]))

print(total_tours)