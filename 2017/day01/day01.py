#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the captcha and save each line
with open('day01_input.txt') as f:
    captchas = [line.rstrip('\n') for line in f]

for captcha in captchas:
    # The captcha requires you to review a sequence of digits (your puzzle input) and find
    # the sum of all digits that match the next digit in the list. The list is circular,
    # so the digit after the last digit is the first digit in the list.
    matches = 0
    for i in range(len(captcha)):
        i_next = (i + 1) % len(captcha)
        if captcha[i] == captcha[i_next]:
            matches += int(captcha[i])
    print 'Part One: sum=%d' % matches

    # Now, instead of considering the next digit, it wants you to consider the digit halfway
    # around the circular list. That is, if your list contains 10 items, only include a digit
    # in your sum if the digit 10/2 = 5 steps forward matches it. Fortunately, your list has
    # an even number of elements.
    matches = 0
    for i in range(len(captcha)):
        i_next = (i + len(captcha) / 2) % len(captcha)
        if captcha[i] == captcha[i_next]:
            matches += int(captcha[i])
    print 'Part Two: sum=%d' % matches