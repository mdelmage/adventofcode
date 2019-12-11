#!/usr/bin/python

class Body:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def orbit_count(self):
        direct_orbits = 1
        indirect_orbits = 0 if self.parent == "COM" else bodies[self.parent].orbit_count()
        return direct_orbits + indirect_orbits

    def orbit_path(self):
        if self.parent == "COM":
            return []
        else:
            path = bodies[self.parent].orbit_path()
            path.append(self)
            return path

    def orbit_dist(self, dest):
        path = self.orbit_path()
        dest_path = bodies[dest].orbit_path()

        # Clip ourselves and the destination object
        path = path[:-1]
        dest_path = dest_path[:-1]

        # Trim the common bodies from the paths
        for body in path[:]:
            if body in dest_path[:]:
                path[:] = [x for x in path if x is not body]
                dest_path[:] = [x for x in dest_path if x is not body]

        # The remaining paths are the travel distance
        return len(path) + len(dest_path)

# Open input file
filename = "day06.txt"
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
print "YOU --> SAN travel distance is {0}.".format(bodies["YOU"].orbit_dist("SAN"))