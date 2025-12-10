#!/usr/bin/env python
# -*- coding: utf-8 -*-

def point_inside_path(p):
    if p in red_tiles:
        #print('{0} is a red tile, success'.format(p))
        return True

    if p in green_tiles:
        #print('{0} is a green tile, success'.format(p))
        return True

    (col, row) = p

    # Go left
    crossings = 0
    for (col_start, col_end) in map_rows.get(row, []):
        if col > col_start:
            crossings += 1
        else:
            break
    if crossings % 2 == 0:
        #print('\t{0}: Left check failed because there were {1} crossings'.format(p, crossings))
        return False

    # Go up
    crossings = 0
    for (row_start, row_end) in map_cols.get(col, []):
        if row > row_start:
            crossings += 1
        else:
            break
    if crossings % 2 == 0:
        print('\t{0}: Up check failed because there were {1} crossings'.format(p, crossings))
        return False

    # Go right
    crossings = len(map_rows.get(row, []))
    for (col_start, col_end) in map_rows.get(row, []):
        if col > col_end:
            crossings -= 1
        else:
            break
    if crossings % 2 == 0:
        print('\t{0}: Right check failed because there were {1} crossings'.format(p, crossings))
        return False

    # Go down
    crossings = len(map_cols.get(col, []))
    for (row_start, row_end) in map_cols.get(col, []):
        if row > row_end:
            crossings -= 1
        else:
            break
    if crossings % 2 == 0:
        print('\t{0}: Down check failed because there were {1} crossings'.format(p, crossings))
        return False

    return True

def rect_inside_path(rect):
    perimeter = set()
    col1 = min(rect[0][0], rect[1][0])
    col2 = max(rect[0][0], rect[1][0])
    row1 = min(rect[0][1], rect[1][1])
    row2 = max(rect[0][1], rect[1][1])

    for col in range(col1, col2 + 1):
        perimeter.add((col, row1))
        perimeter.add((col, row2))
    for row in range(row1, row2 + 1):
        perimeter.add((col1, row))
        perimeter.add((col2, row))

    for p in perimeter:
        if not point_inside_path(p):
            return False
    return True

def find_biggest_rect():
    for area in sorted(areas, reverse=True):
        print(area)
        for rect in areas[area]:
            if rect_inside_path(rect): return area
    return None

# Parse the red tiles list
with open('day09_input.txt') as f:
    tiles = [tuple([int(n) for n in line.rstrip('\n').split(',')]) for line in f]

areas = {}
largest_rectangle = 0
for t1, t2 in [(t1, t2) for t1 in tiles for t2 in tiles if t1 != t2]:
    area = (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)
    if area not in areas: areas[area] = []
    areas[area].append((t1, t2))
    largest_rectangle = max(largest_rectangle, abs(t1[0] - t2[0] + 1) * abs(t1[1] - t2[1] + 1))

red_tiles = set()
for tile in tiles: red_tiles.add(tile)
#print(len(red_tiles))

# Using two red tiles as opposite corners, what is the largest area of any rectangle you can make?
print('Part One: The area of the largest rectangle made with red tile corners is {0}.'.format(largest_rectangle))

map_rows = {}
map_cols = {}

green_tiles = set()
for i in range(len(tiles)):
    t1 = tiles[i]
    t2 = tiles[(i + 1) % len(tiles)]
    if t1[0] != t2[0]:
        # Horizontal line
        y = t1[1]
        x_min = min(t1[0], t2[0])
        x_max = max(t1[0], t2[0])
        for x in range(x_min + 1, x_max):
            green_tiles.add((x, y))
            if x not in map_cols: map_cols[x] = []
            map_cols[x].append((y, y))
        if y not in map_rows: map_rows[y] = []
        map_rows[y].append((x_min, x_max))
    else:
        # Vertical line
        x = t1[0]
        y_min = min(t1[1], t2[1])
        y_max = max(t1[1], t2[1])
        for y in range(y_min + 1, y_max):
            green_tiles.add((x, y))
            if y not in map_rows: map_rows[y] = []
            map_rows[y].append((x, x))
        if x not in map_cols: map_cols[x] = []
        map_cols[x].append((y_min, y_max))


for row in map_rows:
    map_rows[row] = sorted(map_rows[row])
for col in map_cols:
    map_cols[col] = sorted(map_cols[col])

# Using two red tiles as opposite corners, what is the largest area of any rectangle you can make
# using only red and green tiles?
print('Part Two: The area of the largest rectangle made with red tile corners is {0}.'.format(find_biggest_rect()))