#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the password list and save each line
with open('day02_input.txt') as f:
    passwords = [line.replace(':', '').rstrip('\n') for line in f]

policy1_passwords = 0
policy2_passwords = 0
for p in passwords:
    # Each line gives the password policy and then the password.
    (policy, letter, password) = p.split()
    (p1, p2) = [int(c) for c in policy.split('-')]

    # The password policy indicates the lowest and highest number
    # of times a given letter must appear for the password to be valid.
    letter_count = password.count(letter)
    if letter_count >= p1 and letter_count <= p2:
        policy1_passwords +=1

    # Each policy actually describes two positions in the password, where
    # 1 means the first character, 2 means the second character, and so on.
    # (Be careful; Toboggan Corporate Policies have no concept of "index zero"!)
    # Exactly one of these positions must contain the given letter.
    # Other occurrences of the letter are irrelevant for the purposes of policy enforcement.
    if (password[p1 - 1] == letter) ^ (password[p2 - 1] == letter):
        policy2_passwords += 1

print 'Part One: There were {0} valid passwords.'.format(policy1_passwords)
print 'Part Two: There were {0} valid passwords.'.format(policy2_passwords)