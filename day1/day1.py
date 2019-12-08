#!/usr/bin/python

import math

# Open input file
filename = "day1.txt"
f = open(filename, "r")

total_fuel = 0

with open(filename, "r") as f:
    for line in f:
        mass = int(line.strip())
        fuel = int(math.floor(mass / 3) - 2)
        total_fuel += fuel

print "Total Fuel Requirement: {0}".format(total_fuel)