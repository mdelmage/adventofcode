#!/usr/bin/env python
# -*- coding: utf-8 -*-

DETERMINISTIC_DIE_SIDES = 100
BOARD_SPACES = 10

WINNING_SCORE_PART_ONE = 1000
WINNING_SCORE_PART_TWO = 21

def increment_die():
	# Since the first game is a practice game, the submarine opens a compartment labeled
	# deterministic dice and a 100-sided die falls out. This die always rolls 1 first,
	# then 2, then 3, and so on up to 100, after which it starts over at 1 again.
	# Play using this die.
	global die
	global die_rolls
	die = (die + 1) % DETERMINISTIC_DIE_SIDES
	die_rolls += 1

def move_pawn(player):
	global die

	for i in range(die):
		# Then, the player moves their pawn that many times forward around the track
		# (that is, moving clockwise on spaces in order of increasing value, wrapping
		# back around to 1 after 10).
		positions[player] += 1
		if positions[player] > BOARD_SPACES: positions[player] = 1
	increment_die()

# Parse the starting spaces file
with open('day21_input.txt') as f:
	lines = [line.rstrip('\n').split('starting position: ') for line in f]

# Each player's starting space is chosen randomly (your puzzle input).
# Player 1 goes first.
pos_p1 = int(lines[0][1])
pos_p2 = int(lines[1][1])
positions = [pos_p1, pos_p2]
player = 0
scores = [0, 0]
die_rolls = 0
die = 1

while True:
	# Players take turns moving. On each player's turn, the player rolls the die three times
	# and adds up the results. Then, the player moves their pawn that many times forward around the track.
	move_pawn(player)
	move_pawn(player)
	move_pawn(player)

	# After each player moves, they increase their score by the value of the space
	# their pawn stopped on. Players' scores start at 0.
	scores[player] += positions[player]
	if scores[player] >= WINNING_SCORE_PART_ONE:
		losing_score = scores[player ^ 1]
		break

	# Switch players.
	player ^= 1

print('Part One: Losing score times die rolls is {0}.'.format(die_rolls * losing_score))

# Generate a probability table for rolling a 3-sided Dirac die three times.
# We could just write this out statically, but it's easier to modify if
# we want to model different kinds of dice.
rolls = {}
for r1 in range(1, 4):
	for r2 in range(1, 4):
		for r3 in range(1, 4):
			rolls[r1 + r2 + r3] = rolls.get(r1 + r2 + r3, 0) + 1

# Keep track of quantum game states.
# The key is the scores and positions for each player.
# The value is the number of universes with that setup.
quantum_games = {((0, 0), (pos_p1, pos_p2)): 1}

# Track how many universes in which each player wins.
wins = [0, 0]

# Player 1 starts the game.
player = 0

# Evaluate all possible universes. To do this, start at the initial state.
# For each turn, multiply the probability table against each possible game state
# for the active player, then record the resulting state.
# If that turn results in a win for the active player, remove that game state
# from the list of games to evaluate.
while len(quantum_games) > 0:
	new_games = {}
	for (scores, positions) in quantum_games:
		for r in rolls:
			# Calculate the new board position after the roll.
			# That's also the score to add for that player.
			new_position = positions[player] + r
			if new_position > BOARD_SPACES: new_position -= 10
			new_score = scores[player] + new_position

			# Apply the new score and position to the active player.
			if player == 0:
				new_scores = (new_score, scores[1])
				new_positions = (new_position, positions[1])
			else:
				new_scores = (scores[0], new_score)
				new_positions = (positions[0], new_position)

			# If there's a player that won, we're done evaluating that quantum position.
			# Count how many universes have that result, and increment the wins.
			# Otherwise generate the next quantum game state.
			if new_scores[0] >= WINNING_SCORE_PART_TWO:
				wins[0] += quantum_games[(scores, positions)] * rolls[r]
			elif new_scores[1] >= WINNING_SCORE_PART_TWO:
				wins[1] += quantum_games[(scores, positions)] * rolls[r]
			else:
				prev_count = new_games.get((new_scores, new_positions), 0)
				new_count = quantum_games[(scores, positions)] * rolls[r]
				new_games[(new_scores, new_positions)] = prev_count + new_count

	# Replace the previous set of games with our new set.
	quantum_games = new_games

	# Switch players.
	player ^= 1

print('Part Two: Most winning player wins in {0} universes.'.format(max(wins)))