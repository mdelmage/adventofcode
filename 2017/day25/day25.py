#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the Turing machine blueprints file
with open('day25_input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

# First line specifies the starting state.
# Format: 'Begin in state X.'
# Extract the state.
state = lines[0][-2:-1]

# Second line specifies the step count.
# Format: 'Perform a diagnostic checksum after 12345 steps.'
# Extract the step count.
step_count = int(lines[1].split()[5])

# Remaining blueprints are groups of ten lines.
# Format:
# <blank line>
# In state X:
#  If the current value is 0:
#    - Write the value 1.
#    - Move one slot to the left.
#    - Continue with state Y.
#  If the current value is 1:
#    - Write the value 0.
#    - Move one slot to the right.
#    - Continue with state Z.
#
# Extract the state instructions.
instructions = {}
for line_num in range(3, len(lines), 10):
    i_state = lines[line_num][-2:-1]
    i_zero_val = int(lines[line_num + 2][-2:-1])
    if lines[line_num + 3].split()[6][:-1] == 'left':
        i_zero_dir = -1
    else:
        i_zero_dir = 1
    i_zero_state = lines[line_num + 4][-2:-1]

    i_one_val = int(lines[line_num + 6][-2:-1])
    if lines[line_num + 7].split()[6][:-1] == 'left':
        i_one_dir = -1
    else:
        i_one_dir = 1
    i_one_state = lines[line_num + 8][-2:-1]

    instructions[(i_state, 0)] = (i_zero_val, i_zero_dir, i_zero_state)
    instructions[(i_state, 1)] = (i_one_val, i_one_dir, i_one_state)

tape = {}
current_slot = 0
current_step = 0
while current_step < step_count:
# Grab the instructions, which are tuples of (write_val, move_dir, new_state).
    (write_val, move_dir, new_state) = instructions[(state, tape.get(current_slot, 0))]

    # Perform the instruction: write, move, update state.
    tape[current_slot] = write_val
    current_slot += move_dir
    state = new_state
    current_step += 1

    # Small optimization here. Delete any zeroes, so we can count the ones
    # just by measuring the length of the tape dict.
    if write_val == 0: del tape[current_slot - move_dir]

print 'Part One: Diagnostic value is {0}.'.format(len(tape))