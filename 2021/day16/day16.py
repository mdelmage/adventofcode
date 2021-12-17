#!/usr/bin/env python
# -*- coding: utf-8 -*-

TYPE_SUM          = 0
TYPE_PRODUCT      = 1
TYPE_MINIMUM      = 2
TYPE_MAXIMUM      = 3
TYPE_LITERAL      = 4
TYPE_GREATER_THAN = 5
TYPE_LESS_THAN    = 6
TYPE_EQUAL_TO     = 7

LENGTH_TYPE_BITS       = 0
LENGTH_TYPE_SUBPACKETS = 1

BITS_VERSION         = 3
BITS_TYPE_ID         = 3
BITS_LENGTH_TYPE_ID  = 1
BITS_LITERAL_CONT    = 1
BITS_LITERAL_NIBBLE  = 4
BITS_SUBPACKET_BITS  = 15
BITS_SUBPACKET_COUNT = 11

class Packet:
	def __init__(self, binary_str):
		(self.version, binary_str) = pop(binary_str, BITS_VERSION)
		(self.type_id, binary_str) = pop(binary_str, BITS_TYPE_ID)
		self.subpackets = []

		if self.type_id == TYPE_LITERAL:
			done = False
			literal = 0
			while not done:
				(continuation, binary_str) = pop(binary_str, BITS_LITERAL_CONT)
				if continuation == 0: done = True
				(nibble, binary_str) = pop(binary_str, BITS_LITERAL_NIBBLE)
				literal *= (2 ** BITS_LITERAL_NIBBLE)
				literal += nibble
			self.value = literal
		else:
			# Every other type of packet (any packet with a type ID other than 4) represent
			# an operator that performs some calculation on one or more sub-packets contained within.
			# Right now, the specific operations aren't important; focus on parsing the hierarchy of sub-packets.
			#
			# An operator packet contains one or more packets.
			(length_type_id, binary_str) = pop(binary_str, 1)
			if length_type_id == LENGTH_TYPE_BITS:
				(subpacket_bits, binary_str) = pop(binary_str, BITS_SUBPACKET_BITS)
				following_bits = len(binary_str) - subpacket_bits
				while len(binary_str) > following_bits:
					subpacket = Packet(binary_str)
					binary_str = subpacket.remainder
					self.subpackets.append(subpacket)					
			elif length_type_id == LENGTH_TYPE_SUBPACKETS:
				(subpacket_count, binary_str) = pop(binary_str, BITS_SUBPACKET_COUNT)
				for i in range(subpacket_count):
					subpacket = Packet(binary_str)
					binary_str = subpacket.remainder
					self.subpackets.append(subpacket)

			if self.type_id == TYPE_SUM:
				# Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets.
				# If they only have a single sub-packet, their value is the value of the sub-packet.
				self.value = sum([s.value for s in self.subpackets])
			elif self.type_id == TYPE_PRODUCT:
				# Packets with type ID 1 are product packets - their value is the result of multiplying together
				# the values of their sub-packets. If they only have a single sub-packet, their value is the value
				# of the sub-packet.
				self.value = 1
				for s in self.subpackets:
					self.value *= s.value
			elif self.type_id == TYPE_MINIMUM:
				# Packets with type ID 2 are minimum packets - their value is the minimum of the values
				# of their sub-packets.
				self.value = self.subpackets[0].value
				for s in self.subpackets:
					if s.value < self.value: self.value = s.value
			elif self.type_id == TYPE_MAXIMUM:
				# Packets with type ID 3 are maximum packets - their value is the maximum of the values
				# of their sub-packets.
				self.value = self.subpackets[0].value
				for s in self.subpackets:
					if s.value > self.value: self.value = s.value
			elif self.type_id == TYPE_GREATER_THAN:
				# Packets with type ID 5 are greater than packets - their value is 1 if the value of the first
				# sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0.
				self.value = 1 if self.subpackets[0].value > self.subpackets[1].value else 0
			elif self.type_id == TYPE_LESS_THAN:
				# Packets with type ID 6 are less than packets - their value is 1 if the value of the first
				# sub-packet is less than the value of the second sub-packet; otherwise, their value is 0.
				self.value = 1 if self.subpackets[0].value < self.subpackets[1].value else 0
			elif self.type_id == TYPE_EQUAL_TO:
				# Packets with type ID 7 are equal to packets - their value is 1 if the value of the first
				# sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0.
				self.value = 1 if self.subpackets[0].value == self.subpackets[1].value else 0
			else:
				self.value = 0

		self.remainder = binary_str
		self.version_sum = self.version + sum([s.version_sum for s in self.subpackets])

def hex2bin(hex_string):
	# Convert the hexadecimal string to a binary string.
	# Do this four bits (one hex character) at a time, to preserve
	# any leading zeroes and keep the output a multiple of four characters.
	binary_str = ''
	for ch in hex_string:
		binary_str += '{0:04b}'.format(int(ch, 16))
	return binary_str

def pop(binary_str, bits):
	# Remove the specified number of bits from the binary string, convert it
	# to an integer, and then return that and the remainder of the string.
	return (int(binary_str[:bits], 2), binary_str[bits:])

# Parse the transmission packets file
with open('day16_input.txt') as f:
	lines = [line.rstrip('\n') for line in f]

for line in lines:
	binary_str = hex2bin(line)
	p = Packet(binary_str)
	print('Part One: sum of all packet versions is {0}.'.format(p.version_sum))
	print('Part Two: value of the BITS transmission is {0}.'.format(p.value))