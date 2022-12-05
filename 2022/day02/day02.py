#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the Rock Paper Scissors encrypted stategy guide
with open('day02_input.txt') as f:
    guide = [tuple(line.rstrip('\n').split()) for line in f]

# The first column is what your opponent is going to play:
# A for Rock, B for Paper, and C for Scissors.
OPPONENT_ROCK     = 'A'
OPPONENT_PAPER    = 'B'
OPPONENT_SCISSORS = 'C'

# The second column, you reason, must be what you should play in response:
# X for Rock, Y for Paper, and Z for Scissors.
YOU_ROCK     = 'X'
YOU_PAPER    = 'Y'
YOU_SCISSORS = 'Z'

# Your total score is the sum of your scores for each round.
# The score for a single round is the score for the shape you selected
# (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for
# the outcome of the round (0 if you lost, 3 if the round was a draw,
# and 6 if you won).
YOU_LOSE = 0
YOU_DRAW = 3
YOU_WIN  = 6

score_a = { YOU_ROCK:     1,
            YOU_PAPER:    2,
            YOU_SCISSORS: 3}

score_b = { (OPPONENT_ROCK, YOU_PAPER): YOU_WIN,
            (OPPONENT_ROCK, YOU_ROCK): YOU_DRAW,
            (OPPONENT_ROCK, YOU_SCISSORS): YOU_LOSE,

            (OPPONENT_PAPER, YOU_SCISSORS): YOU_WIN,
            (OPPONENT_PAPER, YOU_PAPER): YOU_DRAW,
            (OPPONENT_PAPER, YOU_ROCK): YOU_LOSE,

            (OPPONENT_SCISSORS, YOU_ROCK): YOU_WIN,
            (OPPONENT_SCISSORS, YOU_SCISSORS): YOU_DRAW,
            (OPPONENT_SCISSORS, YOU_PAPER): YOU_LOSE}

score = 0
for round in guide:
    score += score_a[round[1]] + score_b[round]

print('Part One: your total score is {0}.'.format(score))

# The Elf finishes helping with the tent and sneaks back over to you.
# "Anyway, the second column says how the round needs to end:
# X means you need to lose, Y means you need to end the round in a draw,
# and Z means you need to win. Good luck!"
YOU_LOSE = 'X'
YOU_DRAW = 'Y'
YOU_WIN  = 'Z'

you_play = { (OPPONENT_ROCK, YOU_WIN): YOU_PAPER,
             (OPPONENT_ROCK, YOU_DRAW): YOU_ROCK,
             (OPPONENT_ROCK, YOU_LOSE): YOU_SCISSORS,

             (OPPONENT_PAPER, YOU_WIN): YOU_SCISSORS,
             (OPPONENT_PAPER, YOU_DRAW): YOU_PAPER,
             (OPPONENT_PAPER, YOU_LOSE): YOU_ROCK,

             (OPPONENT_SCISSORS, YOU_WIN): YOU_ROCK,
             (OPPONENT_SCISSORS, YOU_DRAW): YOU_SCISSORS,
             (OPPONENT_SCISSORS, YOU_LOSE): YOU_PAPER}

score_b = { YOU_LOSE: 0,
            YOU_DRAW: 3,
            YOU_WIN:  6}

score = 0
for round in guide:
    # The total score is still calculated in the same way, but now you need
    # to figure out what shape to choose so the round ends as indicated.
    score += score_a[you_play[round]] + score_b[round[1]]

print('Part Two: your total score is {0}.'.format(score))
