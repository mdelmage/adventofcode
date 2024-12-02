#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the locations list.
with open('day01_input.txt') as f:
    locations = [[int(l) for l in line.rstrip('\n').split()] for line in f]

# Throughout the Chief's office, the historically significant locations are listed
# not by name but by a unique number called the location ID. To make sure they don't
# miss anything, The Historians split into two groups, each searching the office
# and trying to create their own complete list of location IDs.
list1 = []
list2 = []
list2_counts = {}
for (loc1, loc2) in locations:
    list1.append(loc1)
    list2.append(loc2)
    list2_counts[loc2] = list2_counts.get(loc2, 0) + 1

# Maybe the lists are only off by a small amount! To find out, pair up the numbers
# and measure how far apart they are. Pair up the smallest number in the left list
# with the smallest number in the right list, then the second-smallest left number
# with the second-smallest right number, and so on.
list1 = sorted(list1)
list2 = sorted(list2)

# Within each pair, figure out how far apart the two numbers are;
# you'll need to add up all of those distances.
total_distance = 0
for l in range(len(list1)):
    total_distance += abs(list1[l] - list2[l])

# Your actual left and right lists contain many location IDs.
# What is the total distance between your lists?
print('Part One: The total distance between the lists is {0}.'.format(total_distance))

# This time, you'll need to figure out exactly how often each number from the left list
# appears in the right list. Calculate a total similarity score by adding up each number
# in the left list after multiplying it by the number of times that number appears in the right list.
similarity_score = 0
for location in list1:
    similarity_score += location * list2_counts.get(location, 0)

# Once again consider your left and right lists. What is their similarity score?
print('Part Two: The similarity score of the lists is {0}.'.format(similarity_score))
