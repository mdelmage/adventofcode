#!/usr/bin/env python
# -*- coding: utf-8 -*-

random_ints = [
18283234231373,
143371719012,
18746944625405,
4850111356957,
7066956166684,
12882332524514,
1681885316546,
5573742091346,
14803762405008,
6751535573163,
7388443505139,
14468038367372,
15408832572421,
16178252555987,
8834783776697,
9121262198560,
8161171876833,
16242177876820,
4554007602652,
16306328165765
]

# By inspection of the puzzle input.
BIT_WIDTH = 46

def connect_nets(addend1=None, addend2=None):
    # If provided custom addends, use those instead.
    if addend1 and addend2:
        nets_local = {}
        for bit in range(BIT_WIDTH):
            nets_local['x{0:02}'.format(bit)] = addend1 & 1
            nets_local['y{0:02}'.format(bit)] = addend2 & 1
            addend1 //= 2
            addend2 //= 2
    else:
        nets_local = nets.copy()

    # Loop through all the gates and see if there's any substitutions to be made.
    # If so, iterate again.
    done = False
    while not done:
        done = True
        for (in1, in2, func, output) in gates:
            if in1 in nets_local and in2 in nets_local and output not in nets_local:
                if func == 'AND':
                    nets_local[output] = nets_local[in1] and nets_local[in2]
                    done = False
                elif func == 'OR':
                    nets_local[output] = nets_local[in1] or nets_local[in2]
                    done = False
                elif func == 'XOR':
                    nets_local[output] = nets_local[in1] ^ nets_local[in2]
                    done = False

    # Reassemble the nets into integers.
    x_value = 0
    for digit in sorted([n for n in nets_local if n[0] == 'x'], reverse=True):
        x_value *= 2
        x_value += nets_local[digit]

    y_value = 0
    for digit in sorted([n for n in nets_local if n[0] == 'y'], reverse=True):
        y_value *= 2
        y_value += nets_local[digit]

    z_value = 0
    for digit in sorted([n for n in nets_local if n[0] == 'z'], reverse=True):
        z_value *= 2
        z_value += nets_local[digit]

    return (x_value, y_value, z_value)

# Sample a variety of large pseudo-random integers and figure out the least significant bit
# that contains an error in the addition operation.
def lowest_error_bit():
    error = 0
    for i in range(len(random_ints)):
        x, y, z = connect_nets(random_ints[i], random_ints[(i + 1) % len(random_ints)])
        error |= (z ^ (x + y))

    # To simplify the comparisons, if there is no error and the operation is correct, return a bit
    # that is higher than the width of the machine.
    error_str = '1{' + '0:0{0}b'.format(BIT_WIDTH) + '}'
    error_str = error_str.format(error)
    error_bit = 0
    while error_str[-1] == '0':
        error_bit += 1
        error_str = error_str[:-1]
    return error_bit

# Swap outputs between gates to test whether we've improved the circuit.
def swap(out1, out2):
    global gates
    gates_new = []
    for in1, in2, op, out in gates:
        if out == out1:
            gates_new.append((in1, in2, op, out2))
        elif out == out2:
            gates_new.append((in1, in2, op, out1))
        else:
            gates_new.append((in1, in2, op, out))
    gates = gates_new

def bit_level(output):
    # Skip end outputs -- we already know what level they are.
    if output[0] in ['x', 'y', 'z']: return int(output[1:])

    # String-replace all outputs with their respective inputs until no more substitions are left.
    done = False
    while not done:
        done = True
        for in1, in2, op, out in gates:
            if out in output:
                output = output.replace(out, '{0} {1}'.format(in1, in2))
                done = False

    # The level of an output is the highest output bit that it affects.
    for l in range(BIT_WIDTH, -1, -1):
        if '{0:02}'.format(l) in output:
            return l

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
outputs = []
for inputs, output in [x.split(' -> ') for x in gates_input]:
    in1, op, in2 = inputs.split()
    gates.append((in1, in2, op, output))
    outputs.append(output)

# Evaluate the output of each level.
bit_levels = {}
for o in outputs:
    l = bit_level(o)
    if l not in bit_levels: bit_levels[l] = []
    bit_levels[l].append(o)

# Simulate the system of gates and wires. What decimal number does it output on the wires starting with z?
x, y, z = connect_nets()
print('Part One: The decimal output of the z wires is {0}.'.format(z))

# Based on forensic analysis of scuff marks and scratches on the device, you can tell that there are exactly
# four pairs of gates whose output wires have been swapped. (A gate can only be in at most one such pair;
# no gate's output was swapped multiple times.)
swaps = set()
while len(swaps) < 8:
    # Generate a list of potential swaps to make (single pairs).
    # To optimize the search space, only consider outputs that affect the lowest bit that's showing an error.
    error_lsb = lowest_error_bit()

    # Check every pair to see if the addition is correct for more bits. If so, add the pair to our swaps list.
    for a, b in [(a, b) for a in bit_levels[error_lsb] for b in bit_levels[error_lsb] if a != b]:
        swap(a, b)
        if lowest_error_bit() > error_lsb:
            swaps.add(a)
            swaps.add(b)
            break
        swap(a, b)

# Your system of gates and wires has four pairs of gates which need their output wires swapped - eight wires in total.
# Determine which four pairs of gates need their outputs swapped so that your system correctly performs addition;
# what do you get if you sort the names of the eight wires involved in a swap and then join those names with commas?
solution_str = ''.join(['{0},'.format(s) for s in sorted(swaps)])[:-1]
print('Part Two: The sorted list of swapped wires is {0}.'.format(solution_str))