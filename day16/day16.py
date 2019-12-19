#!/usr/bin/python
# coding: utf-8

PATTERN_BASE = [0, 1, 0, -1]

def fft(number, phases):
    print "FFTing {0} for {1} phases!".format(number, phases)

    # Turn the input into a list
    signal = [int(x) for x in number]

    for phase in range(phases):
        new_signal = []
        for digit in range(1, len(signal) + 1):
            pattern = [item for item in PATTERN_BASE for i in range(digit)]
            while len(pattern) < len(signal) + 1:
                pattern += pattern
            
            # lol list comprehensions
            new_signal.append(abs(sum([x*y for x,y in zip(pattern[1:len(signal) + 1], signal)])) % 10)

        signal = new_signal
    print signal[:8]

# Open input file
filename = "day16.txt"
with open(filename, "r") as f:
    for line in f:
        i = line.strip()
        fft(i, 100)