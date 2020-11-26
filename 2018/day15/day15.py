import copy

ATTACK_GOBLIN = 3
ATTACK_ELF = 3
HIT_POINTS = 200
BIG_NUM = 999

PART2 = True

# Note: locations are all indexed by (y,x) so they sort nicely into 'reading order'

class Warrior(object):
    def __init__(self, y, x, chr):
        self._pos = (y, x)
        self._hp = HIT_POINTS
        warriors[self._pos] = self

    def move(self):
        in_range = None
        reachable = None
        len_path = None
        min_path = None
        travel_square = None
        
        # Step 1: Determine if we are already 'in range' of an enemy
        if len(self.adjacent_enemies()) > 0: return

        # Step 2: Determine squares that are 'in range'
        in_range = []
        for warrior in warriors:
            if type(warriors[warrior]) is not type(self):
                enemy = warriors[warrior]
                for square in empty_squares(enemy._pos, world_global):
                    if square not in in_range: in_range.append(square)
        #print "%d squares in range: %s" % (len(in_range), in_range)
        if len(in_range) is 0: return

        # Step 3: Determine which of those squares are 'reachable'
        reachable = {}
        for square in in_range:
            len_path = measure_path(square, self._pos)
            if len_path >= 0:
                reachable[square] = len_path
        #print "%d squares are reachable: %s \r\n%s" % (len(reachable), reachable, sorted(reachable, key=reachable.get))
        if len(reachable) is 0: return

        # Step 4: Choose the nearest square, tiebreaking by 'reading order'
        min_path = min(reachable.values())
        for square in sorted(reachable):
            if reachable[square] is min_path:
                selected_square = square
                break
        #print "%s at %s targeting %s, at a distance of %d" % (self, self._pos, selected_square, reachable[selected_square])

        # Step 5: Select the step to take towards the chosen square, tiebreaking by 'reading order'
        travel_square = None
        measure_path(selected_square, self._pos)
        #print_world(world_paths)
        for square in sorted(adjacent_squares(self._pos, world_paths)):
            if world_paths[square] is min_path:
                travel_square = square
                break
        #print "%s at %s: traveling to %s" % (self, self._pos, travel_square)

        # Step 6: Update everything!
        del warriors[self._pos]
        world_global[self._pos] = '.'
        self._pos = travel_square
        world_global[self._pos] = self
        warriors[self._pos] = self
        return

    def attack(self):
        # Step 1: Determine if we are already 'in range' of an enemy
        nearby_enemies = self.adjacent_enemies()
        if len(nearby_enemies) is 0: return

        # Step 2: Determine which enemy has the lowest HP, tiebreaking by 'reading order'
        lowest_hp = BIG_NUM
        target_enemy = None
        for enemy in sorted(nearby_enemies):
            potential_enemy = world_global[enemy]
            if potential_enemy._hp < lowest_hp:
                lowest_hp = potential_enemy._hp
                target_enemy = potential_enemy

        # Step 3: Unload on this dude
        target_enemy._hp -= self._attack
        if target_enemy._hp <= 0:
            if PART2 and type(target_enemy) is Elf:
                raise ValueError('Elves can\'t be allowed to die!')
            del warriors[target_enemy._pos]
            world_global[target_enemy._pos] = '.'
        return

    def alive(self):
        return self._hp > 0

    def turn(self):
        if not self.alive():
            raise ValueError('I should be dead!')

        done = True
        for warrior in warriors:
            if type(warriors[warrior]) is not type(self):
                done = False

        self.move()
        self.attack()
        return done

    def adjacent_enemies(self):
        nearby_enemies = []
        for square in adjacent_squares(self._pos, world_global):
            if isinstance(world_global[square], Warrior) and type(world_global[square]) is not type(self):
                nearby_enemies.append(square)
        return nearby_enemies

class Elf(Warrior):
    def __init__(self, y, x):
        super(Elf, self).__init__(y, x, 'E')
        self._attack = ATTACK_ELF

    def __str__(self):
        return 'E'

class Goblin(Warrior):
    def __init__(self, y, x):
        super(Goblin, self).__init__(y, x, 'G')
        self._attack = ATTACK_GOBLIN

    def __str__(self):
        return 'G'

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def measure_path(src, dest):
    global world_paths
    world_paths = copy.deepcopy(world_global)
    #print "measuring from %s to %s" % (src, dest)

    level = 0
    world_paths[src] = 0

    unmeasured_squares = all_empty_squares(world_paths)
    while True:
        level += 1
        squares_measured = []
        for square in unmeasured_squares:
            for neighbor in adjacent_squares(square, world_paths):
                if world_paths[neighbor] is (level - 1):
                    if square not in squares_measured: squares_measured.append(square)

        for square in squares_measured:
            unmeasured_squares.remove(square)
            world_paths[square] = level

        if len(squares_measured) is 0:
            break

    #print_world(world_paths)
    min_path = BIG_NUM
    for square in adjacent_squares(dest, world_paths):
        min_path = min(min_path, world_paths[square])

    if min_path is BIG_NUM:
        return -1
    else:
        return min_path

def all_empty_squares(world):
    squares = []
    for square in world:
        if world[square] is '.': squares.append(square)
    return squares

def empty_squares(pos, world):
    squares = []
    for square in adjacent_squares(pos, world):
        if world[square] is '.': squares.append(square)

    return squares

def adjacent_squares(pos, world):
    return sorted([(pos[0] - 1, pos[1]),
                   (pos[0] + 1, pos[1]),
                   (pos[0], pos[1] - 1),
                   (pos[0], pos[1] + 1)])

def print_world(world):
    for y in range(rows):
        line = ""
        for x in range(cols):
            line += '%s' % world[(y, x)]
        print line
    print ''


#for file in ['advent_15_test_a.txt',
#             'advent_15_test_b.txt',
#             'advent_15_test_c.txt',
#             'advent_15_test_d.txt',
#             'advent_15_test_e.txt',
#             'advent_15_test_f.txt',
#             ]:
while True:
    try:
        warriors = {}
        world_global = {}
        world_paths = None

        # Build the world and add warriors
        with open('day15_input.txt') as f:
            input = [line.rstrip('\n') for line in f]
            y = 0
            for line in input:
                row = []
                x = 0
                for chr in line:
                    if chr is 'E':
                        elf = Elf(y, x)
                        warriors[(y, x)] = elf
                        world_global[(y, x)] = elf
                    elif chr is 'G':
                        goblin = Goblin(y, x)
                        warriors[(y, x)] = goblin
                        world_global[(y, x)] = goblin
                    else:
                        world_global[(y, x)] = chr

                    x += 1
                y += 1
            rows = y
            cols = x

        print "ATTACK_ELF=%d" % ATTACK_ELF
        rounds = 0
        done = False
        while not done:
            rounds += 1
            turn_order = []
            # Pre-calculate turn order before the round starts
            for warrior in sorted(warriors):
                turn_order.append(warriors[warrior])
        
            while len(turn_order) > 0:
                warrior = turn_order.pop(0)
                # Could already have been killed, check again!
                if warrior.alive():
                    done = done or warrior.turn()

        print_world(world_global)

        hp_remain = 0
        for warrior in warriors:
            hp_remain += warriors[warrior]._hp
            print "%s(%d)" % (warriors[warrior], warriors[warrior]._hp)

        print "Combat ends after %d full rounds" % (rounds - 1)
        print "%d total hit points left" % hp_remain
        print "Outcome: %d * %d = %d" % ((rounds - 1), hp_remain, (rounds - 1) * hp_remain)
        print "-------------------------------\r\n\r\n\r\n"
        break
    except ValueError:
        ATTACK_ELF += 1
