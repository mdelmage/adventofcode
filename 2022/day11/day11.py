#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Monkey:
    def __init__(self, number, items, operation, divisor, throw_true, throw_false):
        self.number = number
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.throw_true = throw_true
        self.throw_false = throw_false
        self.inspect_count = 0

    def inspect(self, relief=True):
        item = self.items.pop(0)

        # Operation shows how your worry level changes as that monkey inspects an item.
        # (An operation like new = old * 5 means that your worry level after the monkey
        # inspected the item is five times whatever your worry level was before inspection.)
        (operand1, operation, operand2) = self.operation.split(' ')
        if operation == '*' and operand2 == 'old':
            # Special case: convert 'self = old * old' to a pow() operation.
            item **= 2
        elif operation == '+':
            item += int(operand2)
        elif operation == '*':
            item *= int(operand2)

        # After each monkey inspects an item but before it tests your worry level,
        # your relief that the monkey's inspection didn't damage the item causes
        # your worry level to be divided by three and rounded down to the nearest integer.
        if relief: item //= 3

        # Test shows how the monkey uses your worry level to decide where to throw an item next.
        #
        # If true shows what happens with an item if the Test was true.
        # If false shows what happens with an item if the Test was false.
        if item % self.divisor == 0:
            throw_target = self.throw_true
        else:
            throw_target = self.throw_false

        self.inspect_count += 1
        return (item, throw_target)

class Item:
    def __init__(self, worry, divisors=None):
        if not divisors:
            # Normal/unoptimized mode: store the worry value and do normal operations.
            # This is achieved by using the underlying alternate/optimized mode,
            # but with a single divisor of 1, which kind of defeats the point of the
            # optimizations, but lets us reuse all the optimized class operations.
            self.value = int(worry)
        else:
            # Alternate/optimized mode: instead of storing the actual worry level,
            # store the modulo values (remainders) for divisors that we're interested in.
            #
            # Then, we can perform operations on the modulo values, avoiding huge numbers
            # in Part Two when the worry levels do not get divided by three after every round.
            self.value = None
            self.modulos = {}
            for d in divisors:
                self.modulos[d] = int(worry) % d

    def __iadd__(self, value):
        if self.value:
            self.value += value
        else:
            for d in self.modulos:
                self.modulos[d] = (self.modulos[d] + value) % d
        return self

    def __imul__(self, value):
        if self.value:
            self.value *= value
        else:
            for d in self.modulos:
                self.modulos[d] = (self.modulos[d] * value) % d
        return self

    def __ipow__(self, value):
        if self.value:
            self.value **= value
        else:
            for d in self.modulos:
                self.modulos[d] = (self.modulos[d] ** value) % d
        return self

    def __mod__(self, value):
        if self.value:
            return self.value % value
        else:
            return self.modulos[value]

    def __floordiv__(self, value):
        self.value //= value
        return self

# Parse the program file
with open('day11_input.txt') as f:
    monkey_notes = [line.rstrip('\n') for line in f]

# Scan the notes and determine all the divisors we should be tracking.
divisors = []
for i in range((len(monkey_notes) + 1) // 7):
    divisor = int(monkey_notes[7 * i + 3].split('divisible by ')[1])
    divisors.append(divisor)

# Convert the input to a list of monkeys for Part One
monkeys = []
for i in range((len(monkey_notes) + 1) // 7):
    items = [Item(n) for n in monkey_notes[7 * i + 1].split('items: ')[1].split(',')]
    operation = monkey_notes[7 * i + 2].split('new = ')[1]
    divisor = int(monkey_notes[7 * i + 3].split('divisible by ')[1])
    throw_true = int(monkey_notes[7 * i + 4].split('throw to monkey ')[1])
    throw_false = int(monkey_notes[7 * i + 5].split('throw to monkey ')[1])
    monkeys.append(Monkey(i, items, operation, divisor, throw_true, throw_false))

# Figure out which monkeys to chase by counting how many items they inspect over 20 rounds.
# What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?
for round in range(20):
    for m in monkeys:
        while len(m.items) > 0:
            (item, target) = m.inspect()
            monkeys[target].items.append(item)

inspect_counts = sorted([m.inspect_count for m in monkeys], reverse=True)
print('Part One: Level of monkey business is {0}.'.format(inspect_counts[0] * inspect_counts[1]))

# Convert the input to a list of monkeys for Part Two (same as we did for Part One)
monkeys = []
for i in range((len(monkey_notes) + 1) // 7):
    items = [Item(n, divisors) for n in monkey_notes[7 * i + 1].split('items: ')[1].split(',')]
    operation = monkey_notes[7 * i + 2].split('new = ')[1]
    divisor = int(monkey_notes[7 * i + 3].split('divisible by ')[1])
    throw_true = int(monkey_notes[7 * i + 4].split('throw to monkey ')[1])
    throw_false = int(monkey_notes[7 * i + 5].split('throw to monkey ')[1])
    monkeys.append(Monkey(i, items, operation, divisor, throw_true, throw_false))

# Worry levels are no longer divided by three after each item is inspected;
# you'll need to find another way to keep your worry levels manageable.
# Starting again from the initial state in your puzzle input, what is the level
# of monkey business after 10000 rounds?
for round in range(10000):
    for m in monkeys:
        while len(m.items) > 0:
            (item, target) = m.inspect(relief=False)
            monkeys[target].items.append(item)

inspect_counts = sorted([m.inspect_count for m in monkeys], reverse=True)
print('Part Two: Level of monkey business is {0}.'.format(inspect_counts[0] * inspect_counts[1]))
