#!/usr/bin/python
# coding: utf-8

from collections import namedtuple
import sys


Ingredient = namedtuple('Ingredient', 'quantity link')

CHEMICAL_BASE = "ORE"
CHEMICAL_REFINED = "FUEL"

reactions = {}
reserves = {}
chemicals = set()
ore_mined = 0

def produce(chemical, exit_on_mine=False):
    r = reactions[chemical]

    # Recursion limit. Bail early.
    if CHEMICAL_BASE == chemical:
        if exit_on_mine:
            print reserves
            print "We were able to make {0} units of {1}!".format(reserves[CHEMICAL_REFINED], CHEMICAL_REFINED)
            sys.exit()
        reserves[chemical] += r.quantity
        global ore_mined
        ore_mined += 1
        return

    # Recurse into base chemicals
    for i in r.inputs:
        ingredient_name = i.link.name
        ingredient_quantity = i.quantity
        while reserves[ingredient_name] < ingredient_quantity:
            produce(ingredient_name, exit_on_mine)

        # Consume the ingredient
        reserves[ingredient_name] -= ingredient_quantity

    # We've produced a new chemical! Store it.
    reserves[chemical] += r.quantity
    return

class Reaction():
    def __init__(self):
        self.inputs = []
        self.quantity = 1
        self.name = CHEMICAL_BASE

    def configure(self, inputs, output):
        for i in inputs.split(", "):
            (quantity, name) = i.split(" ")
            c = Ingredient(int(quantity), reactions[name])
            self.inputs.append(c)

        (quantity, name) = output.split(" ")        
        self.quantity = int(quantity)
        self.name = name
    
    def __str__(self):
        string = ""
        for i in self.inputs:
            string += "{0} units of {1} and ".format(i.quantity, i.link.name)
        string = string[:-4] + "become {0} units of {1}".format(self.quantity, self.name)
        return string
    
    def __repr__(self):
        return self.__str__()


filename = "day14.txt"

# First pass: get chemical names as placeholders
with open(filename, "r") as f:
    for reaction in f:
        (inputs, output) = reaction.strip().split(" => ")
        for i in inputs.split(", "):
            (quantity, name) = i.split(" ")
            chemicals.add(name)
        (quantity, name) = output.split(" ")
        chemicals.add(name)

for c in chemicals:
    r = Reaction()
    reactions[c] = r
    reserves[c] = 0

# Second pass: add reactions and make links
with open(filename, "r") as f:
    for reaction in f:
        inputs = [] 
        (inputs, output) = reaction.strip().split(" => ")
        name = output.split(" ")[1]
        reactions[name].configure(inputs, output)


produce(CHEMICAL_REFINED)
print "We mined {0} units of {1} to produce 1 {2}!".format(ore_mined, CHEMICAL_BASE, CHEMICAL_REFINED)

# Reset and add one trillion units of ore
for chemical in reserves:
    reserves[chemical] = 0
reserves[CHEMICAL_BASE] = 1000 * 1000 * 1000 * 1000

# Brute force attack. Ugh.
while True:
    produce(CHEMICAL_REFINED, True)
    if 0 == reserves[CHEMICAL_BASE] % 1000:
        ratio = reserves[CHEMICAL_BASE] / float(1000 * 1000 * 1000 * 1000)
        print "{0} / {1}".format(ratio, reserves[CHEMICAL_REFINED] / (1 - ratio))

