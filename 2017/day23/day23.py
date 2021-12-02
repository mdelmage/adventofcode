#!/usr/bin/env python
# -*- coding: utf-8 -*-

CMD_SET = 'set'
CMD_SUBTRACT = 'sub'
CMD_MULTIPLY = 'mul'
CMD_JUMP_IF_NOT_ZERO = 'jnz'

class Program(object):
    def __init__(self, instructions):
        self.pc = 0
        self.mul_count = 0
        self.registers = {}
        self.instructions = instructions

    def val(self, s):
        if s.isalpha():
            # It's a register name; dereference it
            return self.registers.get(s, 0)
        else:
            # It's a scalar, return that
            return int(s)

    def run(self):
        while self.pc < len(self.instructions):
            cmd = self.instructions[self.pc][0]
            arg1 = self.instructions[self.pc][1]
            if len(self.instructions[self.pc]) == 3: arg2 = self.instructions[self.pc][2]

            if cmd == CMD_SET:
                self.registers[arg1] = self.val(arg2)
            elif cmd == CMD_SUBTRACT:
                self.registers[arg1] = self.val(arg1) - self.val(arg2)
            elif cmd == CMD_MULTIPLY:
                self.registers[arg1] = self.val(arg1) * self.val(arg2)
                self.mul_count += 1
            elif cmd == CMD_JUMP_IF_NOT_ZERO:
                if self.val(arg1) != 0:
                    self.pc += self.val(arg2) - 1
            self.pc += 1

# Parse the program file
with open('day23_input.txt') as f:
    instructions = [line.rstrip('\n').split() for line in f]

# If you run the program (your puzzle input), how many times is the mul instruction invoked?
p = Program(instructions)
p.run()
print 'Part One: mul instruction was invoked {0} times.'.format(p.mul_count)

# By inspection: the program is designed to count how many non-prime integers are in
# a set of 1000 numbers. Here we just copy the relevant parameters out of our specific input
# (adjust yours as necessary).
RANGE_LOW = 109300
RANGE_HIGH = 126300
INCREMENT = 17

nonprime_count = 0
for potential_prime in range(RANGE_LOW, RANGE_HIGH + 1, INCREMENT):
    matched = False
    for factor in range(2, int(potential_prime ** 0.5)):
        if potential_prime % factor == 0:
            matched = True
            break
    if matched: nonprime_count += 1
print 'Part Two: Register h contains the value {0} after program termination.'.format(nonprime_count)