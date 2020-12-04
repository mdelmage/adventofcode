#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Program(object):
    def __init__(self, name, weight, children):
        self.name = name
        self.weight = weight
        self.children = children
        self.total_weight = 0

    def weigh(self):
        correction = 0
        self.total_weight = self.weight
        child_weights = set()
        child_weights_freq = {}

        for c in self.children:
            # A bit clumsy, but keep track of:
            # 1. The total weight of each child, including its own children; and
            # 2. The frequencies of these total weights.
            #
            # The unbalanced program will be the one that does not
            # match the weights of its siblings.
            child_weight = programs[c].weigh()
            child_weights.add(child_weight)
            child_weights_freq[child_weight] = child_weights_freq.get(child_weight, 0) + 1
            self.total_weight += child_weight

        # The children should all weigh the same, so the set of the child weights
        # should be of size 1.
        #
        # If not, it should be of size 2 (since there's only one incorrect weight)
        # and the frequency of the correct weight will be greater than one.
        #
        # The frequency of the incorrect weight will be exactly one.
        if len(child_weights) > 1:
            for w in child_weights_freq:
                if child_weights_freq[w] == 1: wrong_weight = w
                if child_weights_freq[w] > 1: right_weight = w
            correction = right_weight - wrong_weight
            for c in self.children:
                child = programs[c]
                if child.total_weight == wrong_weight:
                    print 'Part Two: %s should weigh %d.' % (child.name, child.weight + correction)

        # To prevent reporting an imbalance all the way up the chain,
        # fix the incorrect weight when reporting it up.
        return self.total_weight + correction

# Parse the programs/towers list and save each line
with open('day07_input.txt') as f:
    program_list = [line.rstrip('\n') for line in f]

programs = {}
program_names = set()
child_program_names = set()
for p in program_list:
    # Tokenize the form "name (weight) -> child1, child2, childN"
    tokens = p.replace('(', '').replace(')', '').replace('-> ', '').replace(',', '').split()
    name = tokens[0]
    weight = int(tokens[1])
    children = tokens[2:]
    programs[name] = Program(name, weight, children)
    program_names.add(name)
    for c in children:
        child_program_names.add(c)

# The root node is the only program that isn't a child name!
root = (program_names - child_program_names).pop()
print 'Part One: root node is %s' % root
programs[root].weigh()