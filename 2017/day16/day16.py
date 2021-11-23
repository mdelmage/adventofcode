#!/usr/bin/env python
# -*- coding: utf-8 -*-

CMD_SPIN = 's'
CMD_EXCHANGE = 'x'
CMD_PARTNER = 'p'

def spin(s, X):
    return s[-X:] + s[:-X]

def exchange(s, A, B):
    return partner(s, s[A], s[B])

def partner(s, A, B):
    return s.replace(A,'A').replace(B,'B').replace('A',B).replace('B',A)

# Parse the program file
with open('day16_input.txt') as f:
    program = [line.rstrip('\n').split(',') for line in f][0]

# There are sixteen programs in total, named a through p.
# They start by standing in a line: a stands in position 0, b stands in position 1,
# and so on until p, which stands in position 15.
dance = ''
for i in range(16):
    dance += chr(ord('a') + i)

iteration = 0

# Keeping the positions they ended up in from their previous dance,
# the programs perform it again and again: including the first dance, a
# total of one billion (1000000000) times.
#
# By inspection: the dance order has period 300. Only execute as many times
# as is needed to simulate one billion iterations.
while iteration < ((1000 * 1000 * 1000) % 300):
    if iteration == 1: print 'Part One: dance order is {0}.'.format(dance)

    for line in program:
        cmd = line[0]
        args = line[1:].split('/')

        if cmd == CMD_SPIN:
            dance = spin(dance, int(args[0]))
        elif cmd == CMD_EXCHANGE:
            dance = exchange(dance, int(args[0]), int(args[1]))
        elif cmd == CMD_PARTNER:
            dance = partner(dance, args[0], args[1])

    iteration += 1

print 'Part Two: dance order is {0}.'.format(dance)