#!/usr/bin/env python
# -*- coding: utf-8 -*-

def straight_line_dist(p1, p2):
    return ((((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2) + ((p1[2] - p2[2]) ** 2)) ** 0.5)

# Parse the junction boxes list
with open('day08_input.txt') as f:
    boxes = [tuple([int(n) for n in line.rstrip('\n').split(',')]) for line in f]

# Generate a full mapping of distances between every junction box.
distances = {}
for b1, b2 in [(b1, b2) for b1 in boxes for b2 in boxes if b1 != b2]:
    dist = straight_line_dist(b1, b2)
    distances[dist] = (b1, b2)

connections = 0
circuits = []
answer_part_one = None
answer_part_two = None

# To save on string lights, the Elves would like to focus on connecting pairs of junction boxes
 #that are as close together as possible according to straight-line distance.
for s in sorted(distances):
    b1, b2 = distances[s]
    new_circuit = set([b1, b2])

    # Determine if there are existing circuits this pair would get added to.
    # Remember them, so we can later remove them and add the newly-joined circuit.
    consolidated_circuits = []
    for c in circuits:
        if b1 in c or b2 in c:
            c.add(b1)
            c.add(b2)
            new_circuit |= c
            consolidated_circuits.append(c)

    # Remove the previous circuits and add the new circuit.
    for c in consolidated_circuits:
        circuits.remove(c)
    circuits.append(new_circuit)

    # The Elves were right; they definitely don't have enough extension cables.
    # You'll need to keep connecting junction boxes together until they're all in one large circuit.
    if len(circuits[0]) == len(boxes):
        # The Elves need to know how far those junction boxes are from the wall so they can pick
        # the right extension cable; multiplying the X coordinates of those two junction boxes [...]
        answer_part_two = b1[0] * b2[0]
        break

    connections += 1
    if connections == 1000:
        # Determine the three largest circuits and multiply their sizes together.
        circuit_lengths = []
        for c in circuits:
            circuit_lengths.append(len(c))
        circuit_lengths = sorted(circuit_lengths, reverse=True)
        answer_part_one = circuit_lengths[0] * circuit_lengths[1] * circuit_lengths[2]

# Your list contains many junction boxes; connect together the 1000 pairs of junction boxes
# which are closest together. Afterward, what do you get if you multiply together the sizes
# of the three largest circuits?
print('Part One: The product of the three largest circuits is {0}.'.format(answer_part_one))

# Your list contains many junction boxes; connect together the 1000 pairs of junction boxes which are
# closest together. Afterward, what do you get if you multiply together the sizes of the three largest circuits?
print('Part Two: The product of the three largest circuits is {0}.'.format(answer_part_two))