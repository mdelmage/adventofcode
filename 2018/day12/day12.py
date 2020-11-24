GENERATIONS = 10000

with open('day12_input.txt') as f:
    input = [line.rstrip('\n') for line in f]

# Set up our initial state
state_str = input[0].split()[2]

rules = {}
for rule_idx in range(32):
    rule_str = input[rule_idx + 2].split(' => ')
    rules[rule_str[0]] = rule_str[1]

for gen in range(GENERATIONS):
    # pad to make room for next-gen pots
    state_str = '......' + state_str + '......'
    new_state_str = ''
    for chr in range(2, len(state_str) - 4):
        new_state_str += rules.get(state_str[chr: chr + 5], '.')

    state_str = new_state_str.rstrip('.')
    #print state_str

    # Calculate score for the current generation.
    # Index moves backwards two pots per generation
    index_pos = (gen+1) * -2
    score = 0
    for chr in state_str:
        if chr is '#': score += index_pos
        index_pos += 1

    if (gen+1) % 1000 == 0: print gen+1, score

# By inspection: score is 26,669 after 1000 generations and
# increases 26000 per 1000 generations.
print (26000 * ((50000000000 / 1000) - 1)) + 26669