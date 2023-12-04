#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the scratchcard table
with open('day04_input.txt') as f:
    scratchcard = [line.rstrip('\n') for line in f]

card_num = 1
total_score = 0
scratchcards = {key: 1 for key in list(range(1, len(scratchcard) + 1))}
scratchcards_played = 0
for line in scratchcard:
    # Picking one up, it looks like each card has two lists of numbers separated by a vertical bar
    # (|): a list of winning numbers and then a list of numbers you have.
    (winners, numbers) = scratchcard[card_num - 1].split(' | ')
    winners = winners.split(': ')[1]
    winners = [int(n) for n in winners.split()]
    numbers = [int(n) for n in numbers.split()]

    # As far as the Elf has been able to figure out, you have to figure out which of the numbers
    # you have appear in the list of winning numbers.
    game_score = 0
    for n in numbers:
        if n in winners:
            game_score += 1

    # Copies of scratchcards are scored like normal scratchcards and have the same card number
    # as the card they copied.
    multiplier = scratchcards[card_num]

    # Just as you're about to report your findings to the Elf, one of you realizes that the rules
    # have actually been printed on the back of every card this whole time.
    #
    # There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards
    # equal to the number of winning numbers you have.
    #
    # Specifically, you win copies of the scratchcards below the winning card equal to the number of matches.
    for winnings in range(1, game_score + 1):
        scratchcards[card_num + winnings] += multiplier

    # Process all of the original and copied scratchcards until no more scratchcards are won.
    scratchcards_played += multiplier
    del scratchcards[card_num]
    card_num += 1

    # The first match makes the card worth one point and each match after the first
    # doubles the point value of that card.
    if game_score > 0: game_score = 2 ** (game_score - 1)
    total_score += game_score

print('Part One: Sum of all the scratchcard scores is {0}.'.format(total_score))
print('Part Two: Total scratchcards played is {0}.'.format(scratchcards_played))