#!/usr/bin/env python
# -*- coding: utf-8 -*-

OP_ADDITION       = 1
OP_MULTIPLICATION = 2
OP_CONCATENATION  = 3

def evaluate_expression(correct_answer, operands, operations):
    possible_answers = [operands[0]]
    operands = operands[1:]

    # Operators are always evaluated left-to-right, not according to precedence rules.
    # Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle,
    # you can see elephants holding two different types of operators: add (+) and multiply (*).
    while len(operands) > 0:
        possible_answers_next = []
        for answer in possible_answers:
            if OP_ADDITION in operations: possible_answers_next.append(answer + operands[0])
            if OP_MULTIPLICATION in operations: possible_answers_next.append(answer * operands[0])

            # The concatenation operator (||) combines the digits from its left and right inputs into a single number.
            if OP_CONCATENATION in operations: possible_answers_next.append(int(str(answer) + str(operands[0])))
        operands = operands[1:]
        possible_answers = possible_answers_next

    # The engineers just need the total calibration result, which is the sum of the test values
     #from just the equations that could possibly be true.
    for answer in possible_answers:
        if answer == correct_answer: return True

    return False

# Parse the calibration equations.
with open('day07_input.txt') as f:
    equations = [[int(n) for n in line.rstrip('\n').replace(':', '').split()] for line in f]

total_calibration_result_part_one = 0
total_calibration_result_part_two = 0
for equation in equations:
    correct_answer = equation[0]
    operands = equation[1:]
    if evaluate_expression(correct_answer, operands, [OP_ADDITION, OP_MULTIPLICATION]):
        total_calibration_result_part_one += correct_answer
    if evaluate_expression(correct_answer, operands, [OP_ADDITION, OP_MULTIPLICATION, OP_CONCATENATION]):
        total_calibration_result_part_two += correct_answer

# Determine which equations could possibly be true. What is their total calibration result?
print('Part One: Total calibration result is {0}.'.format(total_calibration_result_part_one))

# Using your new knowledge of elephant hiding spots, determine which equations could possibly be true.
# What is their total calibration result?
print('Part Two: Total calibration result with concatenation is {0}.'.format(total_calibration_result_part_two))
