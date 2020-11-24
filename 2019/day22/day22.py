#!/usr/bin/python
# coding: utf-8

CMD_NEW_STACK = "deal into new stack"
CMD_INCREMENT = "deal with increment"
CMD_CUT       = "cut"

IDENTITY_LCF = (1,0)

def compose_lcf(current_tuple, next_tuple, n):
    #print "\tcompose_lcf({0}, {1}, {2}".format(current_tuple, next_tuple, n)
    return ((current_tuple[0] * next_tuple[0]) % n, ((current_tuple[1] * next_tuple[0]) + next_tuple[1]) % n)

def compose_lcf_pow(f, k, n):
    #print "compose_lcf_pow({0}, {1}, {2}".format(f, k, n)
    g = (1, 0)
    while k > 0:
        if k % 2 == 1:
            g = compose_lcf(g, f, n)
        k /= 2
        f = compose_lcf(f, f, n)
    return g

def evaluate_lcf(eval_tuple, initial_value, n):
    #print "evaluate_lcf({0}, {1}, {2}".format(eval_tuple, initial_value, n)
    return ((eval_tuple[0] * initial_value) + eval_tuple[1]) % n

def lcf_exp(x, n, m):
    if n == 0: return 1

    t = lcf_exp(x, n / 2, m)

    if n % 2 == 0:
        return (t * t) % m
    else:
        return (t * t * x) % m

def div_mod(a, b, m):
    return (a * modular_multiplicative_inverse(b, m)) % m

def modular_multiplicative_inverse(x, m):
    return lcf_exp(x, m - 2, m)

DECK_SIZE = 10007
TARGET_CARD = 2019
print "\r\n*** Little Deck ({0}) ***".format(DECK_SIZE)

# Open input file
with open("day22.txt", "r") as f:
    lcf = IDENTITY_LCF
    for line in f:
        # print line.strip()
        if CMD_NEW_STACK in line:
            line_lcf = (-1, -1)
        elif CMD_INCREMENT in line:
            increment = int(line[len(CMD_INCREMENT):])
            line_lcf = (increment, 0)
        elif CMD_CUT in line:
            cut = int(line[len(CMD_CUT):])
            line_lcf = (1, -cut)

        lcf = compose_lcf(lcf, line_lcf, DECK_SIZE)

    # print lcf
    # pos = TARGET_CARD
    # k = 1
    # for i in range(k):
    #     pos = evaluate_lcf(lcf, pos, DECK_SIZE)
    #     print "{0}: Found card {1} at position {2}!".format(i, TARGET_CARD, pos)

    k = 1
    pos = TARGET_CARD
    A = lcf[0]
    B = lcf[1]
    m = DECK_SIZE

    lcf_pow = compose_lcf_pow(lcf, k, m)
    pos = evaluate_lcf(lcf_pow, pos, DECK_SIZE)
    print "LCF^{0}: Found card {1} at position {2}!".format(k, TARGET_CARD, pos)

    card = div_mod(pos - lcf_pow[1], lcf_pow[0], DECK_SIZE)
    print "LCF^-{0}: Position {1} has card {2}!".format(k, pos, card)

DECK_SIZE = 119315717514047
SHUFFLE_COUNT = 101741582076661
TARGET_POS = 2020
print "\r\n*** Giant Deck ({0}) ***".format(DECK_SIZE)

# Open input file
with open("day22.txt", "r") as f:
    lcf = IDENTITY_LCF
    for line in f:
        # print line.strip()
        if CMD_NEW_STACK in line:
            line_lcf = (-1, -1)
        elif CMD_INCREMENT in line:
            increment = int(line[len(CMD_INCREMENT):])
            line_lcf = (increment, 0)
        elif CMD_CUT in line:
            cut = int(line[len(CMD_CUT):])
            line_lcf = (1, -cut)

        lcf = compose_lcf(lcf, line_lcf, DECK_SIZE)

    k = SHUFFLE_COUNT
    pos = TARGET_POS
    A = lcf[0]
    B = lcf[1]
    m = DECK_SIZE

    lcf_pow = compose_lcf_pow(lcf, k, m)
    card = div_mod(pos - lcf_pow[1], lcf_pow[0], DECK_SIZE)
    print "LCF^-{0}: Position {1} has card {2}!".format(k, pos, card)
    