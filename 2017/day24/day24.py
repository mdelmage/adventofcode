#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy

longest_bridge_length = 0
longest_bridge_score = 0

def build(port, score, components_used, components_free):
    global longest_bridge_length
    global longest_bridge_score

    # What is the strength of the longest bridge you can make? If you can make multiple bridges of the longest length, pick the strongest one.
    if (len(components_used) > longest_bridge_length) or (len(components_used) == longest_bridge_length and score > longest_bridge_score):
        longest_bridge_length = len(components_used)
        longest_bridge_score = score

    # Recursive search of the strongest bridge, given the remaining components.
    highest_score = score
    candidates = []
    for c in components_free:
        if c[0] == port or c[1] == port:
            # Figure out which port we're connecting, then search for a match for the other one.
            if c[0] == port:
                new_port = c[1]
            else:
                new_port = c[0]

            # Calculate the new score and the components left, and recurse!
            new_score = score + c[0] + c[1]
            new_components_used = components_used + [c]
            new_components_free = copy.deepcopy(components_free)
            new_components_free.remove(c)
            new_score = build(new_port, new_score, new_components_used, new_components_free)

            if new_score > highest_score:
                highest_score = new_score
    return highest_score

# Parse the components list file
with open('day24_input.txt') as f:
    components = []
    for line in f:
        # Each component has two ports, one on each end.
        # The ports come in all different types, and only matching types can be connected.
        components.append([int(n) for n in line.split('/')])

# Your side of the pit is metallic; a perfect surface to connect a magnetic,
# zero-pin port. Because of this, the first port you use must be of type 0.
port_type = 0

print 'Part One: Strongest bridge that can be built has strength = {0}.'.format(build(port_type, 0, [], components))
print 'Part Two: Longest bridge, tiebreaker strongest bridge, has stregth {0}.'.format(longest_bridge_score)