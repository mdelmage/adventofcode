#!/usr/bin/env python
# -*- coding: utf-8 -*-

ITERATIONS_PART_ONE = 5
ITERATIONS_PART_TWO = 18

PIXEL_OFF = '.'
PIXEL_ON = '#'

STARTING_PATTERN = { (0, 0): PIXEL_OFF,
                     (1, 0): PIXEL_ON,
                     (2, 0): PIXEL_OFF,
                     (0, 1): PIXEL_OFF,
                     (1, 1): PIXEL_OFF,
                     (2, 1): PIXEL_ON,
                     (0, 2): PIXEL_ON,
                     (1, 2): PIXEL_ON,
                     (2, 2): PIXEL_ON}

def image_size(i):
    return int(len(i) ** 0.5)

def image_print(i):
    size = image_size(i)
    for y in range(size):
        row = ''
        for x in range(size):
            row += i[(x, y)]
        print row

def image_pixels_on(i):
    pixels_on = 0
    for coord in i:
        if i[coord] == PIXEL_ON: pixels_on += 1
    return pixels_on

def rule_pack(i, x, y, size):
    rule_str = ''
    for y in range(size):
        for x in range(size):
            rule_str += i[(x, y)]
        rule_str += '/'

    # Remove trailing slash
    return rule_str[:-1]

def rule_unpack(rule, image, x, y, size):
    i = 0
    x_cur = x
    y_cur = y
    while i < len(rule):
        if rule[i] == '/':
            x_cur = x
            y_cur += 1
            i += 1
            continue
        image[(x_cur, y_cur)] = rule[i]
        x_cur += 1
        i += 1
    return image

def hflip(image, flip):
    if not flip:
        return image

    hflipped_image = {}
    size = image_size(image)
    for (x, y) in image:
        hflipped_image[(size - 1 - x, y)] = image[(x, y)]
    return hflipped_image

def vflip(image, flip):
    if not flip:
        return image

    vflipped_image = {}
    size = image_size(image)
    for (x, y) in image:
        vflipped_image[(x, size - 1 - y)] = image[(x, y)]
    return vflipped_image

def rot90(image):
    rot90_image = {}
    size = image_size(image)
    for (x, y) in image:
        rot90_image[(size - 1 - y, x)] = image[(x, y)]
    return rot90_image

def rotate(image, degrees):
    for i in range(degrees / 90):
        image = rot90(image)
    return image

def image_subsquare(image, x, y, size):
    subsquare = {}
    for i in range(size):
        for j in range(size):
            subsquare[(i, j)] = image[(x + i, y + j)]
    return subsquare

def match_rule(image):
    size = image_size(image)
    for h in [False, True]:
         for v in [False, True]:
            for angle in [0, 90, 180, 270]:
                fitted_image = rotate(vflip(hflip(image, h), v), angle)
                rule_str = rule_pack(fitted_image, size * x, size * y, size)
                for r in rules:
                     if r[0] == rule_str: return r[1]
    return None

# Parse the rules file
with open('day21_input.txt') as f:
    rules = [line.rstrip('\n').split(' => ') for line in f]

image = STARTING_PATTERN
for iteration in range(ITERATIONS_PART_TWO):
    if iteration == ITERATIONS_PART_ONE:
        print 'Part One: {0} pixels are on after {1} iterations.'.format(image_pixels_on(image), ITERATIONS_PART_ONE)

    image_next = {}
    grid_size = image_size(image)
    if (grid_size % 2) == 0:
        subgrid_size_current = 2
        subgrid_size_next = 3
    else:
        subgrid_size_current = 3
        subgrid_size_next = 4

    for y in range(grid_size / subgrid_size_current):
        for x in range(grid_size / subgrid_size_current):
            subsquare = image_subsquare(image, subgrid_size_current * x, subgrid_size_current * y, subgrid_size_current)
            rule_str = match_rule(subsquare)
            image_next = rule_unpack(rule_str, image_next, subgrid_size_next * x, subgrid_size_next * y, subgrid_size_next)
    image = image_next

print 'Part Two: {0} pixels are on after {1} iterations.'.format(image_pixels_on(image), ITERATIONS_PART_TWO)