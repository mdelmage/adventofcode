#!/usr/bin/python

from itertools import combinations 

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, v): 
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v): 
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

class Moon:
    def __init__(self, x, y, z):
        self.pos = Vector(x, y, z)
        self.vel = Vector(0, 0, 0)

    def __str__(self):
        return "pos=<x={0:3}, y={1:3}, z={2:3}>, vel=<x={3:3}, y={4:3}, z={5:3}>".format(self.pos.x,
                                                                                         self.pos.y,
                                                                                         self.pos.z,
                                                                                         self.vel.x,
                                                                                         self.vel.y,
                                                                                         self.vel.z)
    def __repr__(self):
        return self.__str__()

    @staticmethod
    def attraction(pos):
        if pos > 0:
            return -1
        elif pos < 0:
            return 1
        else:
            return 0

    def gravitate(self, neighbor):
        delta = self.pos - neighbor.pos
        self.vel.x += Moon.attraction(delta.x)
        self.vel.y += Moon.attraction(delta.y)
        self.vel.z += Moon.attraction(delta.z)

    def move(self):
        self.pos += self.vel


moons = []

# Open input file
filename = "day12.txt"
with open(filename, "r") as f:
    for line in f:
        tokens = line.strip().replace("<", "").replace(">", "").replace(" ", "").replace("x=", "").replace("y=", "").replace("z=", "").split(",")
        moons.append(Moon(int(tokens[0]), int(tokens[1]), int(tokens[2])))
    
    print "Step 0:"
    for moon in moons:
        print moon

    for step in range(1000):

        # Get all combinations of moon pairs
        pairs = list(combinations([0, 1, 2, 3], 2))
        for pair in pairs:
            moon_a = moons[pair[0]]
            moon_b = moons[pair[1]]
            moon_a.gravitate(moon_b)
            moon_b.gravitate(moon_a)
        print "Step {0}:".format(step + 1)
        for moon in moons:
            moon.move()
            print moon

    energy = 0
    for moon in moons:
        energy += (abs(moon.pos.x) + abs(moon.pos.y) + abs(moon.pos.z)) * (abs(moon.vel.x) + abs(moon.vel.y) + abs(moon.vel.z))
    print "Total energy = {0}".format(energy)