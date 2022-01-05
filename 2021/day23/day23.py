#!/usr/bin/env python
# -*- coding: utf-8 -*-

AMBER  = 'A'
BRONZE = 'B'
COPPER = 'C'
DESERT = 'D'

ENERGY = { AMBER  :    1,
           BRONZE :   10,
           COPPER :  100,
           DESERT : 1000 }

SIDE_COLS = { AMBER  : 3,
              BRONZE : 5,
              COPPER : 7,
              DESERT : 9 }

NO_STOP_SPACES = [(3, 1), (5, 1), (7, 1), (9, 1)]

SIDE_ROOM_DEPTH = 2

HALLWAY_ROW = 1
HALLWAY_COL_LEFT = 1
HALLWAY_COL_RIGHT = 11

class SideRoom:
	def __init__(self, species, col, depth):
		self.species = species
		self.col = col
		self.depth = depth
		self.rooms = {}
		for row in range(HALLWAY_ROW + 1, HALLWAY_ROW + depth + 1):
			self.rooms[(col, row)] = None

	def organized(self):
		# The amphipods would like a method to organize every amphipod
		# into side rooms so that each side room contains one type of amphipod...
		for r in self.rooms:
			if self.rooms[r] != self.species: return False
		return True

	def available(self):
		# Return the next available space in the side room.
		# If there are wrong species in the room, return None.
		# If the room is properly organized, we're done -- return None.
		available_space = None
		for row in range(HALLWAY_ROW + self.depth, HALLWAY_ROW, -1):
			space = (self.col, row)
			inhabitant = self.rooms[space]
			if inhabitant is None and available_space is None:
				available_space = space
			elif inhabitant != self.species:
				return available_space

		return available_space

	def final(self, pos):
		# Return whether the amphipod in the position is in its final spot.
		# If so, return True.
		(col, row) = pos

		if col != self.col:
			return False

		while pos in self.rooms:
			if self.rooms[pos] != self.species:
				return False
			pos = (pos[0], pos[1] + 1)

		return True

class Hallway:
	def __init__(self):
		self.rooms = {}
		for col in range(HALLWAY_COL_LEFT, HALLWAY_COL_RIGHT + 1):
			self.rooms[(col, HALLWAY_ROW)] = None

class Burrow:
	def __init__(self):
		self.h = Hallway()
		self.s = {}
		self.energy = 0
		self.rooms = {}
		for species in SIDE_COLS:
			col = SIDE_COLS[species]
			self.s[col] = SideRoom(species, col, SIDE_ROOM_DEPTH)

	def copy(self):
		new_burrow = Burrow()
		new_burrow.energy = self.energy
		for pos in self.rooms:
			new_burrow.add(self.rooms[pos], pos)
		return new_burrow

	def add(self, amphipod, pos):
		# Add the amphipod to our global rooms map.
		self.rooms[pos] = amphipod

		# Add the amphipod to our hallway/side room objects.
		(col, row) = pos
		if row == HALLWAY_ROW:
			self.h.rooms[pos] = amphipod
		else:
			self.s[col].rooms[pos] = amphipod

	def move(self, src, dest):
		# Move the amphipod in our global rooms map.
		species = self.rooms[src]
		del self.rooms[src]
		self.rooms[dest] = species

		# Move the amphipod in our hallway/side room objects.
		(scol, srow) = src
		(dcol, drow) = dest

		if srow == HALLWAY_ROW:
			self.s[dcol].rooms[dest] = self.h.rooms[src]
			self.h.rooms[src] = None
		else:
			self.h.rooms[dest] = self.s[scol].rooms[src]
			self.s[scol].rooms[src] = None

		# Update the energy, based on the amphipod species and distance travelled
		self.energy += ENERGY[species] * burrow_distance(src, dest)

	def organized(self):
		# If each side room is organized, the burrow is organized.
		organized = True
		for col in self.s:
			organized &= self.s[col].organized()
		return organized

	def possible_moves(self, src):
		(col, row) = src
		dest = src
		species = self.rooms[src]
		home_col = SIDE_COLS[species]

		moves = []

		if row > HALLWAY_ROW:
			if self.s[home_col].final(src):
				# We're already in our final spot; bail out!
				return []

			while row > HALLWAY_ROW:
				row -= 1
				dest = (col, row)
				if dest in self.rooms:
					# Someone's in our way and we can't get to the hallway.
					# No moves can be made!
					return []

		# Scan leftward in the hallway until we run into an amphipod.
		for new_col in range(col, HALLWAY_COL_LEFT - 1, -1):
			dest = (new_col, row)
			if dest in self.rooms:
				if dest != src: break
			else:
				moves.append(dest)
					
		# Scan rightward in the hallway until we run into an amphipod.
		for new_col in range(col + 1, HALLWAY_COL_RIGHT + 1):
			dest = (new_col, row)
			if dest in self.rooms:
				break
			else:
				moves.append(dest)

		# We started in the hallway -- see if we can get to our home row.
		if src[1] == HALLWAY_ROW:
			if (home_col, HALLWAY_ROW) in moves:
				# Only consider the rearmost side room space.
				home_space = self.s[home_col].available()
				if home_space is None:
					moves = []
				else:
					moves = [home_space]
			else:
				moves = []

		# Amphipods will never stop on the space immediately outside any room.
		# They can move into that space so long as they immediately continue moving.
		# (Specifically, this refers to the four open spaces in the hallway that are
		# directly above an amphipod starting position.)
		moves = [s for s in moves if s not in NO_STOP_SPACES]

		# We've constructed a list of destinations; turn it into (src, dest) pairs.
		moves = [(src,m) for m in moves]
		return moves

	def all_possible_moves(self):
		moves = []
		for pos in self.rooms:
			moves += self.possible_moves(pos)

		return moves

def burrow_distance(a, b):
	# Kind of like Manhattan distance, but sideways travel is only allowed
	# in the hallway row.
	#
	# Calculate what the vertical distance is to the hallway from each spot,
	# then add the Manhattan distance of the horizontal travel.
	return (a[1] - HALLWAY_ROW) + (b[1] - HALLWAY_ROW) + abs(a[0] - b[0])

def iterate(b):
	global lowest_energy

	if b.energy > lowest_energy:
		return

	if b.organized():
		if b.energy < lowest_energy:
			# New best! Remember it.
			lowest_energy = b.energy
		return

	# Gather a list of all possible (src, dest) move pairs.
	next_moves = b.all_possible_moves()

	# If there are any moves that place an amphipod in its final spot
	# in its home row / side room, consider only those moves.
	optimized_moves = [m for m in next_moves if m[1][1] > HALLWAY_ROW]
	if len(optimized_moves) > 0: next_moves = optimized_moves

	for (src, dest) in next_moves:
		next_b = b.copy()
		next_b.move(src, dest)
		iterate(next_b)

def init():
	global b
	global lowest_energy

	# The most energy you could possibly spend organizing the amphipods is in the
	# neighborhood of 100,000 -- but just pick something arbitrarily higher than that.
	lowest_energy = 9999999

	# Construct the Burrow object from the input file.
	b = Burrow()
	for y in range(len(lines)):
		for x in range(len(lines[y])):
			if lines[y][x] not in ' #':
				if lines[y][x] != '.':
					b.add(lines[y][x], (x, y))

# Parse the amphipod burrow diagram file
with open('day23_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

init()
iterate(b)
print('Part One: Least energy to organize the amphipods is {0}.'.format(lowest_energy))

# As you prepare to give the amphipods your solution, you notice that the diagram they handed you
# was actually folded up. As you unfold it, you discover an extra part of the diagram.
#
# Between the first and second lines of text that contain amphipod starting positions,
# insert the following lines:
#
#  #D#C#B#A#
#  #D#B#A#C#
del lines[4]
lines.append(lines[3])
lines.append(lines[3])
lines[3] = '  #D#C#B#A#'
lines[4] = '  #D#B#A#C#'

SIDE_ROOM_DEPTH = 4

# Re-initialize and run again!
init()
iterate(b)
print('Part Two: Least energy to organize the amphipods is {0}.'.format(lowest_energy))