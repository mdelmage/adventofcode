#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Parse the gate connections and initial wire values.
with open('day24_input.txt') as f:
    gates_and_wires = [line.rstrip('\n') for line in f]
    separator = gates_and_wires.index('')
    wires = gates_and_wires[:separator]
    gates_input = gates_and_wires[separator + 1:]

nets = {}
for wire, value in [x.split(': ') for x in wires]:
    nets[wire] = int(value)

gates = []
for inputs, output in [x.split(' -> ') for x in gates_input]:
    in1, func, in2 = inputs.split()
    gates.append((in1, in2, func, output))

while True:
    done = True
    for (in1, in2, func, output) in gates:
        if in1 in nets and in2 in nets and output not in nets:
            #print('i should do something about {0} and {1} to light up {2}'.format(in1, in2, output))
            if func == 'AND':
                nets[output] = nets[in1] and nets[in2]
                done = False
            elif func == 'OR':
                nets[output] = nets[in1] or nets[in2]
                done = False
            elif func == 'XOR':
                nets[output] = nets[in1] ^ nets[in2]
                done = False
    if done: break

value = 0
for digit in sorted([n for n in nets if n[0] == 'z'], reverse=True):
    value *= 2
    value += nets[digit]

print(value)

# Find all the sets of three inter-connected computers.
# How many contain at least one computer with a name that starts with t?
#print('Part One: There are {0} sets of interconnected computers with at least one \'t\'.'.format(len(groups)))