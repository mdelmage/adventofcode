#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the ingredients and allergens list, and save each line
with open('day21_input.txt') as f:
    food_list = [line.rstrip('\n').rstrip(')') for line in f]

all_ingredients = []
allergens = {}
for line in food_list:
    # You start by compiling a list of foods (your puzzle input), one food per line.
    # Each line includes that food's ingredients list followed by some or all
    # of the allergens the food contains.
    tokens = line.split(' (contains ')
    ingredients = tokens[0].split()
    allergens_list = tokens[1].split(', ')

    # Keep track of each ingredient, including duplicates, to do some math later on.
    all_ingredients += ingredients

    # Also record, for each allergen, a set of possible ingredients that could contain it.
    # As we find the allergen listed in other recipies, narrow down that set to the ingredients
    # that are common across all recipies.
    for allergen in allergens_list:
        allergens[allergen] = allergens.get(allergen, set(ingredients)) & set(ingredients)

done = False
while not done:
    done = True
    # Go looking for an allergen that only has one possible ingredient source.
    # That means we can make a direct link between this allergen/ingredient pair.
    # Go back and remove that ingredient from other allergen lists.
    #
    # This will expose another allergen that we can isolate to a single ingredient, and so on.
    #
    # Repeat this process until we've identified exactly which ingredients contain allergens.
    for a in allergens:
        if len(allergens[a]) == 1:
            # Identify this ingredient and remove it from the other allergen sets.
            ingredient = list(allergens[a])[0]
            for other_allergen in [x for x in allergens if x != a]:
                if ingredient in allergens[other_allergen]:
                    allergens[other_allergen].discard(ingredient)
                    done = False

# Compile the list of ingredients that contain allergens.
allergen_ingredients = set([])
for s in allergens:
    allergen_ingredients |= allergens[s]

# Determine which ingredients cannot possibly contain any of the allergens in your list.
# How many times do any of those ingredients appear?
safe_ingredients = [i for i in all_ingredients if i not in allergen_ingredients]
print 'Part One: count of safe ingredients is {0}.'.format(len(safe_ingredients))

# Arrange the ingredients alphabetically by their allergen and separate them by commas
# to produce your canonical dangerous ingredient list. (There should not be any spaces
# in your canonical dangerous ingredient list.)
canonical_dangerous_ingredient_list = ''
for i in sorted(allergens):
    canonical_dangerous_ingredient_list += next(iter(allergens[i])) + ','
print 'Part Two: canonical dangerous ingredient list is \'{0}\'.'.format(canonical_dangerous_ingredient_list.rstrip(','))