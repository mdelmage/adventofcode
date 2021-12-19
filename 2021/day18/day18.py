#!/usr/bin/env python
# -*- coding: utf-8 -*-

def str_to_sf(s):
	sf = []
	for ch in s:
		if ch in '[],':
			sf.append(ch)
		else:
			sf.append(int(ch))
	return sf

def sf_to_list(sf):
	s = ''
	for ch in sf:
		s += '{0}'.format(ch)
	return eval(s)

def explode(sf_num):
	exploded = False
	depth = 0
	prev_num = None
	curr_num1 = None
	curr_num2 = None
	next_num = None
	for i in range(len(sf_num)):
		entry = sf_num[i]
		if entry == '[':
			depth += 1
		elif entry == ']':
			depth -= 1
		elif entry == ',':
			continue
		else:
			if depth == 5 and curr_num1 is None:
				exploded = True
				curr_num1 = i
			elif curr_num1 is not None and curr_num2 is None:
				curr_num2 = i
			elif curr_num1 is not None and curr_num2 is not None and next_num is None:
				next_num = i
			elif curr_num1 is None:
				prev_num = i

	if not exploded: return False
	if prev_num:
		sf_num[prev_num] += sf_num[curr_num1]
	if next_num:
		sf_num[next_num] += sf_num[curr_num2]
	del sf_num[curr_num1 - 1]
	del sf_num[curr_num1 - 1]
	del sf_num[curr_num1 - 1]
	del sf_num[curr_num1 - 1]
	sf_num[curr_num1 - 1] = 0
	return exploded

def split(sf_num):
	splitted = False
	split_idx = None
	for i in range(len(sf_num)):
		entry = sf_num[i]
		if isinstance(entry, int) and entry >= 10:
			splitted = True
			split_idx = i
			break
	if split_idx:
		split_num = sf_num[split_idx]
		sf_num[split_idx] = '['
		sf_num.insert(split_idx + 1, split_num // 2)
		sf_num.insert(split_idx + 2, ',')
		sf_num.insert(split_idx + 3, split_num - (split_num // 2))
		sf_num.insert(split_idx + 4, ']')
	return splitted

def reduce_sf(sf_num):
	done = False
	while not done:
		done = True
		if explode(sf_num):
			done = False
			continue
		if split(sf_num):
			done = False
			continue

def add_sf(sf1, sf2):
	sf = ['['] + sf1 + [','] + sf2 + [']']
	reduce_sf(sf)
	return sf

def list_magnitude(l):
	if isinstance(l[0], int):
		left = l[0]
	else:
		left = list_magnitude(l[0])

	if isinstance(l[1], int):
		right = l[1]
	else:
		right = list_magnitude(l[1])

	return (3 * left) + (2 * right)

# Parse the snailfish math homework file
with open('day18_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

running_sum = str_to_sf(lines[0])
for i in range(1, len(lines)):
	arg = str_to_sf(lines[i])
	running_sum = add_sf(running_sum, arg)
print('Part One: Magnitude of the final sum is {0}.'.format(list_magnitude(sf_to_list(running_sum))))

biggest_sum = 0
for i in range(len(lines)):
	for j in range(len(lines)):
		if i != j:
			op1 = str_to_sf(lines[i])
			op2 = str_to_sf(lines[j])
			test_sum = list_magnitude(sf_to_list(add_sf(op1, op2)))
			if test_sum > biggest_sum:
				biggest_sum = test_sum
print('Part Two: Largest single sum of pairs is {0}.'.format(biggest_sum))