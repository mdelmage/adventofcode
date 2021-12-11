#!/usr/bin/env python
# -*- coding: utf-8 -*-

DELIMITER_START = ['(', '[', '{', '<']
DELIMITER_END = [')', ']', '}', '>']
DELIMITER_POINTS = [3, 57, 1197, 25137]

# Parse the navigation subsystem file
with open('day10_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

syntax_error_score = 0
completion_scores = []
for line in lines:
	chunk_stack = []
	for ch in line:
		if ch in DELIMITER_START:
			chunk_stack.append(DELIMITER_START.index(ch))
		if ch in DELIMITER_END:
			end_delim = DELIMITER_END.index(ch)
			# Some lines are incomplete, but others are corrupted.
			# Find and discard the corrupted lines first.
			if chunk_stack[-1] != end_delim:
				# To calculate the syntax error score for a line, take the first illegal character
				# on the line and look it up in the following table (...)
				syntax_error_score += DELIMITER_POINTS[end_delim]
				line = ''
				break
			else:
				chunk_stack.pop()

	if line != '':
		line_score = 0
		while len(chunk_stack) > 0:
			# The score is determined by considering the completion string character-by-character.
		 	# Start with a total score of 0. Then, for each character, multiply the total score
		 	# by 5 and then increase the total score by the point value given for the character
		 	# in the following table (...)
			end_delim = chunk_stack.pop()
			line_score = (line_score * 5) + end_delim + 1
		completion_scores.append(line_score)

# Find the first illegal character in each corrupted line of the navigation
# subsystem. What is the total syntax error score for those errors?
print('Part One: Total syntax error score is {0}.'.format(syntax_error_score))

# Autocomplete tools are an odd bunch: the winner is found by sorting
# all of the scores and then taking the middle score.
completion_scores.sort()
median_score = completion_scores[len(completion_scores) // 2]
print('Part Two: Winning completion string score is {0}.'.format(median_score))