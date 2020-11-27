from collections import namedtuple
import sys

def dist(bot1, bot2):
    return (abs(bot1.x - bot2.x) + abs(bot1.y - bot2.y) + abs(bot1.z - bot2.z))

def range_remaining(spot, bot):
    return bot.r - dist(spot, bot)

# Parse the nanobots file
with open('day23_input.txt') as f:
    input = [line.rstrip('\n') for line in f]

nanobots = []
for nanobot in input:
    tokens = nanobot.replace('pos=<', '').replace('>', '').replace(', r=', ',').split(',')
    nanobot = namedtuple('Nanobot', 'x y z r')
    nanobot.x = int(tokens[0])
    nanobot.y = int(tokens[1])
    nanobot.z = int(tokens[2])
    nanobot.r = int(tokens[3])
    nanobots.append(nanobot)

strongest_bot = nanobots[0]
for bot in nanobots:
    if bot.r > strongest_bot.r: strongest_bot = bot

bots_in_range = 0
for bot in nanobots:
    if dist(bot, strongest_bot) <= strongest_bot.r: bots_in_range += 1

print 'Strongest bot is %d,%d,%d r=%d and has %d/%d nanobots in range, including itself.' % (strongest_bot.x, strongest_bot.y, strongest_bot.z, strongest_bot.r, bots_in_range, len(nanobots))


x_min = 0
x_max = 0
y_min = 0
y_max = 0
z_min = 0
z_max = 0
r_min = 10000000000000000000000000000000
r_max = 0
for bot in nanobots:
    if (bot.x - bot.r) < x_min: x_min = (bot.x - bot.r)
    if (bot.x + bot.r) > x_max: x_max = (bot.x + bot.r)
    if (bot.y - bot.r) < y_min: y_min = (bot.y - bot.r)
    if (bot.y + bot.r) > y_max: y_max = (bot.y + bot.r)
    if (bot.z - bot.r) < z_min: z_min = (bot.z - bot.r)
    if (bot.z + bot.r) > z_max: z_max = (bot.z + bot.r)
    if bot.r < r_min: r_min = bot.r
    if bot.r > r_max: r_max = bot.r
print '%d-%d, %d-%d, %d-%d, %d-%d' % (x_min, x_max, y_min, y_max, z_min, z_max, r_min, r_max)

x_max_idx = 0
x_max_range = 0
x = x_min
while x <= x_max:
    bots_in_range = 0
    for bot in nanobots:
        if (x >= bot.x and x <= bot.x + bot.r) or (x <= bot.x and x >= bot.x - bot.r): bots_in_range += 1
    if bots_in_range > x_max_range:
        x_max_idx = x
        x_max_range = bots_in_range
    x += r_min
print 'Mostest x was %d with %d connections.' % (x_max_idx, x_max_range)

y_max_idx = 0
y_max_range = 0
y = y_min
while y <= y_max:
    bots_in_range = 0
    for bot in nanobots:
        if (y >= bot.y and y <= bot.y + bot.r) or (y <= bot.y and y >= bot.y - bot.r): bots_in_range += 1
    if bots_in_range > y_max_range:
        y_max_idx = y
        y_max_range = bots_in_range
    y += r_min
print 'Mostest y was %d with %d connections.' % (y_max_idx, y_max_range)


z_max_idx = 0
z_max_range = 0
z = z_min
while z <= z_max:
    bots_in_range = 0
    for bot in nanobots:
        if (z >= bot.z and z <= bot.z + bot.r) or (z <= bot.z and z >= bot.z - bot.r): bots_in_range += 1
    if bots_in_range > z_max_range:
        z_max_idx = z
        z_max_range = bots_in_range
    z += r_min
print 'Mostest z was %d with %d connections.' % (z_max_idx, z_max_range)


current_pos = namedtuple('pos', 'x y z')
current_pos.x = 0
current_pos.y = 0
current_pos.z = 0

closest_in_range_bot = None
closest_in_range_delta = sys.maxint
closest_beyond_range_bot = None
closest_beyond_range_delta = -sys.maxint + 100

while closest_in_range_delta + closest_beyond_range_delta > 0:
    closest_in_range_bot = None
    closest_in_range_delta = sys.maxint
    closest_beyond_range_bot = None
    closest_beyond_range_delta = -sys.maxint + 100
    in_range = 0
    for bot in nanobots:
        range = range_remaining(current_pos, bot)
        if range >= 0:
            in_range += 1
            if range < closest_in_range_delta:
                closest_in_range_delta = range
                closest_in_range_bot = bot
        elif range < 0 and range > closest_beyond_range_delta:
            closest_beyond_range_delta = range
            closest_beyond_range_bot = bot
    print 'I am in range of %d nanobots:' % in_range
    print 'I could move %d and be in range of all bots.' % closest_in_range_delta
    print 'I have to move %d to be in range of another bot.' % (-1 * closest_beyond_range_delta)

    if closest_in_range_delta + closest_beyond_range_delta > 0:
        delta = namedtuple('pos', 'x y z')
        delta.x = current_pos.x - closest_beyond_range_bot.x
        delta.y = current_pos.y - closest_beyond_range_bot.y
        delta.z = current_pos.z - closest_beyond_range_bot.z
        total_delta = delta.x + delta.y + delta.z
        print '\tClosest beyond-range bot is (%d,%d,%d) away...' % (delta.x, delta.y, delta.z)
        move = namedtuple('pos', 'x y z')
        move_dist = -1 * closest_beyond_range_delta
        move.x = int(delta.x * float(move_dist) / total_delta)
        move.y = int(delta.y * float(move_dist) / total_delta)
        move.z = int(delta.z * float(move_dist) / total_delta)
        if move.x + move.y + move.z < move_dist: move.z += 1
        
        current_pos.x += move.x
        current_pos.y += move.y
        current_pos.z += move.z
        print '\tMoving %d (%d,%d,%d) to (%d,%d,%d)...' % (move.x + move.y + move.z, move.x, move.y, move.z, current_pos.x, current_pos.y, current_pos.z)

chattiest_bot = nanobots[0]
chattiest_bot_num = 0
for bot1 in nanobots:
    bots_in_range = 0
    for bot2 in nanobots:
        if dist(bot1, bot2) <= bot2.r: bots_in_range += 1
    if bots_in_range > chattiest_bot_num:
        chattiest_bot_num = bots_in_range
        chattiest_bot = bot1
print 'Chattiest bot is %d,%d,%d r=%d and has %d/%d nanobots in range, including itself.' % (chattiest_bot.x, chattiest_bot.y, chattiest_bot.z, chattiest_bot.r, chattiest_bot_num, len(nanobots))

chattiest_bot.x = x_max_idx
chattiest_bot.y = y_max_idx
chattiest_bot.z = z_max_idx

best_spot = None
max_range = 0
pct = 10000
if True: #for pct in range(10150, 10250):
    spot = namedtuple('pos', 'x y z')
    spot.x = int(chattiest_bot.x * pct / 10000)
    spot.y = int(chattiest_bot.y * pct / 10000)
    spot.z = int(chattiest_bot.z * pct / 10000)
    bots_in_range = 0
    for bot in nanobots:
        if dist(spot, bot) <= bot.r: bots_in_range += 1
    if bots_in_range > max_range:
        max_range = bots_in_range
        best_spot = spot
print '(%d,%d,%d) has %d bots in range!' % (best_spot.x, best_spot.y, best_spot.z, max_range)
print '%d' % (best_spot.x + best_spot.y + best_spot.z)
sys.exit()
print '%d bots in range:' % len(in_range(best_spot))
for bot in in_range(best_spot):
    print '\tthis bot in range by %d' % (bot.r - dist(best_spot, bot))
print '%d bots beyond range:' % len(beyond_range(best_spot))
for bot in beyond_range(best_spot):
    print '\tthis bot beyond range by %d' % (dist(best_spot, bot) - bot.r)
least_in_range_bot = closest_to_beyond_range(best_spot)
least_beyond_range_bot = closest_to_in_range(best_spot)
print 'closest bot to beyond range: within range by %d' % (least_in_range_bot.r - dist(best_spot, least_in_range_bot))
print 'closest bot to in range: out of range by %d' % (dist(best_spot, least_beyond_range_bot) - least_beyond_range_bot.r)

# Parse the nanobots file
with open('day23_input.txt') as f:
    input = [line.rstrip('\n') for line in f]

x_min = 0
x_max = 0
y_min = 0
y_max = 0
z_min = 0
z_max = 0
nanobots = []
for nanobot in input:
    tokens = nanobot.replace('pos=<', '').replace('>', '').replace(', r=', ',').split(',')
    nanobot = namedtuple('Nanobot', 'x y z r')
    nanobot.x = int(tokens[0])
    nanobot.y = int(tokens[1])
    nanobot.z = int(tokens[2])
    nanobot.r = int(tokens[3])
    if (nanobot.x - nanobot.r) < x_min: x_min = (nanobot.x - nanobot.r)
    if (nanobot.x + nanobot.r) > x_max: x_max = (nanobot.x + nanobot.r)
    if (nanobot.y - nanobot.r) < y_min: y_min = (nanobot.y - nanobot.r)
    if (nanobot.y + nanobot.r) > y_max: y_max = (nanobot.y + nanobot.r)
    if (nanobot.z - nanobot.r) < z_min: z_min = (nanobot.z - nanobot.r)
    if (nanobot.z + nanobot.r) > z_max: z_max = (nanobot.z + nanobot.r)
    nanobots.append(nanobot)

giant_grid = {}
for x in range(5, 21):
    for y in range(5, 21):
        for z in range(5, 21):
            loc = namedtuple('Nanobot', 'x y z r')
            loc.x = x
            loc.y = y
            loc.z = z

            bots_in_range = 0
            for bot in nanobots:
                if dist(loc, bot) <= bot.r: bots_in_range += 1
            giant_grid[(x, y, z)] = bots_in_range

connectedest_point = sorted(giant_grid, key=giant_grid.get)[len(giant_grid) - 1]
print '%s: in range of %d nanobots' % (connectedest_point, giant_grid[connectedest_point])
