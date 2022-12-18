#!/usr/bin/env python
# -*- coding: utf-8 -*-

NEIGHBORS = [( 1,  0,  0),
             (-1,  0,  0),
             ( 0,  1 , 0),
             ( 0, -1,  0),
             ( 0,  0,  1),
             ( 0,  0, -1)]

# Parse the droplet scan file
with open('day18_input.txt') as f:
    droplets = [tuple([int(n) for n in line.rstrip('\n').split(',')]) for line in f]

x_min = 1000
x_max = -1000
y_min = 1000
y_max = -1000
z_min = 1000
z_max = -1000

# Bound the lava droplet search area. Allow one extra unit for steam to flow around it.
for d in droplets:
    x_min = min(x_min, d[0] - 1)
    x_max = max(x_max, d[0] + 1)
    y_min = min(y_min, d[1] - 1)
    y_max = max(y_max, d[1] + 1)
    z_min = min(z_min, d[2] - 1)
    z_max = max(z_max, d[2] + 1)

# Start at the "uppermost corner" and expand the steam cloud over/into the lava droplet.
steam = set()
current_expansion = set()
current_expansion.add((x_max + 1, y_max + 1, z_max + 1))
while len(current_expansion) > 0:
    next_expansion = set()
    for d in current_expansion:
        for n in NEIGHBORS:
            # Stop at the outer edges of the lava droplet
            neighbor = (min(x_max, max(x_min, d[0] + n[0])),
                        min(y_max, max(y_min, d[1] + n[1])),
                        min(z_max, max(z_min, d[2] + n[2])))

            # This location can be reached by the steam cloud and we haven't been here yet.
            # Add it to the steam cloud and explore it further in the next loop iteration.
            if neighbor not in droplets and neighbor not in steam:
                steam.add(neighbor)
                next_expansion.add(neighbor)
    current_expansion = next_expansion

surface_area_total = 6 * len(droplets)
surface_area_external = 0
for d in droplets:
    for n in NEIGHBORS:
        neighbor = (d[0]+n[0], d[1]+n[1], d[2]+n[2])
        if neighbor in droplets:
            # To approximate the surface area, count the number of sides of each cube
            # that are not immediately connected to another cube.
            surface_area_total -= 1

        # Instead, consider only cube sides that could be reached by the water and steam
        # as the lava droplet tumbles into the pond. The steam will expand to reach as much
        # as possible, completely displacing any air on the outside of the lava droplet
        # but never expanding diagonally.
        if neighbor in steam:
            surface_area_external += 1

print('Part One: The total surface area of the scanned lava droplet is {0}.'.format(surface_area_total))
print('Part Two: The external surface area of the scanned lava droplet is {0}.'.format(surface_area_external))
