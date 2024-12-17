#!/usr/bin/env python
# -*- coding: utf-8 -*-

def combo(operand):
    # Combo operands 0 through 3 represent literal values 0 through 3.
    if operand in [0, 1, 2, 3]: return operand

    # Combo operand 4 represents the value of register A.
    if operand == 4: return registers['A']

    # Combo operand 5 represents the value of register B.
    if operand == 5: return registers['B']

    # Combo operand 6 represents the value of register C.
    if operand == 6: return registers['C']

    # Combo operand 7 is reserved and will not appear in valid programs.

def run():
    # A number called the instruction pointer identifies the position in the program
    # from which the next opcode will be read; it starts at 0, pointing at the first 3-bit number in the program.
    ip = 0

    output = ''

    # If the computer tries to read an opcode past the end of the program, it instead halts.
    while ip < len(program):
        # The computer knows eight instructions, each identified by a 3-bit number (called the instruction's opcode).
        # Each instruction also reads the 3-bit number after it as an input; this is called its operand.
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:
            # The adv instruction (opcode 0) performs division. The numerator is the value in the A register.
            # The denominator is found by raising 2 to the power of the instruction's combo operand.
            # The result of the division operation is truncated to an integer and then written to the A register.
            numerator = registers['A']
            denominator = 2 ** combo(operand)
            registers['A'] = numerator // denominator
        elif opcode == 1:
            # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's
            # literal operand, then stores the result in register B.
            registers['B'] ^= operand
        elif opcode == 2:
            # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
            # (thereby keeping only its lowest 3 bits), then writes that value to the B register.
            registers['B'] = combo(operand) % 8
        elif opcode == 3:
            # The jnz instruction (opcode 3) does nothing if the A register is 0.
            # However, if the A register is not zero, it jumps by setting the instruction pointer to the value
            # of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2
            # after this instruction.
            if registers['A'] != 0:
                ip = operand - 2
        elif opcode == 4:
            # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores
            # the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
            registers['B'] ^= registers['C']
        elif opcode == 5:
            # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs
            # that value. (If a program outputs multiple values, they are separated by commas.)
            output += '{0},'.format(combo(operand) % 8)
        elif opcode == 6:
            # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result
            # is stored in the B register. (The numerator is still read from the A register.)
            numerator = registers['A']
            denominator = 2 ** combo(operand)
            registers['B'] = numerator // denominator
        elif opcode == 7:
            # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result
            # is stored in the C register. (The numerator is still read from the A register.)
            numerator = registers['A']
            denominator = 2 ** combo(operand)
            registers['C'] = numerator // denominator

        # Except for jump instructions, the instruction pointer increases by 2 after each instruction is processed
        # (to move past the instruction's opcode and its operand).
        ip += 2

    return output[:-1]

# Parse the program and register contents.
with open('day17_input.txt') as f:
    program_input = [line.rstrip('\n') for line in f]
    registers = {}
    registers['A'] = int(program_input[0].split(': ')[1])
    registers['B'] = int(program_input[1].split(': ')[1])
    registers['C'] = int(program_input[2].split(': ')[1])
    program_str = program_input[4].split(': ')[1]
    program = [int(n) for n in program_str.split(',')]

# Using the information provided by the debugger, initialize the registers to the given values,
# then run the program. Once it halts, what do you get if you use commas to join the values it output into a single string?
output = run()
print('Part One: The program output is {0}.'.format(output))

a_guess = 0
while True:
    if a_guess % 100000 == 0: print(a_guess)
    registers['A'] = a_guess
    registers['B'] = int(program_input[1].split(': ')[1])
    registers['C'] = int(program_input[2].split(': ')[1])

    output = run()
    if output == program_str: break
    a_guess += 1

print('Part Two: The correct value for Register A for the program to self-clone is {0}.'.format(a_guess))
