#!/usr/bin/env python
# -*- coding: utf-8 -*-

def snafu_to_decimal(n):
    # Converting to decimal is pretty straightforward.
    # Add up the powers of 5, and allow for the special digits.
    result = 0
    for i in range(len(n)):
        # You ask why some of the digits look like - or = instead of "digits".
        #
        # "You know, I never did ask the engineers why they did that. Instead of
        # using digits four through zero, the digits are 2, 1, 0, minus (written -),
        # and double-minus (written =). Minus is worth -1, and double-minus is worth -2."
        if n[i] == '=':
            digit = -2
        elif n[i] == '-':
            digit = -1
        else:
            digit = int(n[i])
        result += ((5 ** (len(n) - i - 1)) * digit)

    return result

def decimal_to_snafu(n):
    # Converting to snafu is also pretty straightforward.
    # Divide off by powers of 5, and allow for the special digits.
    result = ''
    while n > 0:
        digit = n % 5
        if digit == 3:
            # This is a negative digit, so add back to the result.
            n += 5
            result = '=' + result
        elif digit == 4:
            # This is a negative digit, so add back to the result.
            n += 5
            result = '-' + result
        else:
            result = str(n % 5) + result
        n //= 5

    return result

# Parse the valley and blizzards map file
with open('day25_input.txt') as f:
    snafu_numbers = [line.rstrip('\n')for line in f]

snafu = decimal_to_snafu(sum([snafu_to_decimal(n) for n in snafu_numbers]))
print('Part One: You apply SNAFU number {0} to the console.'.format(snafu))
