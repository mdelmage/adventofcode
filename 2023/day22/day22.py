#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Brick:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

    # Returns the top Z-height of this brick.
    # Cheat a little by noticing that the Z axes of our inputs
    # have already been sorted.
    def bottom(self):
        return self.pos1[2]

    # Returns the bottom Z-height of this brick.
    # Cheat a little by noticing that the Z axes of our inputs
    # have already been sorted.
    def top(self):
        return self.pos2[2]

    # Returns the range of this brick in the X-axis.
    def x_range(self):
        return range(self.pos1[0], self.pos2[0] + 1)

    # Returns the range of this brick in the Y-axis.
    def y_range(self):
        return range(self.pos1[1], self.pos2[1] + 1)

    # Returns whether another brick is directly under us, with an overlapping
    # X/Y area (at least one tile), thereby supporting us.
    def supported_by(self, neighbor):
        # We should only call this function on bricks exactly one level apart.
        # We'll return false even if they're touching horizontally.
        if self.bottom() != neighbor.top() + 1:
            return False

        # If the X and Y axes overlap (and we already proved Z axes are correct),
        # then the neighboring brick supports us.
        #
        # Cheat a little by noticing that the X and Y axes of our inputs
        # have already been sorted.
        if self.pos1[0] > neighbor.pos2[0]: return False
        if self.pos2[0] < neighbor.pos1[0]: return False
        if self.pos1[1] > neighbor.pos2[1]: return False
        if self.pos2[1] < neighbor.pos1[1]: return False

        return True

    # Return whether this brick is supported, e.g., would it fall or not
    # if we ran our simulation?
    def supported(self):
        # The ground -- so supportive.
        if self.bottom() == 1: return True

        for neighbor in bricks:
            if self.supported_by(neighbor):
                # Supported! Bail out early.
                return True

        # We didn't find any support for this brick.
        return False

    def sole_supporter(self):
        sole = False

        # Remove ourselves from the pile of bricks and see if any bricks above us become unsupported.
        bricks.remove(self)
        for neighbor in [b for b in bricks if self.top() + 1 == b.bottom()]:
            if not neighbor.supported():
                # We found a brick that was unsupported after we removed this brick.
                # It must be the sole supporter of this brick, and possibly others!
                # Bail out early.
                sole = True
                break

        # Regardless of the result, put us back in the pile.
        bricks.append(self)
        return sole

    def drop(self):
        dropped = False
        if not self.supported():
            # We're definitely dropping, since we found that we were unsupported.
            dropped = True

            # Instead of dropping iteratively and checking if we're done, just calculate how far the drop will be.
            # Do this by finding the highest support block below us (e.g., overlaps us in the X, Y plane),
            # and then positioning ourselves right above that block.
            highest_support = 0
            for loc in [(x, y) for x in self.x_range() for y in self.y_range()]:
                supports = [b.top() for b in xy_lookup[loc] if b != self and b.top() < self.bottom()]
                highest_support = max(highest_support, max([0] + supports))

            # Move ourself right above that support block.
            adjustment = self.bottom() - highest_support
            self.pos1 = [self.pos1[0], self.pos1[1], self.pos1[2] - adjustment + 1]
            self.pos2 = [self.pos2[0], self.pos2[1], self.pos2[2] - adjustment + 1]

        return dropped

# Do initial setup of the simulation.
# This is a function because we're going to call it repeatedly to test various scenarios.
def setup():
    global bricks
    global z_lookup
    global xy_lookup

    # Main list of which bricks we have.
    bricks = []

    # Lookup table (hashmap) #1: Bricks by bottom height.
    # This helps us drop the bricks efficiently and correctly.
    z_lookup = {}

    # Lookup table (hashmap) #2: Bricks by X, Y coordinate.
    # This helps us find supporting bricks efficiently.
    xy_lookup = {}

    for r in rows:
        (pos1, pos2) = r.split('~')
        pos1 = [int(n) for n in pos1.split(',')]
        pos2 = [int(n) for n in pos2.split(',')]
        brick = Brick(pos1, pos2)

        # Add this brick to the main list.
        bricks.append(brick)

        # Set up the Z lookup.
        z = brick.bottom()
        if z not in z_lookup: z_lookup[z] = []
        z_lookup[z].append(brick)

        # Set up the X, Y lookups.
        for xy in [(x, y) for x in brick.x_range() for y in brick.y_range()]:
            if xy not in xy_lookup: xy_lookup[xy] = []
            xy_lookup[xy].append(brick)

    # Because the snapshot was taken while the bricks were still falling, some bricks
    # will still be in the air; you'll need to start by figuring out where they will end up.
    #
    # (Drop the bricks from bottom-to-top so that nothing ends up stopping in mid-air.)
    for z in sorted(z_lookup.keys()):
        for brick in z_lookup[z]:
            brick.drop()

# Parse the bricks snapshot.
with open('day22_input.txt') as f:
    rows = [line.rstrip('\n') for line in f]
    setup()

# Figure how the blocks will settle based on the snapshot. Once they've settled,
# consider disintegrating a single brick; how many bricks could be safely chosen as the one to get disintegrated?
can_be_disintegrated = 0
for brick in [b for b in bricks]:
    if not brick.sole_supporter(): can_be_disintegrated += 1
print('Part One: The number of bricks that could be safely disintegrated is {0}.'.format(can_be_disintegrated))

# You'll need to figure out the best brick to disintegrate. For each brick, determine how many
# other bricks would fall if that brick were disintegrated.
falling_bricks = 0
for i in range(len(bricks)):
    # Reset our state by performing initial setup again.
    setup()

    brick = bricks[i]

    # "Disintegrate" the brick by:

    # 1. Removing the X, Y lookups.
    for xy in [(x, y) for x in brick.x_range() for y in brick.y_range()]:
        xy_lookup[xy].remove(brick)

    # 2. Removing the brick from the main list.
    del bricks[i]

    # Now see how many bricks fall after disintegrating this one.
    for z in sorted(z_lookup.keys()):
        for brick in z_lookup[z]:
            if brick.drop(): falling_bricks += 1

# For each brick, determine how many other bricks would fall if that brick were disintegrated.
# What is the sum of the number of other bricks that would fall?
print('Part Two: The number of bricks that would fall is {0}.'.format(falling_bricks))