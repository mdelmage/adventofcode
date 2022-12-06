#!/usr/bin/env python
# -*- coding: utf-8 -*-

def scan_unique(buffer, scan_length):
    ch = 0
    while True:
        if len(set(buffer[ch:ch + scan_length])) == scan_length:
            return ch + scan_length
        ch += 1

# Parse the datastream buffer file
with open('day06_input.txt') as f:
    signals = [line.rstrip('\n') for line in f]

# To fix the communication system, you need to add a subroutine to the device
# that detects a start-of-packet marker in the datastream. In the protocol being used
# by the Elves, the start of a packet is indicated by a sequence of four characters
# that are all different.
for signal in signals:
    print('Part One: first start-of-packet marker detected after {0} characters.'.format(scan_unique(signal, 4)))

# Your device's communication system is correctly detecting packets, but still
# isn't working. It looks like it also needs to look for messages.
#
# A start-of-message marker is just like a start-of-packet marker, except
# it consists of 14 distinct characters rather than 4.
for signal in signals:
    print('Part Two: first start-of-message marker detected after {0} characters.'.format(scan_unique(signal, 14)))
