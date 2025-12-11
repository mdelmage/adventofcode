#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To start a machine, its indicator lights must match those shown in the diagram,
# where . means off and # means on.
OFF = '.'
ON = '#'

def generate_combinations(buttons, num_presses):
    search_space = 2 ** len(buttons)

    combos = []
    for i in range(1, search_space):
        combo_str = '{0:024b}'.format(i)[-len(buttons):]
        combo = [int(n) for n in combo_str]
        if sum(combo) == num_presses: combos.append(combo)

    return(combos)

def press(num_lights, buttons, combo):
    lights = OFF * num_lights
    for i in range(len(combo)):
        if combo[i] > 0:
            for light in buttons[i]:
                if lights[light] == OFF:
                    lights = lights[:light] + ON + lights[light + 1:]
                else:
                    lights = lights[:light] + OFF + lights[light + 1:]
 
    return lights

def minimum_presses(lights, buttons):
    presses = 1
    while True:
        combos = generate_combinations(buttons, presses)
        for c in combos:
            if press(len(lights), buttons, c) == lights: return presses
        presses += 1

# Parse the remnants of the manual eaten by a Shiba Inu
with open('day10_input.txt') as f:
    machines = [line.rstrip('\n') for line in f]

i = 0
total_presses = 0
for machine in machines:
    machine = machine.replace('[', '').replace('] (', '/').replace(') {', '/').replace('}', '').split('/')
    lights = machine[0]
    buttons = [x.split(',') for x in machine[1].split(') (')]
    joltages = [int(n) for n in machine[2].split(',')]

    buttons_new = []
    for b in buttons:
        buttons_new.append([int(n) for n in b])
    buttons = buttons_new

    total_presses += minimum_presses(lights, buttons)
    i += 1

# Analyze each machine's indicator light diagram and button wiring schematics.
# What is the fewest button presses required to correctly configure the indicator
# lights on all of the machines?
print('Part One: The fewest button presses to configure the lights is {0}.'.format(total_presses))