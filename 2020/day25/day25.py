#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The card transforms the subject number of 7 according to the card's secret loop size.
# The result is called the card's public key.
# The door transforms the subject number of 7 according to the door's secret loop size.
# The result is called the door's public key.
SUBJECT_NUMBER = 7

# To transform a subject number, start with the value 1. 
INITIAL_VALUE = 1

DIV_VALUE = 20201227

# The handshake used by the card and the door involves
# an operation that transforms a subject number.
def transform(subj, loop_size):
    # To transform a subject number, start with the value 1. 
    value = INITIAL_VALUE
    
    # Then, a number of times called the loop size, perform the following steps:
    #
    # Set the value to itself multiplied by the subject number.
    # Set the value to the remainder after dividing the value by 20201227.
    for i in range(loop_size):
        value *= subj
        value = value % DIV_VALUE
    
    return value

# Brute-forcing a loop size from a public key involves too much computation
# for it to be effective. Instead, walk the public key backwards until we reach
# the initial value of 1, and return how many loops that took to accomplish.
def untransform(pubkey):
    loop_size = 0
    while pubkey != INITIAL_VALUE:
        # Find a multiple of DIV_VALUE to add so that the pubkey is divisible by 7.
        while (pubkey % SUBJECT_NUMBER) != 0:
            pubkey += DIV_VALUE

        # Now do the division and increment the loop count.
        pubkey /= SUBJECT_NUMBER
        loop_size += 1
    return loop_size
    
# Parse the list of public keys, and save each line
with open('day25_input.txt') as f:
    [card_pubkey, door_pubkey] = [int(line.rstrip('\n')) for line in f]

# For example, suppose you know that the card's public key is 5764801.
# With a little trial and error, you can work out that the card's loop size must be 8,
# because transforming the initial subject number of 7 with a loop size of 8
# produces 5764801.
#
# Then, suppose you know that the door's public key is 17807724. By the same process,
# you can determine that the door's loop size is 11, because transforming
# the initial subject number of 7 with a loop size of 11 produces 17807724.
card_loop_size = untransform(card_pubkey)
door_loop_size = untransform(door_pubkey)

# At this point, you can use either device's loop size with the other device's
# public key to calculate the encryption key. 
ek1 = transform(card_pubkey, door_loop_size)
ek2 = transform(door_pubkey, card_loop_size)
if ek1 == ek2:
    print 'Part One: the encryption key is {0}.'.format(ek1)
else:
    print 'Failure! ek1 ({0}) was not equal to ek2 ({1})!'.format(ek1, ek2)