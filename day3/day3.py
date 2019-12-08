#!/usr/bin/python

WIRE1_VALUE = 1
WIRE2_VALUE = 2

dirs = { "U" : (0,  1),
         "D" : (0, -1),
         "L" : (-1, 0),
         "R" : ( 1, 0)}

def zero_manhattan_distance(loc):
    return abs(loc[0]) + abs(loc[1])


def electrical_distance(wire, target_loc):
    elec_dist = 0
    loc = (0, 0)

    for instruction in wire:
        # Where are we going and how far?
        dist = int(instruction[1:])
        delta = dirs[instruction[0]]

        for i in range(dist):
            loc = (loc[0] + delta[0], loc[1] + delta[1])
            elec_dist += 1

            if loc == target_loc:
                return elec_dist


def unroll_wire(wire, value):
    loc = (0, 0)

    for instruction in wire:
        # Where are we going and how far?
        dist = int(instruction[1:])
        delta = dirs[instruction[0]]

        for i in range(dist):
            loc = (loc[0] + delta[0], loc[1] + delta[1])
            if loc in grid:
                grid[loc] |= value
            else:
                grid[loc] = value
    return


# Open input file
filename = "day3.txt"
f = open(filename, "r")

grid = {}
intersections = {}

with open(filename, "r") as f:
    wire1 = f.readline().strip().split(",")
    wire2 = f.readline().strip().split(",")

    unroll_wire(wire1, WIRE1_VALUE)
    unroll_wire(wire2, WIRE2_VALUE)

    # Check wire intersections
    for loc, count in sorted(grid.items(), key=lambda item: item[1], reverse=True):
        if count == (WIRE1_VALUE | WIRE2_VALUE):
            intersections[loc] = electrical_distance(wire1, loc) + electrical_distance(wire2, loc)

    # Report nearest intersection
    nearest_intersection = sorted(intersections.items(), key=lambda item: item[1])[0]
    print "Nearest wire intersection is at {0} at a distance of {1}".format(nearest_intersection[0], nearest_intersection[1])