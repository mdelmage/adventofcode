#!/usr/bin/python

class Body:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def orbit_count(self):
        direct_orbits = 1
        indirect_orbits = 0 if self.parent == "COM" else bodies[self.parent].orbit_count()
        return direct_orbits + indirect_orbits

# Open input file
filename = "day6.txt"
f = open(filename, "r")

bodies = {}
orbit_count = 0

with open(filename, "r") as f:
    for line in f:
        parent, name = line.strip().split(")")
        bodies[name] = Body(name, parent)

for body in bodies:
    orbit_count += bodies[body].orbit_count()

print "{0} total direct+indirect orbits in the system.".format(orbit_count)