#!/usr/bin/env python
# -*- coding: utf-8 -*-

MAX_OPERAND = 1000

def calculate_products(program, use_enables=False):
    # It seems like the goal of the program is just to multiply some numbers.
    # It does that with instructions like mul(X,Y), where X and Y are each
    # 1-3 digit numbers.
    products = 0
    mul_enabled = True
    for line in program:
        for i in range(len(line)):
            # There are two new instructions you'll need to handle:
            #
            # The do() instruction enables future mul instructions.
            # The don't() instruction disables future mul instructions.
            if use_enables and line[i:i+4] == 'do()':
                mul_enabled = True
            elif use_enables and line[i:i+7] == 'don\'t()':
                mul_enabled = False
            elif mul_enabled and line[i:i+4] == 'mul(':
                command = line[i+4:].split(')')
                if len(command) > 1:
                    args = command[0].split(',')
                    if len(args) == 2:
                        # We only expect numbers 0-999 here, even though the puzzle instructions
                        # do not explicitly disallow negative numbers.
                        #
                        # We have exactly two tokens; just cast them both to int and then perform
                        # range checks on them. Treat any exception as a corrupted mul() operation
                        # and throw it out.
                        arg1 = MAX_OPERAND
                        arg2 = MAX_OPERAND
                        try:
                            arg1 = int(args[0])
                            arg2 = int(args[1])
                        except: pass
                        if arg1 < MAX_OPERAND and arg2 < MAX_OPERAND:
                            products += arg1 * arg2

    return products

# Parse the corrupted program memory.
with open('day03_input.txt') as f:
    program = [line.rstrip('\n') for line in f]

# Scan the corrupted memory for uncorrupted mul instructions.
# What do you get if you add up all of the results of the multiplications?
print('Part One: The result of all multiplications is {0}.'.format(calculate_products(program)))

# Handle the new instructions; what do you get if you add up all of the results
# of just the enabled multiplications?
print('Part Two: The result of all multiplications is {0}.'.format(calculate_products(program, use_enables=True)))