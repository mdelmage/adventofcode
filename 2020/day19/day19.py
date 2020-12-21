#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rule(object):
    def __init__(self, r, left=None, right=None, literal=None):
        self.r = r
        self.left = left
        self.right = right
        self.literal = literal

    def __str__(self):
        if self.literal:
            return 'Rule {0}: literal={1}'.format(self.r, self.literal)
        else:
            return 'Rule {0}: left={1}, right={2}'.format(self.r, self.left, self.right)

    def traverse(self, possible_matches):
        remainders = []

        if self.literal:
            for m in possible_matches:
                if len(m) > 0 and m[0] == self.literal:
                    # We matched the leading character in the string. The remainder is
                    # just the rest of the string from the second character onwards
                    # (if any).
                    remainders.append(m[1:])
            return remainders

        # Go down the left subtree and generate a list of remainder strings
        # for all possible rules.
        remainders_left = possible_matches
        for r in self.left:
            remainders_left = rules[r].traverse(remainders_left)
            if len(remainders_left) == 0: break

        # Go down the right subtree (which is optional) and generate a list
        # of remainder strings for all possible rules.
        if self.right:
            remainders_right = possible_matches
            for r in self.right:
                remainders_right = rules[r].traverse(remainders_right)
                if len(remainders_right) == 0: break

        # Combine the remainder strings and return them one level up.
        if len(remainders_left) > 0: remainders += remainders_left
        if self.right and len(remainders_right) > 0: remainders += remainders_right
        return remainders

# Parse the list of message rules and valid messages, and save each line
with open('day19_input.txt') as f:
    messages_and_rules = [line.rstrip('\n') for line in f]

rules = {}
messages = []
for l in messages_and_rules:
    if ':' in l:
        tokens = l.split(': ')
        rule_num = int(tokens[0])
        rule = tokens[1]
        
        if 'a' in rule or 'b' in rule:
            # Some rules, like 3: "b", simply match a single character (in this case, b).
            rules[rule_num] = Rule(rule_num, literal=rule.replace('"', ''))
        else:
            # The remaining rules list the sub-rules that must be followed; for example,
            # the rule 0: 1 2 means that to match rule 0, the text being checked must match
            # rule 1, and the text after the part that matched rule 1 must then match rule 2.
            level_1 = []

            # Some of the rules have multiple lists of sub-rules separated by a pipe (|).
            # This means that at least one list of sub-rules must match. (The ones that match
            # might be different each time the rule is encountered.) For example,
            # the rule 2: 1 3 | 3 1 means that to match rule 2, the text being checked must match
            # rule 1 followed by rule 3 or it must match rule 3 followed by rule 1.
            options = rule.split(' | ')
            for o in options:
                level_2 = []
                for subrule in o.split():                    
                    level_2.append(int(subrule))
                level_1.append(level_2)
            if len(level_1) == 2:
                rules[rule_num] = Rule(rule_num, left=level_1[0], right=level_1[1])
            else:
                rules[rule_num] = Rule(rule_num, left=level_1[0])
                
    elif len(l) > 0:
        # The received messages (the bottom part of your puzzle input) need to be checked
        #  against the rules so you can determine which are valid and which are corrupted.
        messages.append(l)

matches = 0
for m in messages:
    remainders = rules[0].traverse([m])
    if '' in remainders: matches += 1

print 'Part One: there were {0} matching strings.'.format(matches)

# As you look over the list of messages, you realize your matching rules
# aren't quite right. To fix them, completely replace rules 8: 42 and 11: 42 31
# with the following:
#
# 8: 42 | 42 8
# 11: 42 31 | 42 11 3
rules[8] = Rule(8, left=[42], right=[42, 8])
rules[11] = Rule(11, left=[42, 31], right=[42, 11, 31])

matches = 0
for m in messages:
    remainders = rules[0].traverse([m])
    if '' in remainders: matches += 1

print 'Part Two: there were {0} matching strings.'.format(matches)
