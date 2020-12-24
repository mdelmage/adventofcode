#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

# Once the game ends, you can calculate the winning player's score.
# The bottom card in their deck is worth the value of the card multiplied by 1,
# the second-from-the-bottom card is worth the value of the card multiplied by 2,
# and so on. With 10 cards, the top card is worth the value on the card multiplied by 10.
def score(hand):
    score = 0
    for i in range(len(hand)):
        score += hand[i] * (len(hand) - i)

    return score

def combat(hands):
    # Then, the game consists of a series of rounds: both players draw their top card, and the player
    # with the higher-valued card wins the round. The winner keeps both cards, placing them on the bottom
    #  of their own deck so that the winner's card is above the other card. If this causes a player to have
    # all of the cards, they win, and the game ends.
    while len(hands[1]) > 0 and len(hands[2]) > 0:
        player1_card = hands[1].pop(0)
        player2_card = hands[2].pop(0)
        if player1_card > player2_card:
            hands[1].append(player1_card)
            hands[1].append(player2_card)
        else:
            hands[2].append(player2_card)
            hands[2].append(player1_card)

    if len(hands[1]) > 0:
        winning_hand = hands[1]
    else:
        winning_hand = hands[2]

    return score(winning_hand)
    
def recursive_combat(hands):
    # Before either player deals a card, if there was a previous round in this game that had exactly
    # the same cards in the same order in the same players' decks, the game instantly ends in a win
    # for player 1. Previous rounds from other games are not considered.
    history = []  
    while len(hands[1]) > 0 and len(hands[2]) > 0:
        if (tuple(hands[1]), tuple(hands[2])) in history:
            return (1, hands[1])
        history.append((tuple(hands[1]), tuple(hands[2])))
        
        player1_card = hands[1].pop(0)
        player2_card = hands[2].pop(0)

        # If both players have at least as many cards remaining in their deck as the value of the card they just drew,
        # the winner of the round is determined by playing a new game of Recursive Combat (see below).
        if player1_card <= len(hands[1]) and player2_card <= len(hands[2]):
            # To play a sub-game of Recursive Combat, each player creates a new deck by making a copy
            # of the next cards in their deck (the quantity of cards copied is equal to the number
            # on the card they drew to trigger the sub-game). During this sub-game, the game that triggered it
            # is on hold and completely unaffected; no cards are removed from players' decks to form the sub-game.
            subgame_hands = {}
            subgame_hands[1] = hands[1][:player1_card]
            subgame_hands[2] = hands[2][:player2_card]
            (winner, winning_score) = recursive_combat(subgame_hands)    
        else:
            # Otherwise, at least one player must not have enough cards left in their deck to recurse;
            # the winner of the round is the player with the higher-value card.
            winner = 1 if player1_card > player2_card else 2

        # As in regular Combat, the winner of the round (even if they won the round by winning a sub-game)
        # takes the two cards dealt at the beginning of the round and places them on the bottom of
        # their own deck (again so that the winner's card is above the other card).
        if winner == 1:
            hands[1].append(player1_card)
            hands[1].append(player2_card)
        else:
            hands[2].append(player2_card)
            hands[2].append(player1_card)

    if len(hands[1]) > 0:
        return (1, score(hands[1]))
    else:
        return (2, score(hands[2]))

# Parse the starting decks file, and save each line
with open('day22_input.txt') as f:
    starting_decks = [line.rstrip('\n').rstrip(')') for line in f]

hands = { 1: [], 2: []}
for line in starting_decks:
    if 'Player' in line:
        player = int(line.replace('Player ', '').replace(':', ''))
    elif line != '':
        hands[player].append(int(line))

# Play (non-recursive) Combat.
# Use a copy of the starting hands so that we can play Recursive Combat later.
game1_score = combat(copy.deepcopy(hands))
print 'Part One: score of the winning hand is {0}.'.format(game1_score)

# Play Recursive Combat.
(winner, game2_score) = recursive_combat(hands)
print 'Part Two: score of the winning hand is {0}.'.format(game2_score)
