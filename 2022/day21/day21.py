#!/usr/bin/env python
# -*- coding: utf-8 -*-

OP_CONSTANT = '.'
OP_ADD      = '+'
OP_SUBTRACT = '-'
OP_MULTIPLY = '*'
OP_DIVIDE   = '/'

def build(monkeys, exclude=None):
    unsolved = {}
    solved = []
    for m in monkeys:
        (name, job) = m.split(': ')
        job = job.split(' ')
        if len(job) > 1:
            operand1 = job[0]
            operand2 = job[2]
            operation = job[1]
            unsolved[name] = Monkey(name, operation, operand1, operand2)
        elif name != exclude:
            solved.append(Monkey(name, OP_CONSTANT, int(job[0])))

    return unsolved, solved

def reduce(unsolved, solved):
    # Each monkey is given a job: either to yell a specific number or to yell
    # the result of a math operation. All of the number-yelling monkeys know
    # their number from the start; however, the math operation monkeys need to wait
    # for two other monkeys to yell a number, and those two other monkeys might
    # also be waiting on other monkeys.
    #
    # Your job is to work out the number the monkey named root will yell before
    # the monkeys figure it out themselves.
    while len(solved) > 0:
        m = solved.pop()
        removal_list = []
        for name in unsolved:
            u = unsolved[name]
            if u.operand1 == m.name: u.operand1 = m.value
            if u.operand2 == m.name: u.operand2 = m.value
            u.evaluate()
            if u.hasValue():
                # This monkey has figured out its value -- remove it from the unsolved
                # list and add it to the constants list.
                removal_list.append(name)
                solved.append(u)
                if u.name == 'root':
                    print('Part One: Monkey named root yells {0}.'.format(u.value))

        for name in removal_list:
            del unsolved[name]

    return unsolved, solved

class Monkey:
    def __init__(self, name, operation, operand1, operand2=None):
        self.name = name
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.value = None

        if operation == OP_CONSTANT:
            self.value = operand1
            self.operand1 = None
            self.operand2 = None

    def hasValue(self):
        return (self.value is not None)

    def evaluate(self):
        if not (isinstance(self.operand1, int) and isinstance(self.operand2, int)):
            return

        if self.operation == OP_ADD:
            self.value = self.operand1 + self.operand2
        elif self.operation == OP_SUBTRACT:
            self.value = self.operand1 - self.operand2
        elif self.operation == OP_MULTIPLY:
            self.value = self.operand1 * self.operand2
        elif self.operation == OP_DIVIDE:
            self.value = self.operand1 // self.operand2

        self.operation = OP_CONSTANT
        self.operand1 = None
        self.operand2 = None

    def __str__(self):
        if self.value:
            return '{0}: {1}'.format(self.name, self.value)
        else:
            return '{0}: {1} {2} {3}'.format(self.name, self.operand1, self.operation, self.operand2)

# Parse the monkey jobs file
with open('day21_input.txt') as f:
    monkeys = [line.rstrip('\n')for line in f]

# Generate and solve for Part 1.
unsolved, solved = build(monkeys)
reduce(unsolved, solved)

# Generate and solve for Part 2.
# It's easier to just rebuild the setup from the monkeys file, since we've
# done some solving previously and the root and humn objects have been reduced.
# Don't include the 'humn' object, since we want to figure that out for ourselves.
unsolved, solved = build(monkeys, exclude='humn')
unsolved, solved = reduce(unsolved, solved)

# Figure out our starting point -- it's the root monkey's expected value
# on one side of the equality test. We'll work backwards from that value
# to figure out what we ('humn') need to yell for this to work.
root = unsolved['root']
if isinstance(root.operand1, int):
    target = root.operand2
    value = root.operand1
else:
    target = root.operand1
    value = root.operand2

# Work backwards -- undo each operation until we get to ourselves.
while target != 'humn':
    t = unsolved[target]
    if isinstance(t.operand1, int):
        if t.operation == OP_ADD:
            value -= t.operand1
        elif t.operation == OP_SUBTRACT:
            value = t.operand1 - value
        elif t.operation == OP_MULTIPLY:
            value //= t.operand1
        elif t.operation == OP_DIVIDE:
            value *= t.operand1
        target = t.operand2
    if isinstance(t.operand2, int):
        if t.operation == OP_ADD:
            value -= t.operand2
        elif t.operation == OP_SUBTRACT:
            value += t.operand2
        elif t.operation == OP_MULTIPLY:
            value //= t.operand2
        elif t.operation == OP_DIVIDE:
            value *= t.operand2
        target = t.operand1

print('Part Two: you need to yell {0} to pass root\'s equality test.'.format(value))
