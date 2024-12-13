#!/usr/bin/env python
# -*- coding: utf-8 -*-

def solve_linear(a, b, c):
    # Linear math follows. Don't try to follow too much.
    # Basically, solve the linear equations:
    # Ax + By = C
    # Dx + Ey = F
    solution_a = (c[1] - b[1]*c[0]/b[0])/(a[1] - b[1]*a[0]/b[0])
    solution_b = (c[1] - a[1] * solution_a) / b[1]
    return ((solution_a, solution_b))

# Parse the list of every machine's button behavior and prize location.
with open('day13_input.txt') as f:
    g = [line.rstrip('\n') for line in f] + ['']
    prizes = []
    for sublist in range(len(g) // 4):
        # With a little experimentation, you figure out that each machine's buttons are configured to move the claw
        # a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis)
        # each time that button is pressed.
        #
        # Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize
        # on both the X and Y axes.
        button_a = [int(n) for n in g[sublist * 4].replace('Button A: X+', '').replace(', Y+', ' ').split()]
        button_b = [int(n) for n in g[sublist * 4 + 1].replace('Button B: X+', '').replace(', Y+', ' ').split()]
        prize = [int(n) for n in g[sublist * 4 + 2].replace('Prize: X=', '').replace(', Y=', ' ').split()]
        prizes.append((button_a, button_b, prize))

tokens_total_part_one = 0
tokens_total_part_two = 0
for (button_a, button_b, target) in prizes:
    (a, b) = solve_linear(button_a, button_b, target)

    # We are simulating button presses, so only whole-number solutions are correct.
    # Round and re-verify.
    a = round(a)
    b = round(b)
    if button_a[0]*a + button_b[0]*b == target[0] and button_a[1]*a + button_b[1]*b == target[1]:
        # It costs 3 tokens to push the A button and 1 token to push the B button.
        tokens_total_part_one += 3*a + b

    # As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be.
    # Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000
    # higher on both the X and Y axis!
    target = (target[0] + 10000000000000, target[1] + 10000000000000)
    (a, b) = solve_linear(button_a, button_b, target)

    # We are simulating button presses, so only whole-number solutions are correct.
    # Round and re-verify.
    a = round(a)
    b = round(b)
    if button_a[0]*a + button_b[0]*b == target[0] and button_a[1]*a + button_b[1]*b == target[1]:
        # It costs 3 tokens to push the A button and 1 token to push the B button.
        tokens_total_part_two += 3*a + b

# Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend
# to win all possible prizes?
print('Part One: Fewest tokens to win all prizes is {0}.'.format(tokens_total_part_one))

# Using the corrected prize coordinates, figure out how to win as many prizes as possible.
# What is the fewest tokens you would have to spend to win all possible prizes?
print('Part Two: Fewest tokens to win all prizes is {0}.'.format(tokens_total_part_two))
