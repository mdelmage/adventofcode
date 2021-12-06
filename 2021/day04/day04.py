#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BingoBoard:
	def __init__(self, lines):
		self.marked = {}
		self.unmarked = {}
		for y in range(5):
			for x in range(5):
				self.unmarked[(x, y)] = int(lines[y].split()[x])

	def mark(self, number):
		for spot in self.unmarked:
			if self.unmarked[spot] == number:
				self.marked[spot] = self.unmarked[spot]
				del self.unmarked[spot]
				return

	def match_horizontal(self):
		for row in range(5):
			matched = True
			for col in range(5):
				if (col, row) not in self.marked: matched = False
			if matched: return True
		return False

	def match_vertical(self):
		for col in range(5):
			matched = True
			for row in range(5):
				if (col, row) not in self.marked: matched = False
			if matched: return True
		return False

	def bingo(self):
		if self.match_horizontal() or self.match_vertical():
			return sum(self.unmarked.values())
		else:
			return None

def play():
	for n in draw:
		for b in boards:
			b.mark(n)
			if b.bingo():
				if len(boards) == initial_board_count:
					# To guarantee victory against the giant squid, figure out which board
					# will win first. What will your final score be if you choose that board?
					print('Part One: First board to win has score {0}.'.format(n * b.bingo()))
				elif len(boards) == 1:
					# On the other hand, it might be wise to try a different strategy:
					# let the giant squid win.
					#
					# Figure out which board will win last.
					# Once it wins, what would its final score be?
					print ('Part Two: Last board to win has score {0}.'.format(n * b.bingo()))
				boards.remove(b)
				return

# Parse the bingo file
with open('day04_input.txt') as f:
	boards_file = [line.rstrip('\n') for line in f]

draw = [int(n) for n in boards_file[0].split(',')]

# A bit of ugly parsing: grab sets of five lines and turn them into bingo boards.
boards = []
for i in range((len(boards_file) - 1) // 6):
	boards.append(BingoBoard(boards_file[2 + (i * 6) : 7 + (i * 6)]))

initial_board_count = len(boards)
while len(boards) > 0:
	play()