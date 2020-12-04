#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __builtin__ import True

# Parse the bank list and save each line
with open('day06_input.txt') as f:
    banks = [line.rstrip('\n') for line in f]
    banks = [int(n) for n in banks[0].split()]

bank_history = {}
bank_states = set()
done = False
rebalance_cycles = 0
while not done:
    # The reallocation routine operates in cycles.  
    rebalance_cycles += 1

    # In each cycle, it finds the memory bank with the most blocks
    # (ties won by the lowest-numbered memory bank) and redistributes
    # those blocks among the banks.
    rebalance_bank = 0
    rebalance_count = 0
    for i in range(len(banks)):
        if banks[i] > rebalance_count:
            rebalance_bank = i
            rebalance_count = banks[i]

    # To do this, it removes all of the blocks from the selected bank, then moves to
    # the next (by index) memory bank and inserts one of the blocks. It continues
    # doing this until it runs out of blocks; if it reaches the last memory bank,
    # it wraps around to the first one.
    banks[rebalance_bank] = 0
    while rebalance_count > 0:
        rebalance_bank = (rebalance_bank + 1) % len(banks)
        banks[rebalance_bank] += 1
        rebalance_count -= 1

    # Check if we have a previously-seen state.
    state = tuple(banks)
    if state in bank_states:
        done = True
    else:
        bank_history[state] = rebalance_cycles
        bank_states.add(state)

print 'Part One: %d cycles seen before a duplicate configuration was seen.' % rebalance_cycles
print 'Part Two: state loops every %d cycles.' % (rebalance_cycles - bank_history[state])