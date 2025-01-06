#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The map shows the current position of the guard with ^
# (to indicate the guard is currently facing up from the perspective of the map).
GUARD = '^'

# Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.
OBSTRUCTION = '#'

SPACE = '.'

# Lab guards in 1518 follow a very strict patrol protocol which involves
# repeatedly following these steps:
#
# If there is something directly in front of you, turn right 90 degrees.
# Otherwise, take a step forward.
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def loop_detected(new_obstruction):
    # Guard initially faces up ('^').
    current_dir = 0

    guard_pos = guard_pos_orig
    patrolled = set()
    while True:
        # Calculate the potential next guard position. It could be blocked by an obstruction.
        guard_pos_next = (guard_pos[0] + DIRECTIONS[current_dir][0], guard_pos[1] + DIRECTIONS[current_dir][1])

        # Next position isn't in the patrol map -- no loop detected!
        if guard_pos_next not in patrol_map: return False

        # If there is something directly in front of you, turn right 90 degrees.
        # Otherwise, take a step forward.
        if patrol_map[guard_pos_next] == OBSTRUCTION or guard_pos_next == new_obstruction:
            current_dir = (current_dir + 1) % len(DIRECTIONS)
        else:
            guard_pos = guard_pos_next
            if (guard_pos, current_dir) in patrolled: return True
            patrolled.add((guard_pos, current_dir))

# Parse the patrol map and locate the guard.
with open('day06_input.txt') as f:
    p = [line.rstrip('\n') for line in f]

    # Convert from list to dict for ease of processing.
    patrol_map = {}
    for row in range(len(p)):
        for col in range(len(p[row])):
            patrol_map[(col, row)] = p[row][col]

            # Note the guard's position when we see it.
            if p[row][col] == GUARD:
                guard_pos_orig = (col, row)


# Guard initially faces up ('^').
current_dir = 0

# Predict the path of the guard. How many distinct positions will the guard visit
# before leaving the mapped area?
patrolled = set()
guard_pos = guard_pos_orig
while(True):
    # Calculate the potential next guard position. It could be blocked by an obstruction.
    guard_pos_next = (guard_pos[0] + DIRECTIONS[current_dir][0], guard_pos[1] + DIRECTIONS[current_dir][1])

    # Next position isn't in the patrol map -- we're done!
    if guard_pos_next not in patrol_map: break

    # If there is something directly in front of you, turn right 90 degrees.
    # Otherwise, take a step forward.
    if patrol_map[guard_pos_next] == OBSTRUCTION:
        current_dir = (current_dir + 1) % len(DIRECTIONS)
    else:
        guard_pos = guard_pos_next
        patrolled.add(guard_pos)

print('Part One: Guard will visit {0} distinct positions.'.format(len(patrolled)))

# To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible
# positions for such an obstruction. The new obstruction can't be placed at the guard's starting position -
# the guard is there right now and would notice.
loops_created = 0
for new_obstruction in [l for l in patrolled if l != guard_pos_orig]:
    if loop_detected(new_obstruction): loops_created += 1

# You need to get the guard stuck in a loop by adding a single new obstruction.
# How many different positions could you choose for this obstruction?
print('Part Two: Adding obstructions in {0} positions would cause loops.'.format(loops_created))