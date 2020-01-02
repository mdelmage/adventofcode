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

# https://gist.github.com/endolith/114336/eff2dc13535f139d0d6a2db68597fad2826b53c3
def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)

def periodicity(l):
    factor = 0
    while True:
        factor += 1
        if l[:100] == l[factor:factor + 100]:
            return factor
        if factor > 1000000:
            print "i gave up!"
            return 1

moons = []

# Open input file
filename = "day12.txt"
with open(filename, "r") as f:
    for line in f:
        tokens = line.strip().replace("<", "").replace(">", "").replace(" ", "").replace("x=", "").replace("y=", "").replace("z=", "").split(",")
        moons.append(Moon(int(tokens[0]), int(tokens[1]), int(tokens[2])))
    
    history = [[[] for axis in ['x', 'y', 'z']] for m in moons]
    for step in range(1000000):
        for i in range(len(moons)):
            history[i][0].append(moons[i].pos.x)
            history[i][1].append(moons[i].pos.y)
            history[i][2].append(moons[i].pos.z)

        # Get all combinations of moon pairs
        pairs = list(combinations([0, 1, 2, 3], 2))
        for pair in pairs:
            moon_a = moons[pair[0]]
            moon_b = moons[pair[1]]
            moon_a.gravitate(moon_b)
            moon_b.gravitate(moon_a)

        for moon in moons:
            moon.move()

    factors = set()
    for moon in range(len(history)):
        for axis in range(len(history[moon])):
            factors.add(periodicity(history[moon][axis]))

    print factors
    least_multiple = 1
    for f in factors:
        least_multiple = lcm(least_multiple, f)
    print "Universe repeats in {0} steps!".format(least_multiple)
