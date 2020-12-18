#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import prod

# Rather than evaluating multiplication before addition, the operators
# have the same precedence, and are evaluated left-to-right regardless
# of the order in which they appear.
def eval_part_one_rules(expr):
    # Tokenize the expression, and convert the number strings to integers.
    tokens = expr.split()
    tokens = [x if x in ('+', '*') else int(x) for x in tokens]

    # Start with the first token (leftmost number).
    result = tokens[0]

    # Now, going rightward, take pairs of operators/numbers.
    # Evaluate them in order.
    for i in range(len(tokens) / 2):
        if tokens[2*i + 1] == '+':
            result += tokens[2*i + 2]
        else:
            result *= tokens[2*i + 2]

    return result

# Now, addition and multiplication have different precedence levels, but
# they're not the ones you're familiar with. Instead, addition is evaluated
# before multiplication.
def eval_part_two_rules(expr):
    # Tokenize the expression, and convert the number strings to integers.
    tokens = expr.split()
    tokens = [x if x in ('+', '*') else int(x) for x in tokens]

    # Evaluate and reduce the addition tokens first
    while '+' in tokens:
        for i in range(len(tokens)):
            if tokens[i] == '+':
                # We have an expression of the form:
                # i - 2   i - 1    i    i + 1   i + 2
                # .....     x      +      y     .........
                #
                # Remove the middle three tokens, evaluate the sum, and
                # put the result back in the list.
                before = tokens[:max(0,i - 1)]
                sum_result = [tokens[i - 1] + tokens[i + 1]]
                after = tokens[i + 2:]
                tokens = before + sum_result + after
                break

    # Now all we're (possibly) left with is multiplication.
    # Generate the product of 'every other' token (i.e., skip the '*' tokens).
    return prod(tokens[::2])

def solve(problem, eval_func):
    # Hunt for parentheses sub-expressions and reduce them.
    while '(' in problem:
        paren = -1
        for i in range(len(problem)):
            if problem[i] == '(':
                paren = i
            elif problem[i] == ')':
                # We've identified one inner parentheses expression. Evaluate it.
                problem = problem[:paren] + str(eval_func(problem[paren+1:i])) + problem[i+1:]
                break

    # We've reduced the problem so it has no more parentheses.
    # Evaluate it one more time.
    return eval_func(problem)

# Parse the math homework and save each line
with open('day18_input.txt') as f:
    homework = [line.rstrip('\n') for line in f]

answers = []
for problem in homework:
    answers.append(solve(problem, eval_part_one_rules))
print 'Part One: sum of expressions is {0}.'.format(sum(answers))

answers = []
for problem in homework:
    answers.append(solve(problem, eval_part_two_rules))
print 'Part Two: sum of expressions is {0}.'.format(sum(answers))