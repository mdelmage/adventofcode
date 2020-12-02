#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the passphrase list and save each line
with open('day04_input.txt') as f:
    passphrases = [line.rstrip('\n') for line in f]

valid_passphrases1 = 0
valid_passphrases2 = 0
for p in passphrases:
    valid1 = True
    valid2 = True
    words1 = set()
    words2 = set()

    for word in p.split():
        if word in words1:
            # To ensure security, a valid passphrase must contain no duplicate words.
            valid1 = False
        else:
            words1.add(word)
        
        sorted_word = ''.join(sorted(word))
        if sorted_word in words2:
            # For added security, yet another system policy has been put in place.
            # Now, a valid passphrase must contain no two words that are anagrams of each other -
            # that is, a passphrase is invalid if any word's letters can be rearranged to form
            # any other word in the passphrase.
            valid2 = False
        else:
            words2.add(sorted_word)
            
    if valid1: valid_passphrases1 += 1
    if valid2: valid_passphrases2 += 1

print 'Part One: %d passphrases were valid.' % valid_passphrases1
print 'Part One: %d passphrases were valid.' % valid_passphrases2