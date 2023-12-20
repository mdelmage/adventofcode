#!/usr/bin/env python
# -*- coding: utf-8 -*-

ACCEPT = 'A'
REJECT = 'R'

# Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1
# to a maximum of 4000. Of all possible distinct combinations of ratings, your job is to
# figure out which ones will be accepted.
MIN = 1
MAX = 4000
class Rating:
    def __init__(self):
        self.range = {'x': (MIN, MAX),
                      'm': (MIN, MAX),
                      'a': (MIN, MAX),
                      's': (MIN, MAX)}

    def size(self):
        # Invalid range -- return 0.
        if self.range['x'][0] > self.range['x'][1]: return 0
        if self.range['m'][0] > self.range['m'][1]: return 0
        if self.range['a'][0] > self.range['a'][1]: return 0
        if self.range['s'][0] > self.range['s'][1]: return 0

        # Valid range -- return product of all sub-ranges.
        return (self.range['x'][1] - self.range['x'][0] + 1) * \
               (self.range['m'][1] - self.range['m'][0] + 1) * \
               (self.range['a'][1] - self.range['a'][0] + 1) * \
               (self.range['s'][1] - self.range['s'][0] + 1)

    # Apply a simple expression and return the resulting rating range.
    # Optionally, apply an inversion to the expression (return the 'else' clause).
    #
    # This operation is not self-modifying.
    def eval(self, expr, invert=False):
        r = Rating()
        r.range['x'] = self.range['x']
        r.range['m'] = self.range['m']
        r.range['a'] = self.range['a']
        r.range['s'] = self.range['s']

        category = expr[0]
        val = int(expr[2:])
        if invert:
            if expr[1] == '>':
                # Greater than ('>') is inverted to become less-than-or-equal-to ('<=')
                r.range[category] = (r.range[category][0], min(r.range[category][1], val))
            else:
                # Less than ('<') is inverted to become greater-than-or-equal-to ('>=')
                r.range[category] = (max(r.range[category][0], val), r.range[category][1])
        else:
            if expr[1] == '>':
                r.range[category] = (max(r.range[category][0], val + 1), r.range[category][1])
            else:
                r.range[category] = (r.range[category][0], min(r.range[category][1], val - 1))
        return r

def validate(workflow='in', rating=Rating()):
    if workflow == ACCEPT:
        return rating.size()
    if workflow == REJECT:
        return 0

    # Go through all steps in this workflow and determine the number of valid ratings.
    valid_count = 0
    for step in range(len(workflows[workflow])):
        rule = workflows[workflow][step]

        if ':' in rule:
            # The rule is an expression. Parse it and recurse into it!
            expr = rule.split(':')[0]
            workflow_new = rule.split(':')[1]
            valid_count += validate(workflow_new, rating.eval(expr))

            # For the rest of this workflow, consider the rating as if it did NOT pass the expression.
            # This persists for the subsequent processing at this level, and all recursion levels below it.
            rating = rating.eval(expr, invert=True)
        else:
            # The rule is a workflow. Recurse into it!
            workflow_new = rule
            valid_count += validate(workflow_new, rating)

    return valid_count

# Parse the workflows and part ratings.
with open('day19_input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

    # Find the blank line and split the input into workflows and parts.
    split_line = [n for n in range(len(lines)) if lines[n] == ''][0]
    w = lines[:split_line]
    p = lines[split_line + 1:]

    # Parse the workflow strings. Yeah, it's ugly.
    workflows = {ACCEPT: [], REJECT: []}
    for workflow in w:
        workflow = workflow.rstrip('}')
        split = workflow.find('{')
        name = workflow[:split]
        flow = workflow[split + 1:].split(',')
        workflows[name] = flow

    # Parse the parts strings. Yeah, it's ugly. But less ugly. Kinda.
    parts = []
    for part in p:
        spec = {}
        for attrib in part.lstrip('{').rstrip('}').split(','):
            (name, val) = attrib.split('=')
            spec[name] = int(val)
        parts.append(spec)

sum_parts = 0
for part in parts:
    r = Rating()
    for category in ['x', 'm', 'a', 's']:
        r.range[category] = (part[category], part[category])

    # If this part was validated, sum up the ratings for each of its categories.
    if validate(rating=r) == 1:
        s = sum([part[x] for x in part])
        sum_parts += s

# Sort through all of the parts you've been given; what do you get if you add together
# all of the rating numbers for all of the parts that ultimately get accepted?
print('Part One: Sum of ratings for all accepted parts is {0}.'.format(sum_parts))

# Consider only your list of workflows; the list of part ratings that the Elves wanted
# you to sort is no longer relevant. How many distinct combinations of ratings will be
# accepted by the Elves' workflows?
print('Part One: Number of combinations of ratings accepted is {0}.'.format(validate()))