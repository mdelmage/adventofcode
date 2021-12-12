#!/usr/bin/env python
# -*- coding: utf-8 -*-

PART_ONE = 1
PART_TWO = 2

class Traversal:
	def __init__(self, rules, visited_nodes):
		self.rules = rules
		self.visited_nodes = visited_nodes
		self.visited_two_small_caves = False
		self.invalid = False
		self.complete = False

	def visit(self, node):
		t = Traversal(self.rules, [n for n in self.visited_nodes])
		t.visited_two_small_caves = self.visited_two_small_caves

		if node.isupper():
			# Uppercase node (big cave). No restritions; visit it.
			t.visited_nodes.append(node)
		elif node == 'start':
			# Start node. Not a valid traversal.
			t.invalid = True
		elif node == 'end':
			# End node. Nice work!
			t.visited_nodes.append(node)
			t.complete = True
		else:
			if self.rules == PART_ONE:
				# It would be a waste of time to visit any small cave more than once,
				# but big caves are large enough that it might be worth visiting them multiple times.
				# So, all paths you find should visit small caves at most once, and can visit
				# big caves any number of times.
				if node in t.visited_nodes:
					t.invalid = True
				else:
					t.visited_nodes.append(node)
			elif self.rules == PART_TWO:
				# After reviewing the available paths, you realize you might have time to visit
				# a single small cave twice. Specifically, big caves can be visited any number of times,
				# a single small cave can be visited at most twice, and the remaining small caves
				# can be visited at most once.
				visit_count = t.visited_nodes.count(node)
				if visit_count == 0:
					t.visited_nodes.append(node)
				elif visit_count == 1 and not t.visited_two_small_caves:
					t.visited_two_small_caves = True
					t.visited_nodes.append(node)
				else:
					t.invalid = True

		return t

def traverse(t):
	if t.invalid:
		return

	if t.complete:
		solutions.append(t.visited_nodes)
		return

	for node in the_map:
		last_node = t.visited_nodes[-1]
		if node[0] == last_node:
				next_node = node[1]
				traverse(t.visit(next_node))
		elif node[1] == last_node:
				next_node = node[0]
				traverse(t.visit(next_node))

# Parse the cave map path file
with open('day12_input.txt') as f:
	paths = [line.rstrip('\n') for line in f]

the_map = []
for path in paths:
	p = path.split('-')
	the_map.append((p[0], p[1]))

solutions = []
traverse(Traversal(PART_ONE, ['start']))
print('Part One: There are {0} paths through this cave system that visit small caves at most once.'.format(len(solutions)))

solutions = []
traverse(Traversal(PART_TWO, ['start']))
print('Part Two: There are {0} paths that visit one small cave at most twice, and other small caves at most once.'.format(len(solutions)))