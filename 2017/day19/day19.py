#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dictionaries that know how to change velocity left or right
left_turn = { (1, 0) : (0, -1),
              (0, 1) : (1, 0),
              (-1, 0): (0, 1),
              (0, -1): (-1, 0)}


right_turn = { (1, 0) : (0, 1),
               (0, 1) : (-1, 0),
               (-1, 0): (0, -1),
               (0, -1): (1, 0)}

# Parse the map file
with open('day19_input.txt') as f:
    diagram = [line.rstrip('\n')for line in f]

pos = None
vel = (0, 1)
route_map = {}
route_string = ''
route_len = 1

# Extract any non-space characters into our route map
y = 0
for line in diagram:
    for x in range(len(line)):
        if line[x] != ' ':
            route_map[(x, y)] = line[x]
            if not pos: pos = (x, y)
    y += 1

# Traverse the route until we can't go left, forward or right
while pos is not None:
    # We found a route letter; save it
    if route_map[pos].isalpha(): route_string += route_map[pos]

    # Pre-calculate what left/straight/right would look like
    vel_left = left_turn[vel]
    vel_right = right_turn[vel]
    pos_ahead = (pos[0] + vel[0], pos[1] + vel[1])
    pos_left = (pos[0] + vel_left[0], pos[1] + vel_left[1])
    pos_right = (pos[0] + vel_right[0], pos[1] + vel_right[1])

    # Prefer straight ahead, but fall back to left/right turns
    if pos_ahead in route_map:
        pos = pos_ahead
    elif pos_left in route_map:
        pos = pos_left
        vel = vel_left
    elif pos_right in route_map:
        pos = pos_right
        vel = vel_right
    else:
        pos = None
        route_len -= 1
    route_len += 1

print 'Part One: Letters seen were {0}.'.format(route_string)
print 'Part Two: Scan length was {0}.'.format(route_len)