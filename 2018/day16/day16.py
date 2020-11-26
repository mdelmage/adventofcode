import copy

# Input definitions
BEFORE       = 0
INSTRUCTION  = 1
AFTER        = 2
BLANK        = 3

# Instruction definitions
OPCODE       = 0
SRC_A        = 1
SRC_B        = 2
DEST         = 3

samples = []

def addr(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = registers[src_a] + registers[src_b]
    return result

def addi(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = registers[src_a] + src_b
    return result

def mulr(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = registers[src_a] * registers[src_b]
    return result

def muli(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = registers[src_a] * src_b
    return result

def banr(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = registers[src_a] & registers[src_b]
    return result

def bani(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = registers[src_a] & src_b
    return result

def borr(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = registers[src_a] | registers[src_b]
    return result

def bori(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = registers[src_a] | src_b
    return result

def setr(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = registers[src_a]
    return result

def seti(registers, src_a, src_b, dest):
    result = copy.deepcopy(registers)
    result[dest] = src_a
    return result

def gtir(registers, src_a, src_b, dest):
    # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    result = copy.deepcopy(registers)
    if src_a > registers[src_b]:
        result[dest] = 1
    else:
        result[dest] = 0
    return result

def gtri(registers, src_a, src_b, dest):
    # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    result = copy.deepcopy(registers)
    if registers[src_a] > src_b:
        result[dest] = 1
    else:
        result[dest] = 0
    return result

def gtrr(registers, src_a, src_b, dest):
    # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
    result = copy.deepcopy(registers)
    if registers[src_a] > registers[src_b]:
        result[dest] = 1
    else:
        result[dest] = 0
    return result

def eqir(registers, src_a, src_b, dest):
    # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    result = copy.deepcopy(registers)
    if src_a == registers[src_b]:
        result[dest] = 1
    else:
        result[dest] = 0
    return result

def eqri(registers, src_a, src_b, dest):
    # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    result = copy.deepcopy(registers)
    if registers[src_a] == src_b:
        result[dest] = 1
    else:
        result[dest] = 0
    return result

def eqrr(registers, src_a, src_b, dest):
    # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
    result = copy.deepcopy(registers)
    if registers[src_a] == registers[src_b]:
        result[dest] = 1
    else:
        result[dest] = 0
    return result

unknown_opcodes = [ addr,
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

known_opcodes = {}

# Parse all the samples for Part 1
with open('day16_input.txt') as f:
    input = [line.rstrip('\n') for line in f]
    i = 0
    while True:
        before      = input[(4 * i) + BEFORE]
        instruction = input[(4 * i) + INSTRUCTION]
        after       = input[(4 * i) + AFTER]
        blank       = input[(4 * i) + BLANK]
        i += 1

        # No delimiter found; we're done
        if len(before.split(': ')) is 1:
            break

        # Parse 'Before' string
        before = before.split(': ')[1].replace('[', '').replace(']', '')
        before_regs = []
        for part in before.split(','):
            before_regs.append(int(part))

        # Parse instructions
        instruction_parts = []
        for part in instruction.split():
            instruction_parts.append(int(part))

        # Parse 'After' string (yes, the delimiter has two spaces)
        after = after.split(':  ')[1].replace('[', '').replace(']', '')
        after_regs = []
        for part in after.split(','):
            after_regs.append(int(part))

        samples.append([before_regs, instruction_parts, after_regs])

# Run the samples through each instruction and find matches
sample_characterization = {}
first_pass = True
while len(unknown_opcodes) > 0:
    for sample in samples:
        before = sample[BEFORE]
        opcode = sample[INSTRUCTION][OPCODE]
        src_a = sample[INSTRUCTION][SRC_A]
        src_b = sample[INSTRUCTION][SRC_B]
        dest = sample[INSTRUCTION][DEST]
        after = sample[AFTER]

        # Skip known codes while we figure out the unknowns
        if not first_pass and opcode in known_opcodes:
            continue

        # See if there is a sample that is provably from a unique instruction.
        # Map the sample's opcode to that instruction.
        matches = 0
        for instr in unknown_opcodes:
            if after == instr(before, src_a, src_b, dest):
                matches += 1
                matched_instr = instr
                matched_sample = sample
        sample_characterization[matches] = sample_characterization.get(matches, 0) + 1
        if matches is 1: known_opcodes[opcode] = matched_instr

    # Remove known opcodes from the search space
    for opcode in known_opcodes:
          if known_opcodes[opcode] in unknown_opcodes:
             unknown_opcodes.remove(known_opcodes[opcode])

    # Part 1: Report how many samples had three+ matches on the initial pass
    if first_pass:
        print sample_characterization
        triple_matches = 0
        for key in sample_characterization:
            if key >= 3: triple_matches += sample_characterization[key]
        print '%d samples behave like three or more opcodes.' % triple_matches
        first_pass = False

for opcode in known_opcodes:
    print 'opcode %d --> %s' % (opcode, known_opcodes[opcode].__name__)


# Part 2: Run a program!
with open('day16_input2.txt') as f:
    program = [line.rstrip('\n') for line in f]

registers = [0, 0, 0, 0]
for instruction in program:
    instruction_parts = []
    for part in instruction.split():
        instruction_parts.append(int(part))

    opcode = instruction_parts[OPCODE]
    src_a = instruction_parts[SRC_A]
    src_b = instruction_parts[SRC_B]
    dest = instruction_parts[DEST]
    registers = known_opcodes[opcode](registers, src_a, src_b, dest)

print 'After %d instructions: %s' % (len(program), registers)
