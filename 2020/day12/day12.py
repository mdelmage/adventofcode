#!/usr/bin/env python
# -*- coding: utf-8 -*-

class coord(object):    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, c):
        return coord(self.x + c.x, self.y + c.y)

    def __sub__(self, c):
        return coord(self.x - c.x, self.y - c.y)

    def __eq__(self,c):
        return (self.x == c.x and self.y == c.y)

    def __mul__(self, n):
        return coord(self.x * n, self.y * n)

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def dist(self):
        return (abs(self.x) + abs(self.y))

    def rotate(self, angle):
        # Naïve rotation algorithm: rotate right, N times.
        n = ((angle + 360) / 90) % len(HEADINGS)
        for i in range(n):
            old_x = self.x
            old_y = self.y
            self.x = old_y
            self.y = -old_x

CMD_NORTH   = 'N'
CMD_SOUTH   = 'S'
CMD_EAST    = 'E'
CMD_WEST    = 'W'
CMD_LEFT    = 'L'
CMD_RIGHT   = 'R'
CMD_FORWARD = 'F'

EAST  = 0
SOUTH = 1
WEST  = 2
NORTH = 3

HEADINGS = [coord( 1,  0), # East
            coord( 0, -1), # South
            coord(-1,  0), # West
            coord( 0,  1)] # North

# The ship starts by facing east.
heading = coord(1, 0)

# Start at the origin position.
position = coord(0, 0)

# Parse the navigation instructions and save each line
with open('day12_input.txt') as f:
    commands = []
    directions = [line.rstrip('\n') for line in f]
    for line in directions:
        command = line[0]
        value = int(line[1:])
        commands.append((command, value))

# The navigation instructions (your puzzle input) consists of a sequence of single-character
# actions paired with integer input values. After staring at them for a few minutes,
# you work out what they probably mean:
#
# Action N means to move north by the given value.
# Action S means to move south by the given value.
# Action E means to move east by the given value.
# Action W means to move west by the given value.
# Action L means to turn left the given number of degrees.
# Action R means to turn right the given number of degrees.
# Action F means to move forward by the given value in the direction the ship is currently facing.
for (command, value) in commands:
    if   command == CMD_NORTH:   position += (HEADINGS[NORTH] * value)
    elif command == CMD_SOUTH:   position += (HEADINGS[SOUTH] * value)
    elif command == CMD_EAST:    position += (HEADINGS[EAST]  * value)
    elif command == CMD_WEST:    position += (HEADINGS[WEST]  * value)
    elif command == CMD_LEFT:    heading.rotate(-value)
    elif command == CMD_RIGHT:   heading.rotate(value)
    elif command == CMD_FORWARD: position += (heading * value)

print 'Part One: Manhattan distance from origin is {0}.'.format(position.dist())

# The waypoint starts 10 units east and 1 unit north relative to the ship.
waypoint = coord(10, 1)

# Reset the ship to the origin.
position = coord(0, 0)

# Before you can give the destination to the captain, you realize that the actual
# action meanings were printed on the back of the instructions the whole time.
#
# Almost all of the actions indicate how to move a waypoint which is relative
# to the ship's position:
#
# Action N means to move the waypoint north by the given value.
# Action S means to move the waypoint south by the given value.
# Action E means to move the waypoint east by the given value.
# Action W means to move the waypoint west by the given value.
# Action L means to rotate the waypoint around the ship left (counter-clockwise)the given number of degrees.
# Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
# Action F means to move forward to the waypoint a number of times equal to the given value.
for (command, value) in commands:
    if   command == CMD_NORTH:   waypoint += (HEADINGS[NORTH] * value)
    elif command == CMD_SOUTH:   waypoint += (HEADINGS[SOUTH] * value)
    elif command == CMD_EAST:    waypoint += (HEADINGS[EAST]  * value)
    elif command == CMD_WEST:    waypoint += (HEADINGS[WEST]  * value)
    elif command == CMD_LEFT:    waypoint.rotate(-value)
    elif command == CMD_RIGHT:   waypoint.rotate(value)
    elif command == CMD_FORWARD: position += (waypoint * value)

print 'Part Two: Manhattan distance from origin is {0}.'.format(position.dist())