#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Every hand is exactly one type. From strongest to weakest, they are:
#
# Five of a kind, where all five cards have the same label: AAAAA
STRENGTH_FIVE_OF_A_KIND = 6
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
STRENGTH_FOUR_OF_A_KIND = 5
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
STRENGTH_FULL_HOUSE = 4
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from
# nany other card in the hand: TTT98
STRENGTH_THREE_OF_A_KIND = 3
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has
# a third label: 23432
STRENGTH_TWO_PAIR = 2
# One pair, where two cards share one label, and the other three cards have a different label from the pair and
# each other: A23A4
STRENGTH_ONE_PAIR = 1
# High card, where all cards' labels are distinct: 23456
STRENGTH_HIGH_CARD = 0

def hand_strength_without_jokers(h):
    return hand_strength(h, jokers_wild=False)

def hand_strength_with_jokers(h):
    return hand_strength(h, jokers_wild=True)

def hand_strength(h, jokers_wild):
    hand = h[0]
    cards = {}

    # Count up how many of each card we have.
    if jokers_wild:
        # To handle jokers, count how many we have -- but remove them from the actual hand we're counting.
        joker_count = hand.count('J')
        jokerless_hand = hand.replace('J', '')
        for c in jokerless_hand:
            cards[c] = cards.get(c, 0) + 1
    else:
        for c in hand:
            cards[c] = cards.get(c, 0) + 1

    # The easiest way to determine the type of hand we have is to list the card counts, in descending order.
    histogram = sorted(cards.values(), reverse=True)

    if jokers_wild:
        if len(histogram) == 0:
            # Ultimate hand -- all jokers!
            histogram = [5]
        else:
            # The jokers just count as the most common card. Add them here.
            histogram[0] += joker_count

    if histogram[0] == 5:
        hand_type = STRENGTH_FIVE_OF_A_KIND
    elif histogram[0] == 4:
        hand_type = STRENGTH_FOUR_OF_A_KIND
    elif histogram[0] == 3 and histogram[1] == 2:
        hand_type = STRENGTH_FULL_HOUSE
    elif histogram[0] == 3:
        hand_type = STRENGTH_THREE_OF_A_KIND
    elif histogram[0] == 2 and histogram[1] == 2:
        hand_type = STRENGTH_TWO_PAIR
    elif histogram[0] == 2:
        hand_type = STRENGTH_ONE_PAIR
    else:
        hand_type = STRENGTH_HIGH_CARD

    # Now score the hand itself by turning it into a hexidecimal number.
    # This lets us compare equal-strength hands directly, by value.
    # Note that the strongest hand ('AAAAA', or 0xeeeee, is just under one million.
    for (src, dest) in FACE_CARD_VALUES:
        hand = hand.replace(src, dest)
    hand_score = int(hand, base=16)

    # The final hand strength is its type multiplied by an arbitrary-but-large-enough value,
    # in this case one million, plus its hand score as a tiebreaker.
    return (1000000 * hand_type) + hand_score

# Parse the hands file
with open('day07_input.txt') as f:
    hands = [(hand, int(bid)) for (hand, bid) in [line.rstrip('\n').split() for line in f]]

# A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
# The relative strength of each card follows this order, where A is the highest and 2 is the lowest.
#
# Map face cards into hexadecimal values.
# Use lower-case hex destination values to avoid confusion.
# Number cards remain as they are.
FACE_CARD_VALUES = [('A', 'e'),
                    ('K', 'd'),
                    ('Q', 'c'),
                    ('J', 'b'),
                    ('T', 'a')]

# Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1,
# the second-weakest hand gets rank 2, and so on up to the strongest hand.
#
# Now, you can determine the total winnings of this set of hands by adding up the result of multiplying
# each hand's bid with its rank.
#
# Find the rank of every hand in your set. What are the total winnings?
rank = 1
winnings = 0
for (hand, bid) in sorted(hands, key=hand_strength_without_jokers):
    winnings += rank * bid
    rank += 1

print('Part One: Total winnings is {0}.'.format(winnings))

# To make things a little more interesting, the Elf introduces one additional rule.
# Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.
#
# To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in
# the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.
#
# Use a similar map as in Part One, except now 'J' is worth 1. It could also be worth 0.
FACE_CARD_VALUES = [('A', 'd'),
                    ('K', 'c'),
                    ('Q', 'b'),
                    ('T', 'a'),
                    ('J', '1')]

# Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
rank = 1
winnings = 0
for (hand, bid) in sorted(hands, key=hand_strength_with_jokers):
    winnings += rank * bid
    rank += 1

print('Part Two: Total winnings (with Jokers) is {0}.'.format(winnings))