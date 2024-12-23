#!/usr/bin/env python
# -*- coding: utf-8 -*-

def fully_linked(computer, group):
    for peer in group:
        if computer not in links[peer]: return False
    return True

# Parse the map of the local network.
with open('day23_input.txt') as f:
    network = [line.rstrip('\n').split('-') for line in f]

computers = set()
links = {}
for c1, c2 in network:
    computers.add(c1)
    computers.add(c2)
    if c1 not in links: links[c1] = []
    if c2 not in links: links[c2] = []
    links[c1].append(c2)
    links[c2].append(c1)

# LAN parties typically involve multiplayer games, so maybe you can locate it by finding groups
# of connected computers. Start by looking for sets of three computers where each computer in the set
# is connected to the other two computers.
#
# If the Chief Historian is here, and he's at the LAN party, it would be best to know that right away.
# You're pretty sure his computer's name starts with t, so consider only sets of three computers where
# at least one computer's name starts with t.
groups = set()
for c1, c2, c3 in [(c1, c2, c3) for c1 in computers for c2 in computers for c3 in computers if c3[0] == 't']:
    if c2 in links[c1] and c3 in links[c1] and c3 in links[c2]:
        groups.add(tuple(sorted((c1, c2, c3))))

# Find all the sets of three inter-connected computers.
# How many contain at least one computer with a name that starts with t?
print('Part One: There are {0} sets of interconnected computers with at least one \'t\'.'.format(len(groups)))

# There are still way too many results to go through them all. You'll have to find the LAN party another way
# and go there yourself.
#
# Since it doesn't seem like any employees are around, you figure they must all be at the LAN party.
# If that's true, the LAN party will be the largest set of computers that are all connected to each other.
# That is, for each computer at the LAN party, that computer will have a connection to every other computer
# at the LAN party.
largest_group = []
for c in computers:
    local_group = [c]
    for peer in links[local_group[0]]:
        if peer in computers and fully_linked(peer, local_group): local_group.append(peer)
    if len(local_group) > len(largest_group): largest_group = local_group
 
# The LAN party posters say that the password to get into the LAN party is the name of every computer
# at the LAN party, sorted alphabetically, then joined together with commas.
password = ''
for computer in sorted(largest_group):
    password += '{0},'.format(computer)
password = password[:-1]

# What is the password to get into the LAN party?
print('Part Two: The LAN party password is \'{0}\'.'.format(password))