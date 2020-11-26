# Input definitions
BEFORE       = 0
INSTRUCTION  = 1
AFTER        = 2
BLANK        = 3

# Instruction definitions
INSTR_NAME   = 0
SRC_A        = 1
SRC_B        = 2
DEST         = 3

def addr(src_a, src_b, dest):
    registers[dest] = registers[src_a] + registers[src_b]

def addi(src_a, src_b, dest):
    registers[dest] = registers[src_a] + src_b

def mulr(src_a, src_b, dest):
    registers[dest] = registers[src_a] * registers[src_b]

def muli(src_a, src_b, dest):
    registers[dest] = registers[src_a] * src_b

def banr(src_a, src_b, dest):
    registers[dest] = registers[src_a] & registers[src_b]

def bani(src_a, src_b, dest):
    registers[dest] = registers[src_a] & src_b

def borr(src_a, src_b, dest):
    registers[dest] = registers[src_a] | registers[src_b]

def bori(src_a, src_b, dest):
    registers[dest] = registers[src_a] | src_b

def setr(src_a, src_b, dest):
    registers[dest] = registers[src_a]

def seti(src_a, src_b, dest):
    registers[dest] = src_a

def gtir(src_a, src_b, dest):
    # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    if src_a > registers[src_b]:
        registers[dest] = 1
    else:
        registers[dest] = 0

def gtri(src_a, src_b, dest):
    # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    if registers[src_a] > src_b:
        registers[dest] = 1
    else:
        registers[dest] = 0

def gtrr(src_a, src_b, dest):
    # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
    if registers[src_a] > registers[src_b]:
        registers[dest] = 1
    else:
        registers[dest] = 0

def eqir(src_a, src_b, dest):
    # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    if src_a == registers[src_b]:
        registers[dest] = 1
    else:
        registers[dest] = 0

def eqri(src_a, src_b, dest):
    # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    if registers[src_a] == src_b:
        registers[dest] = 1
    else:
        registers[dest] = 0

def eqrr(src_a, src_b, dest):
    # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
    if registers[src_a] == registers[src_b]:
        registers[dest] = 1
    else:
        registers[dest] = 0

instruction_list = [ addr,
                    addi,
                    mulr,
                    muli,
                    banr,
                    bani,
                    borr,
                    bori,
                    setr,
                    seti,
                    gtir,
                    gtri,
                    gtrr,
                    eqir,
                    eqri,
                    eqrr ]

# Map instruction names to their actual functions
instructions = {}
for instruction in instruction_list:
    instructions[instruction.__name__] = instruction

# Parse the program
with open('day19_input.txt') as f:
    input = [line.rstrip('\n') for line in f]

instruction_register = int(input[0].split()[1])
print 'Instruction Pointer bound to Register %d' % instruction_register

program = []
for i in range(0, len(input) - 1):
    program.append(input[i + 1].split())
    program[i][SRC_A] = int(program[i][SRC_A])
    program[i][SRC_B] = int(program[i][SRC_B])
    program[i][DEST] = int(program[i][DEST])

ip = 0
cycle_count = 0
registers = [1, 0, 0, 0, 0, 0]
r0 = registers[0]
profiler = {}
# Run the program!
while ip < len(program):
    output = 'ip=%d %s %s ' % (ip, registers, input[ip + 1])
    if cycle_count % 100000 == 0: print registers

    profiler[ip] = profiler.get(ip, 0) + 1
    line = program[ip]
    instruction = instructions[line[INSTR_NAME]]
    instruction(line[SRC_A], line[SRC_B], line[DEST])
    output += '%s' % registers
    registers[instruction_register] += 1
    ip = registers[instruction_register]

    cycle_count += 1
    if registers[0] is not r0:
        print '%d (+%d)' % (registers[0], registers[0] - r0)
        r0 = registers[0]

print 'Program terminated after %d cycles. Registers: %s' % (cycle_count, registers)

# By inspection: r0 will contain the sum of the factors of r1.
# For Part 1:
# r1 = 909
# sum(1, 3, 9, 101, 303, 909) = 1326

# For Part 2:
# set r0 = 1
# r1 = 10551309
# sum(1, 3, 41, 109, 123, 327, 787, 2361, 4469, 13407, 32267,
# 85783, 96801,257349, 3517103, 10551309) = 14562240
