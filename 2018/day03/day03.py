fabric = {}
dupe_squares = 0

with open('day03_input.txt') as f:
    claims = [line.rstrip('\n') for line in f]

for claim in claims:
    # aww yeah, quick and dirty tokenize
    tokens = claim.replace(' ', '').replace('@', ',').replace(':', ',').replace('x', ',').split(',')
    start_x = int(tokens[1])
    start_y = int(tokens[2])
    width = int(tokens[3])
    height = int(tokens[4])
    for x in range(start_x, start_x + width):
        for y in range(start_y, start_y + height):
            fabric[x, y] = fabric.get((x, y), 0) + 1
            if fabric[x, y] is 2:
                dupe_squares = dupe_squares + 1

print "Duplicate square inches: %d" % dupe_squares

for claim in claims:
    # aww yeah, quick and dirty tokenize AGAIN
    tokens = claim.replace(' ', '').replace('@', ',').replace(':', ',').replace('x', ',').split(',')
    claim_dupes = 0
    start_x = int(tokens[1])
    start_y = int(tokens[2])
    width = int(tokens[3])
    height = int(tokens[4])
    for x in range(start_x, start_x + width):
        for y in range(start_y, start_y + height):
            if fabric[x, y] > 1: claim_dupes = claim_dupes + 1
    if claim_dupes is 0: print 'No overlaps: %s' % claim
