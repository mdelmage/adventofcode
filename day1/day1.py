#!/usr/bin/python

import math

def fuel_requirements(mass):
    return max(0, int(math.floor(mass / 3) - 2))

# Open input file
filename = "day1.txt"
f = open(filename, "r")

total_fuel = 0
total_fuel_including_fuel = 0

with open(filename, "r") as f:
    for line in f:
        mass = int(line.strip())
        fuel = fuel_requirements(mass)
        total_fuel += fuel
        total_fuel_including_fuel += fuel

        while fuel > 0:
            fuel = fuel_requirements(fuel)
            total_fuel_including_fuel += fuel

print "Total Fuel Requirement: {0}".format(total_fuel)
print "Total Fuel Requirement (including fuel): {0}".format(total_fuel_including_fuel)