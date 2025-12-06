#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the math worksheet
with open('day06_input.txt') as f:
    # Cephalopod math doesn't look that different from normal math.
    # The math worksheet (your puzzle input) consists of a list of problems;
    # each problem has a group of numbers that need to be either added (+)
    # or multiplied (*) together.
    problems = [line.rstrip('\n') for line in f]
    operators = problems[-1].split()
    problems = problems[:-1]

digits = []
for row in [n.split() for n in problems]:
    digits.append([int(n) for n in row])

# To check their work, cephalopod students are given the grand total
# of adding together all of the answers to the individual problems.
grand_total_part_one = 0
for problem_number in range(len(operators)):
    operator = operators[problem_number]
    total = 0 if operator == '+' else 1
    # Each problem's numbers are arranged vertically; at the bottom of the problem
    # is the symbol for the operation that needs to be performed. Problems are
    # separated by a full column of only spaces. The left/right alignment of numbers
    # within each problem can be ignored.
    for digit in range(len(problems)):
        if operator == '+':
            total += digits[digit][problem_number]
        else:
            total *= digits[digit][problem_number]
    grand_total_part_one += total

# Cephalopod math is written right-to-left in columns.
# Each number is given in its own column, with the most significant digit
# at the top and the least significant digit at the bottom.
grand_total_part_two = 0
problem = len(operators) - 1
operator = operators[problem]
total = 0 if operator == '+' else 1
for col in range(len(problems[0]) - 1, -1, -1):
    number = 0
    exponent = 0
    for row in range(len(problems) - 1, -1, -1):
        if problems[row][col] != ' ':
            # Add the digit to the number, and increment the tens place.
            number += (10 ** exponent) * int(problems[row][col])
            exponent += 1
    if number == 0:
        # We went through a columnn without any digits, meaning we're at
        # the end of the current problem. Update the grand total, decrement
        # the problem number and set up for another pass.
        grand_total_part_two += total
        problem -= 1
        operator = operators[problem]
        total = 0 if operator == '+' else 1
    else:
        # Our column had at least one digit, so add/multiply the number
        # to our running total.
        if operator == '+':
            total += number
        else:
            total *= number

# Do one last update to the grand total.
grand_total_part_two += total

# Solve the problems on the math worksheet. What is the grand total
# found by adding together all of the answers to the individual problems?
print('Part One: The grand total of all answers is {0}.'.format(grand_total_part_one))

# Solve the problems on the math worksheet again. What is the grand total found
# by adding together all of the answers to the individual problems?
print('Part Two: The grand total of all answers is {0}.'.format(grand_total_part_two))