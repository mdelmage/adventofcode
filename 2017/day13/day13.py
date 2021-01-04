#!/usr/bin/env python
# -*- coding: utf-8 -*-

def run1():
    severity = 0
    for layer in firewall:
        # A scanner's period is given by its range.
        period = ((firewall[layer] - 1) * 2)
        caught = (layer % period) == 0

        if caught:
            # The severity of getting caught on a layer is equal to its depth multiplied by its range.
            # (Ignore layers in which you do not get caught.)
            severity += (layer * firewall[layer])
    return severity

def run2(delay):
    for layer in firewall:
        # A scanner's period is given by its range.
        period = ((firewall[layer] - 1) * 2)

        # For each picosecond you delay the packet before beginning your trip, all security scanners move one step.
        caught = ((layer + delay) % period) == 0
        if caught: return True
    return False

# Parse the firewall layers configuration, and save each line
with open('day13_input.txt') as f:
    layers = [line.rstrip('\n').split(': ') for line in f]

# By studying the firewall briefly, you are able to record (in your puzzle input)
# the depth of each layer and the range of the scanning area for the scanner within it,
# written as depth: range. Each layer has a thickness of exactly 1. A layer at depth 0
# begins immediately inside the firewall; a layer at depth 1 would start immediately after that.
firewall = {}
for (layer, lrange) in layers:
    firewall[int(layer)] = int(lrange)

print 'Part One: severity is {0}.'.format(run1())

# You can't control the speed of the packet, but you can delay it any number of picoseconds.
# For each picosecond you delay the packet before beginning your trip, all security scanners
# move one step. You're not in the firewall during this time; you don't enter layer 0
# until you stop delaying the packet.
delay = 0
caught = True
while caught:
    delay += 1
    caught = run2(delay)

print 'Part Two: uncaught when delay is {0}.'.format(delay)