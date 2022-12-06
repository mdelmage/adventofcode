#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the starting stacks and rearrangement procedure file
with open('day05_input.txt') as f:
    manifest = [line.rstrip('\n') for line in f]

line = 0
stacks_done = False
num_stacks = int((len(manifest[line]) + 1) / 4)
stacks = [[] for i in range(num_stacks)]
while not stacks_done:
    if len(manifest[line]) == 0:
        # Find the split-point between the stacks diagram and the move instructions
        stacks_done = True
    else:
        # Append crates to the bottom of the stack, since we're parsing downwards
        for stack in range(num_stacks):
            crate = manifest[line][stack * 4 + 1]
            if crate.isalpha(): stacks[stack].append(crate)

    line += 1

while line < len(manifest):
    # Then, the rearrangement procedure is given. In each step of the procedure,
    # a quantity of crates is moved from one stack to a different stack.
    (move_count, source, target) = [int(i) for i in manifest[line].replace('move ', '').replace('from ', '').replace('to ', '').split(' ')]

    # Account for 1-indexing of stack names
    source -= 1
    target -= 1

    for c in range(move_count):
        # Move crates between stacks, using LIFO (stack) rules
        stacks[target].insert(0, stacks[source].pop(0))

    line += 1

# The Elves just need to know which crate will end up on top of each stack.
phrase = [stacks[i][0] for i in range(len(stacks))]
print('Part One: message at the top of the stacks is {0}.'.format(''.join(phrase)))

# Redo the entire stacks setup from the manifest, because I'm lazy
line = 0
stacks_done = False
num_stacks = int((len(manifest[line]) + 1) / 4)
stacks = [[] for i in range(num_stacks)]
while not stacks_done:
    if len(manifest[line]) == 0:
        # Find the split-point between the stacks diagram and the move instructions
        stacks_done = True
    else:
        # Append crates to the bottom of the stack, since we're parsing downwards
        for stack in range(num_stacks):
            crate = manifest[line][stack * 4 + 1]
            if crate.isalpha(): stacks[stack].append(crate)

    line += 1

while line < len(manifest):
    # Then, the rearrangement procedure is given. In each step of the procedure,
    # a quantity of crates is moved from one stack to a different stack.
    (move_count, source, target) = [int(i) for i in manifest[line].replace('move ', '').replace('from ', '').replace('to ', '').split(' ')]

    # Account for 1-indexing of stack names
    source -= 1
    target -= 1

    # Some mud was covering the writing on the side of the crane, and you quickly wipe it away.
    # The crane isn't a CrateMover 9000 - it's a CrateMover 9001.
    #
    # The CrateMover 9001 is notable for many new and exciting features: air conditioning,
    # leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

    # Move crates between stacks, using FIFO (queue) rules
    stacks[target] = stacks[source][:move_count] + stacks[target]
    stacks[source] = stacks[source][move_count:]

    line += 1

# After the rearrangement procedure completes, what crate ends up on top of each stack?
phrase = [stacks[i][0] for i in range(len(stacks))]
print('Part Two: message at the top of the stacks is {0}.'.format(''.join(phrase)))
