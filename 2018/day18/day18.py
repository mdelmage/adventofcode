OPEN        = '.'
TREES       = '|'
LUMBERYARD  = '#'

def print_area():
    global size
    for y in range(size):
        line = ''
        for x in range(size):
            line += area[(x, y)]
        print line
    print ''

def convert(current, trees, lumberyards):
    if current is OPEN:
        if trees >= 3:
            return TREES
        else:
            return OPEN
    elif current is TREES:
        if lumberyards >= 3:
            return LUMBERYARD
        else:
            return TREES
    else:
        if trees > 0 and lumberyards > 0:
            return LUMBERYARD
        else:
            return OPEN

def get_neighbors(x, y):
    neighbors = {}

    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:
            if (i, j) not in area or (i == x and j == y):
                neighbors[OPEN] = neighbors.get(OPEN, 0) + 1
            else:
                neighbors[area[(i, j)]] = neighbors.get(area[(i, j)], 0) + 1

    return neighbors

def tick():
    global area
    area_new = {}
    for (x, y) in area:
        neighbors = get_neighbors(x, y)
        area_new[(x, y)] = convert(area[(x, y)], neighbors.get(TREES, 0), neighbors.get(LUMBERYARD, 0))

    area = area_new

area = {}
# Build the lumber area
with open('day18_input.txt') as f:
    y = 0
    for line in f:
        x = 0
        size = len(line.rstrip('\n'))
        for chr in line.rstrip('\n'):
            area[(x, y)] = chr
            x += 1
        y += 1

print_area()
i = 0
while True:
    tick()
    i += 1

    if i % 1000 is 0 or i == 10:
        trees = 0
        lumberyards = 0
        for square in area:
            if area[square] is TREES: trees += 1
            if area[square] is LUMBERYARD: lumberyards += 1

        print '%05d: Total resource value = %d wooded acres and %d lumberyards = %d' % (i, trees, lumberyards, trees * lumberyards)

# By inspection: today's input has a 7000-tick resonance.
# 1000000000 % 7000 is 1000, so the value after 1000000000 ticks
# is the same as after 1000 ticks.
