#!/usr/bin/python
# coding: utf-8

CMD_NEW_STACK = "deal into new stack"
CMD_INCREMENT = "deal with increment"
CMD_CUT       = "cut"

DECK_SIZE = 10007
TARGET_CARD = 2019

deck = [x for x in range(DECK_SIZE)]

def cmd_new_stack():
    global deck
    deck.reverse()

def cmd_cut(n):
    global deck
    deck = deck[n:] + deck[:n]

def cmd_increment(n):
    global deck
    new_deck = [0 for x in range(DECK_SIZE)]
    for i in range(DECK_SIZE):
        new_deck[(i * n) % DECK_SIZE] = deck[i]
    deck = new_deck

# Open input file
with open("day22.txt", "r") as f:
    for line in f:
        print line.strip()
        if CMD_NEW_STACK in line:
            cmd_new_stack()
        elif CMD_INCREMENT in line:
            increment = int(line[len(CMD_INCREMENT):])
            cmd_increment(increment)
        elif CMD_CUT in line:
            cut = int(line[len(CMD_CUT):])
            cmd_cut(cut)

    for i in range(DECK_SIZE):
        if TARGET_CARD == deck[i]:
            print "Found card {0} at position {1}!".format(TARGET_CARD, i)
            break