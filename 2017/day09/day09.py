#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the virtual stream and save each line
with open('day09_input.txt') as f:
    stream = [line.rstrip('\n') for line in f]

for line in stream:
    garbage = False
    garbage_count = 0
    level = 0
    score = 0
    for i in range(len(line)):
        if line[i] == '<' and not garbage:
            garbage = True
            # This character doesn't count against the garbage count,
            # so pre-decrement.
            garbage_count -= 1
        if line[i] == '>':
            garbage = False

        if line[i] == '{' and not garbage: level += 1
        if line[i] == '}' and not garbage:
            score += level
            level -= 1
        # In a futile attempt to clean up the garbage, some program has canceled
        # some of the characters within it using !: inside garbage, any character
        # that comes after ! should be ignored, including <, >, and even another !.
        if garbage:
            if line[i] == '!':
                # Replace the garbage indicator and the subsequent character.
                # The next character doesn't count against the garbage count,
                # so pre-decrement.
                line = line[:i] + '--' + line[i+2:]
                garbage_count -= 1
            else:
                # To prove you've removed it, you need to count all of the characters
                # within the garbage. The leading and trailing < and > don't count,
                # nor do any canceled characters or the ! doing the canceling.
                garbage_count += 1

    print 'Part One: score was {0}.'.format(score)
    print 'Part Two: {0} garbage characters.'.format(garbage_count)