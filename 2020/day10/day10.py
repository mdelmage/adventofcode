#!/usr/bin/env python
# -*- coding: utf-8 -*-

# You glance back down at your bag and try to remember why you brought so many adapters;
# there must be more than a trillion valid ways to arrange them! Surely, there must be
# an efficient way to count the arrangements.
traversal_cache = {}

def traverse(adapter):
    # Look at us, being all efficient and stuff
    if adapter in traversal_cache: return traversal_cache[adapter]

    # The last adapter only has itself to connect to
    if adapter == max(adapters): return 1

    options = 0
    for a in adapter_options[adapter]:
        options += traverse(a)

    # Add our hard work to the traversal cache
    traversal_cache[adapter] = options

    return options

# Parse the adapter list and save each line
with open('day10_input.txt') as f:
    # Treat the charging outlet near your seat as having an effective joltage rating of 0.
    adapters = [0]
    for line in f:
        adapters.append(int(line))

    # In addition, your device has a built-in joltage adapter rated for 3 jolts higher
    # than the highest-rated adapter in your bag.
    adapters = sorted(adapters)
    adapters.append(adapters[-1:][0] + 3)

# Find a chain that uses all of your adapters to connect the charging outlet to your device's built-in adapter
# and count the joltage differences between the charging outlet, the adapters, and your device.
adapter_history = {}
for i in range(1, len(adapters)):
    jolts = adapters[i] - adapters[i - 1]
    adapter_history[jolts] = adapter_history.get(jolts, 0) + 1

print 'Part One: 1-jolt differences times 3-jolt differences is {0}.'.format(adapter_history[1] * adapter_history[3])

adapter_options = {}
for i in range(len(adapters)):
    # Each of your joltage adapters is rated for a specific output joltage (your puzzle input).
    # Any given adapter can take an input 1, 2, or 3 jolts lower than its rating and still
    # produce its rated output joltage.
    adapter_options[adapters[i]] = [x for x in adapters[i + 1:] if x <= adapters[i] + 3]

print 'Part Two: There are {0} different ways to arrange the adapters.'.format(traverse(0))