# The immune system and the infection each have an army made up of several groups;
# each group consists of one or more identical units. The armies repeatedly fight
# until only one army has units remaining.
#
# Units within a group all have the same hit points (amount of damage a unit can take
# before it is destroyed), attack damage (the amount of damage each unit deals), an 
# attack type, an initiative (higher initiative units attack first and win ties), and
# sometimes weaknesses or immunities.
class ArmyGroup(object):
    def __init__(self, army, group_num, units, hp, damage, attack_type, initiative, weaknesses, immunities):
        self.army = army
        self.group_num = group_num
        self.units = units
        self.hp = hp
        self.damage = damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.target = None

    def __str__(self):
        return 'Group %d contains %d units' % (self.group_num, self.units)

    def effectivePower(self):
        # Each group also has an effective power: the number of units
        # in that group multiplied by their attack damage.
        damage = self.damage
        if self.army == IMMUNE_SYSTEM: damage += BOOST
        return self.units * damage

    def actualDamage(self, target):
        # By default, an attacking group would deal damage equal to its effective power
        # to the defending group. However, if the defending group is immune to the
        # attacking group's attack type, the defending group instead takes no damage;
        # if the defending group is weak to the attacking group's attack type, the
        # defending group instead takes double damage.
        if self.army == target.army: return 0
        if self.attack_type in target.weaknesses: return self.effectivePower() * 2
        if self.attack_type in target.immunities: return 0
        return self.effectivePower()

    def selectTarget(self, target_list):
        # The attacking group chooses to target the group in the enemy army to which
        # it would deal the most damage (after accounting for weaknesses and immunities,
        # but not accounting for whether the defending group has enough units to
        # actually receive all of that damage).
        #
        # If an attacking group is considering two defending groups to which it would deal
        # equal damage, it chooses to target the defending group with the largest
        # effective power; if there is still a tie, it chooses the defending group with
        # the highest initiative.
        target_order_list = []
        for t in target_list:
            if self.actualDamage(t) > 0:
                print '%s group %d would deal defending group %d %d damage' % (armies_str[self.army], self.group_num, t.group_num, self.actualDamage(t))
            target_order_list.append([self.actualDamage(t), t.effectivePower(), t.initiative, t])
        target_order_list = sorted(target_order_list, key = lambda x: (x[0], x[1], x[2]), reverse=True)
        
        # If it cannot deal any defending groups damage, it does not choose a target.
        if target_order_list[0][0] == 0:
            return None
        else:
            self.target = target_order_list[0][3]
            return self.target
        
    def attack(self):
        if self.target is None:
            return 
        
        # The defending group only loses whole units from damage; damage is always dealt
        # in such a way that it kills the most units possible, and any remaining damage
        # to a unit that does not immediately kill it is ignored.
        killed_units = min(self.target.units, self.actualDamage(self.target) / self.target.hp)
        print '%s group %d attacks defending group %d, killing %d units' % (armies_str[self.army], self.group_num, self.target.group_num, killed_units)
        self.target.units -= killed_units
        
        # Groups never have zero or negative units; instead, the group is removed from combat.
        if self.target.units == 0:
            del initiatives[self.target.initiative]
            armies[self.target.army].remove(self.target)

        # Clear the target.
        self.target = None
        return

# The immune system and the infection each have an army made up of several groups
UNKNOWN_SYSTEM = -1
IMMUNE_SYSTEM  =  0
INFECTION      =  1

armies_str = \
{
    IMMUNE_SYSTEM : 'Immune System',
    INFECTION : 'Infection'
}

# ...and sometimes weaknesses or immunities.
UNKNOWN_ATTR = -1
WEAKNESS     =  0
IMMUNITY     =  1

# A boost is an integer increase in immune system units' attack damage.
# By inspection, numbers smaller than this either result in the
# immune system losing, or a stalemate in which all groups are immune
# to their enemies' attacks.
BOOST = 57

army = UNKNOWN_SYSTEM
armies = {}
armies[IMMUNE_SYSTEM] = []
armies[INFECTION] = []
initiatives = {}
group_num = 0

# Parse the input file
with open('day24_input.txt') as f:
    lines = [line.rstrip('\n') for line in f]
    for line in lines:
        if 'Immune System' in line:
            army = IMMUNE_SYSTEM
            group_num = 0
        if 'Infection' in line:
            army = INFECTION
            group_num = 0
        if 'each' in line:
            group_num += 1
            print '{0}: {1}'.format(army, line)
            # Make sure there are parentheses, since they're optional.
            line = line.replace('hit points with', 'hit points () with')
            
            # Excise unnecessary words.
            line = line.replace('units each with ', '')
            line = line.replace('hit points ', '')
            line = line.replace('to ', '')
            line = line.replace('with an attack that does ', '')
            line = line.replace('damage at initiative ', '')
            
            # Break out the portion in parentheses
            tokens = line.replace(')', '(').split('(')

            # The fixed part of the group descriptor contains:
            # 1) count
            # 2) hp
            # 3) damage
            # 4) type
            # 5) initiative
            fixed_tokens = (tokens[0] + tokens[2]).replace('  ', ' ').split(' ')
            units = int(fixed_tokens[0])
            hp = int(fixed_tokens[1])
            damage = int(fixed_tokens[2])
            attack_type = fixed_tokens[3]
            initiative = int(fixed_tokens[4])
            print '\tunits = %d' % units
            print '\thp = %d' % hp
            print '\tdamage = %d' % damage
            print '\ttype = %s' % attack_type
            print '\tinitiative = %d' % initiative
            
            # The variable part of the group descriptor contains attributes:
            # 1) weaknesses (optional)
            # 2) immunities (optional)
            attr_tokens = tokens[1].replace('; ', ' ').replace(', ', ' ').split(' ')
            attr = UNKNOWN_ATTR
            weaknesses = []
            immunities = []
            for token in attr_tokens:
                if token == 'weak':
                    attr = WEAKNESS
                elif token == 'immune':
                    attr = IMMUNITY
                else: 
                    if attr == WEAKNESS: weaknesses.append(token)
                    if attr == IMMUNITY: immunities.append(token)
            print '\tweaknesses: %s' % weaknesses
            print '\timmunities: %s' % immunities
            
            g = ArmyGroup(army, group_num, units, hp, damage, attack_type, initiative, weaknesses, immunities)
            initiatives[initiative] = g
            armies[army].append(g)

    for i in sorted(initiatives, reverse=True):
        print '{0}: {1}'.format(i, initiatives[i])

done = False
while not done:
    # *** SELECTION PHASE ***
    # During the target selection phase, each group attempts to choose one target.
    target_selection_order_list = []
    for a in armies:
        print armies_str[a] + ':'
        for g in armies[a]:
            print g
            # In decreasing order of effective power, groups choose their targets;
            # in a tie, the group with the higher initiative chooses first.
            target_selection_order_list.append([g.effectivePower(), g.initiative, g])
    print ''
    possible_targets_list = [initiatives[i] for i in initiatives]
    target_selection_order_list = sorted(target_selection_order_list, key = lambda x: (x[0], x[1]), reverse=True)
    target_selection_order_list = [x[2] for x in target_selection_order_list]
    for group in target_selection_order_list:
        target = group.selectTarget(possible_targets_list)
        if target is not None: possible_targets_list.remove(target)

    # At the end of the target selection phase, each group has selected
    # zero or one groups to attack and each group is being attacked
    # by zero or one groups.

    # *** ATTACKING PHASE ***
    # During the attacking phase, each group deals damage
    # to the target it selected, if any. Groups attack in decreasing order
    # of initiative, regardless of whether they are part of the infection
    # or the immune system.
    attack_order_list = sorted(initiatives, reverse=True)
    for initiative in attack_order_list:
        if initiative in initiatives: initiatives[initiative].attack()
    
    print ''
    
    done = (len(armies[IMMUNE_SYSTEM]) == 0 or len(armies[INFECTION]) == 0)

# Battle over! Print the result.
winning_army_units = 0
for a in armies:
    print armies_str[a] + ':'
    if len(armies[a]) == 0: print 'No groups remain.'
    for g in armies[a]:
        print g
        winning_army_units += g.units
print 'Winning army has %d units remaining.' % winning_army_units
