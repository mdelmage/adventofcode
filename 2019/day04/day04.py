#!/usr/bin/python

PW_MIN = 136760
PW_MAX = 595730

def password_acceptable(password):
    # Build an array of password digits
    digits = []
    while password > 0:
        digits.append(password % 10)
        password /= 10
    digits.reverse()

    # Criteria 1: Two digits are the same
    # and NOT part of a larger match group

    # First, find all triplets ("111", "444", etc.)
    triplets = {}
    for i in range(len(digits) - 2):
        if (digits[i] == digits[i + 1]) and (digits[i + 1] == digits[i + 2]):
            if digits[i] not in triplets: triplets[digits[i]] = 1

    # Now find pairs that aren't triples
    adjacent_match = False
    for i in range(len(digits) - 1):
        if (digits[i] == digits[i + 1]) and (digits[i] not in triplets):
            adjacent_match = True
    if not adjacent_match: return False
        

    # Criteria 2: Digits monotonically increase
    last_digit = 0
    for digit in digits:
        if digit < last_digit:
            return False
        else:
            last_digit = digit

    return True


viable_passwords = 0

for password in range(PW_MIN, PW_MAX + 1):
    if password_acceptable(password):
        viable_passwords += 1
print "{0} passwords between {1}-{2} meet criteria.".format(viable_passwords, PW_MIN, PW_MAX)