#!/usr/bin/env python
# -*- coding: utf-8 -*-

A_BUNCH_OF_ITERATIONS = 100

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '<{0},{1},{2}>'.format(self.x, self.y, self.z)

    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y, self.z + p.z)

    def dist(self, p):
        # Measure this using the Manhattan distance, which in this situation is simply
        # the sum of the absolute values of a particle's X, Y, and Z position.
        return abs(self.x - p.x) + abs(self.y - p.y) + abs(self.z - p.z)

    def as_tuple(self):
        return (self.x, self.y, self.z)

class Particle:
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a

    def __str__(self):
        return 'p={0}, v={1}, a={2}'.format(self.p, self.v, self.a)

    def dist(self, p):
        return self.p.dist(p)

    def step(self):
        # Each tick, all particles are updated simultaneously. A particle's properties are updated in the following order:
        # Increase the X velocity by the X acceleration.
        # Increase the Y velocity by the Y acceleration.
        # Increase the Z velocity by the Z acceleration.
        # Increase the X position by the X velocity.
        # Increase the Y position by the Y velocity.
        # Increase the Z position by the Z velocity.
        self.v += self.a
        self.p += self.v

# Parse the map file
with open('day20_input.txt') as f:
    str_particles = [line.rstrip('\n').split(', ') for line in f]

particles = []
origin = Point(0, 0, 0)
for particle in str_particles:
    # Ugly string parsing. Get lists of coordinates for each attribute.
    p = [int(x) for x in particle[0][3:].strip()[:-1].split(',')]
    v = [int(x) for x in particle[1][3:].strip()[:-1].split(',')]
    a = [int(x) for x in particle[2][3:].strip()[:-1].split(',')]

    # Convert lists to Points
    p = Point(p[0], p[1], p[2])
    v = Point(v[0], v[1], v[2])
    a = Point(a[0], a[1], a[2])

    particles.append(Particle(p, v, a))

# Because of seemingly tenuous rationale involving z-buffering, the GPU would like to know
# which particle will stay closest to position <0,0,0> in the long term. Measure this using
# the Manhattan distance, which in this situation is simply the sum of the absolute values
# of a particle's X, Y, and Z position.
lowest_accel = None
lowest_accel_particle = None
for i in range(len(particles)):
    # This problem can be simplified to "find the particle with the lowest overall acceleration".
    dist_a = particles[i].a.dist(origin)
    if lowest_accel is None or dist_a < lowest_accel:
        lowest_accel = dist_a
        lowest_accel_particle = i

print 'Part One: Particle {0} will stay closest to the origin in the long-term.'.format(lowest_accel_particle)

# There is probably a programmatic way to decide when we're done, but for this implementation,
# just keep stepping until we can be reasonably sure that no more collisions will occur.
iteration = 0
while iteration < A_BUNCH_OF_ITERATIONS:
    closest_particle = None
    closest_distance = None
    particle_locations = {}
    for i in range(len(particles)):
        particles[i].step()
        loc = particles[i].p.as_tuple()

        # Build up a histogram of locations that particles are at.
        if loc not in particle_locations:
            particle_locations[loc] = [particles[i]]
        else:
            particle_locations[loc].append(particles[i])

    # Now check the histogram and remove particles where there are duplicates.
    for loc in particle_locations:
        if len(particle_locations[loc]) > 1:
            for p in particle_locations[loc]:
                particles.remove(p)

    iteration += 1

print 'Part Two: {0} particles remain after all collisisons.'.format(len(particles))