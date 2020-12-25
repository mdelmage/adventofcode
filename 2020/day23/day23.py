#!/usr/bin/env python
# -*- coding: utf-8 -*-

CUPS_TEST  = 389125467
CUPS_INPUT = 167248359

# Convert our puzzle input, a number, into an ordered list of cups
seed = CUPS_INPUT
cups = []
while seed > 0:
    cups.insert(0, seed % 10)
    seed /= 10

current_cup = cups[0]
for i in range(100):
    #print cups
    #print 'current cup: %d' % current_cup
    picked_up_cups = []
    for x in range(3):
        current_cup_idx = cups.index(current_cup)
        pick_up_cup_idx = (current_cup_idx + 1) % len(cups)
        picked_up_cups.append(cups.pop(pick_up_cup_idx))
    #print 'okay i picked up %s, leaving %s' % (picked_up_cups, cups)
    
    destination_cup = (current_cup - 1) % (len(cups) + len(picked_up_cups))
    if destination_cup == 0: destination_cup = (len(cups) + len(picked_up_cups))
    while destination_cup in picked_up_cups:
        destination_cup = (destination_cup - 1) % (len(cups) + len(picked_up_cups))
        if destination_cup == 0: destination_cup = len(cups) + len(picked_up_cups)
    #print 'destination cup: %d' % destination_cup
    destination_cup_idx = cups.index(destination_cup)
    
    cups = cups[:destination_cup_idx+1] + picked_up_cups + cups[destination_cup_idx+1:]
    #print 'okay now i put the cups back, leaving %s' % cups
    
    current_cup_idx = (cups.index(current_cup) + 1) % len(cups)
    current_cup = cups[current_cup_idx]
    #print ''

answer = ''
cup_one_idx = cups.index(1)
for i in range(len(cups) - 1):
    answer += str(cups[(cup_one_idx + 1 + i) % len(cups)])

print answer

seed = CUPS_TEST
cups = []
while seed > 0:
    cups.insert(0, seed % 10)
    seed /= 10

cups += [i+1 for i in range(1000000)][len(cups):]
print len(cups)
print cups[:100]
print cups[-100:]

history = {}
current_cup = cups[0]
for i in range(10000000):
    result = tuple(cups[cups.index(1)+1:cups.index(1)+3])
    if result not in history:
        history[result] = 1
        print i, result
    #print cups
    #print 'current cup: %d' % current_cup
    picked_up_cups = []
    for x in range(3):
        current_cup_idx = cups.index(current_cup)
        pick_up_cup_idx = (current_cup_idx + 1) % len(cups)
        picked_up_cups.append(cups.pop(pick_up_cup_idx))
    #print 'okay i picked up %s, leaving %s' % (picked_up_cups, cups)

    destination_cup = (current_cup - 1) % (len(cups) + len(picked_up_cups))
    if destination_cup == 0: destination_cup = (len(cups) + len(picked_up_cups))
    while destination_cup in picked_up_cups:
        destination_cup = (destination_cup - 1) % (len(cups) + len(picked_up_cups))
        if destination_cup == 0: destination_cup = len(cups) + len(picked_up_cups)
    #print 'destination cup: %d' % destination_cup
    destination_cup_idx = cups.index(destination_cup)

    cups = cups[:destination_cup_idx+1] + picked_up_cups + cups[destination_cup_idx+1:]
    #print 'okay now i put the cups back, leaving %s' % cups

    current_cup_idx = (cups.index(current_cup) + 1) % len(cups)
    current_cup = cups[current_cup_idx]
    #print ''
