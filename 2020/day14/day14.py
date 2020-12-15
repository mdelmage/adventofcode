#!/usr/bin/env python
# -*- coding: utf-8 -*-

BIT_CLEAR    = '0'
BIT_SET      = '1'
BIT_FLOATING = 'X'

BIT_WIDTH = 36
BIT_FORMAT_STR = '036b'

def replace_floating_bits(floating_address_str, replacement_strings):
    addresses = []

    # Somewhat-naïve replacement algorithm:
    # Going left to right in the replacement string, hunt down
    # the leftmost floating bit and replace it.
    for s in replacement_strings:
        floated_str = floating_address_str
        for i in range(len(s)):
            float_idx = floated_str.find(BIT_FLOATING)
            floated_str = floated_str[:float_idx] + s[i] + floated_str[float_idx + 1:]

        # Save the generated address as an integer
        addresses.append(int(floated_str, 2))

    return addresses

# Parse the bitmask program and save each line
with open('day14_input.txt') as f:
    program = [line.rstrip('\n') for line in f]

memory = {}

for line in program:
    if 'mask' in line:
        # Don't do stringwise masking; convert to integers and split out
        # the AND and OR parts of the mask.
        mask = line.split('mask = ')[1]
        and_mask = int(mask.replace(BIT_FLOATING, BIT_SET), 2)
        or_mask = int(mask.replace(BIT_FLOATING, BIT_CLEAR), 2)
    else:
        tokens = line.replace('mem[', '').replace('] = ', ' ').split()
        register = int(tokens[0])
        value = int(tokens[1])

        # The current bitmask is applied to values immediately before they are written
        # to memory: a 0 or 1 overwrites the corresponding bit in the value, while an X
        # leaves the bit in the value unchanged.
        masked_value = (value & and_mask) | or_mask
        memory[register] = masked_value

# To initialize your ferry's docking program, you need the sum of all values left in memory
# after the initialization program completes. (The entire 36-bit address space begins
# initialized to the value 0 at every address.)
print 'Part One: sum of all values in memory is {0}.'.format(sum(memory.values()))

memory = {}

for line in program:
    if 'mask' in line:
        mask = line.split('mask = ')[1]
    else:
        tokens = line.replace('mem[', '').replace('] = ', ' ').split()
        address = format(int(tokens[0]), BIT_FORMAT_STR)
        value = int(tokens[1])

        # A version 2 decoder chip doesn't modify the values being written at all.
        # Instead, it acts as a memory address decoder. Immediately before a value is written
        # to memory, each bit in the bitmask modifies the corresponding bit of the
        # destination memory address in the following way:
        #
        # If the bitmask bit is 0, the corresponding memory address bit is unchanged.
        # If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
        # If the bitmask bit is X, the corresponding memory address bit is floating.
        floating_address = ''
        for i in range(BIT_WIDTH):
            if mask[i] == BIT_FLOATING:
                floating_address += BIT_FLOATING
            elif mask[i] == BIT_SET:
                floating_address += BIT_SET
            elif mask[i] == BIT_CLEAR:
                floating_address += address[i]

        # Now we have an address with floating bits that match the version 2 spec.
        # Generate all possible permutations of the floating bits.
        floating_bit_strings = []
        floating_bit_count = mask.count(BIT_FLOATING)
        for i in range(1 << floating_bit_count):
            floating_bit_strings.append(format(i, BIT_FORMAT_STR)[-floating_bit_count:])

        # Then, inject these permutations into the floating bits.
        # The result is a list of all registers that we're writing to.
        registers = replace_floating_bits(floating_address, floating_bit_strings)
    
        # Perform the write(s).
        for r in registers:
            memory[r] = value

print 'Part Two: sum of all values in memory is {0}.'.format(sum(memory.values()))
