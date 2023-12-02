#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The Elf would first like to know which games would have been possible
# if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?
QUANTITIES = { 'red': 12, 'green' : 13, 'blue' : 14}
TOTAL_QUANTITY = sum(QUANTITIES.values())

# Parse the input
with open('day02_input.txt') as f:
    games = [line.rstrip('\n') for line in f]

possible_game_ids_sum = 0
power_sum = 0
for game in games:
    possible = True
    (game_id, g) = game.split(': ')
    game_id = int(game_id.replace('Game ', ''))
    minimum_quantities = { 'red': 0, 'green' : 0, 'blue' : 0}
    for sets in g.split('; '):
        total_cubes = 0
        for cubes in sets.split(', '):
            (quantity, color) = cubes.split(' ')
            quantity = int(quantity)
            total_cubes += quantity
            minimum_quantities[color] = max(minimum_quantities[color], quantity)

            # Check 1: If there are more cubes of a certain color than we want, mark the game as impossible.
            if quantity > QUANTITIES[color]: possible = False

        # Check 2: If there are more cubes in total than we want, mark the game as impossible.
        if total_cubes > TOTAL_QUANTITY: possible = False

    # Determine which games would have been possible if the bag had been loaded with only 12 red cubes,
    # 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
    if possible: possible_game_ids_sum += game_id

    # As you continue your walk, the Elf poses a second question: in each game you played, what is the
    # fewest number of cubes of each color that could have been in the bag to make the game possible?
    #
    # The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
    #
    # For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
    power_sum += minimum_quantities['red'] * minimum_quantities['blue'] * minimum_quantities['green']

print('Part One: Sum of all the possible game IDs is {0}.'.format(possible_game_ids_sum))
print('Part Two: Sum of all the power values is {0}.'.format(power_sum))
