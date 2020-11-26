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
    #print '%d >? %d' % (src_a, registers[src_b])
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
    #print '%d >? %d' % (registers[src_a], registers[src_b])
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

r1_check = {}
last_good_r1 = None
def eqrr(src_a, src_b, dest):
    global last_good_r1
    r1_check[registers[src_a]] = r1_check.get(registers[src_a], 0) + 1
    if r1_check[registers[src_a]] > 1:
        print 'r1 duplicate at %06X; last non-dupe was %06X' % (registers[src_a], last_good_r1)
        return
    last_good_r1 = registers[src_a]

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
with open('day21_input.txt') as f:
    input = [line.rstrip('\n') for line in f]

instruction_register = int(input[0].split()[1])
print 'Instruction Pointer bound to Register %d' % instruction_register

program = []
for i in range(0, len(input) - 1):
    program.append(input[i + 1].split())
    program[i][SRC_A] = int(program[i][SRC_A])
    program[i][SRC_B] = int(program[i][SRC_B])
    program[i][DEST] = int(program[i][DEST])

if True:
    ip = 0
    cycle_count = 0
    registers = [0, 0, 0, 0, 0, 0]
    r0 = registers[0]
    profiler = {}
    # Run the program!
    while ip < len(program):
        profiler[ip] = profiler.get(ip, 0) + 1
        line = program[ip]
        instruction = instructions[line[INSTR_NAME]]
        instruction(line[SRC_A], line[SRC_B], line[DEST])

        registers[instruction_register] += 1
        ip = registers[instruction_register]

        cycle_count += 1
        if registers[0] is not r0:
            print '%d (+%d)' % (registers[0], registers[0] - r0)
            r0 = registers[0]

    print 'Program terminated after %d cycles. Registers: %s' % (cycle_count, registers)

# Part 1: By inspection, the eqrr at the end of the program (termination check)
# wants r0 to be equal to 16311888 after the first loop.

# Part 2: By inspection, the eqrr (termination check) value starts looping with
# a period of 1000. The last unique value to pass through the check is 1413889.
# Program converted to C to speed it up because I couldn't see the trick to making
# it faster in Python, although the Python version does finish in an hour or so.
