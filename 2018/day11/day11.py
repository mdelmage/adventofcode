import time

GRID = 2866
GRID_SIZE = 300

def power_level(cell, grid):
    x = cell[0]
    y = cell[1]
    rack_id = x + 10
    power = rack_id * y
    power += grid
    power *= rack_id
    power = (power / 100) % 10
    power -= 5
    return power

# Calculate the delta power of one larger grid size
#
# For example, if we've already calculated the power of a 3x3 grid
# (marked with '3' below), add a row and column to make it a 4x4 grid:
#
# 3334
# 3334
# 3334
# 4444
#
def power_delta(cell, grid, size):
    power = 0
    for y in range(size):
        power += power_level((cell[0] + size - 1, cell[1] + y), grid)
    for x in range(size - 1):
        power += power_level((cell[0] + x, cell[1] + size - 1), grid)
    return power

max_power = 0
max_coord = None
timestamp = time.time()
for y in range(GRID_SIZE):
    print y
    timestamp = time.time()
    for x in range(GRID_SIZE):
        current_power = 0
        # for search_size in range(3 + 1), for Part A
        for search_size in range(min(GRID_SIZE - x, GRID_SIZE - y)):
            current_power += power_delta((x, y), GRID, search_size)
            if current_power > max_power:
                max_power = current_power
                max_coord = (x, y, search_size)

print "max power is %d at %s" % (max_power, max_coord)

