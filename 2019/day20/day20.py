#!/usr/bin/python
# coding: utf-8

import copy

MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]

TILE_EMPTY    = ' '
TILE_PASSAGE  = '.'
TILE_WALL     = '#'

STARTING_PORTAL = 'AA'
ENDING_PORTAL   = 'ZZ'

starting_coord = None
ending_coord = None
maze_x = None
maze_y = None
maze = {}
portals = {}
portal_names = set()
portal_pairs = {}
levels = {}

def is_capital_letter(l):
    return (ord(l) >= ord('A')) and (ord(l) <= ord('Z'))

def print_maze(level):
    x = 0
    y = 0

    print "Maze Level {0}".format(level)

    m = levels[level]
    while (x, y) in m:
        while (x, y) in m:
            if isinstance(m[(x, y)], int):
                print m[(x, y)] % 10,
            else:
                print m[(x, y)],
            x += 1
        print ""
        y += 1
        x = 0

def portal_exits(l):
    in_level = l[0]
    in_coord = (l[1], l[2])
    if in_coord not in portal_pairs:
        return []

    out_coord  = portal_pairs[in_coord]
    if in_coord[0] < 4 or in_coord[1] < 4 or in_coord[0] > maze_x - 4 or in_coord[1] > maze_y - 4:
        out_level = in_level - 1
        if out_level < 0: return []
    else:
        out_level = in_level + 1

    e = (out_level, out_coord[0], out_coord[1])
    return [e]
    
def find_paths():
    global maze
    path_len = 0
    paths = {path_len: [(0, starting_coord[0], starting_coord[1])]}

    # Flood-style pathfinding:
    # Find all grid squares at a distance of 1, then 2, 3...
    # Artificial path limit of 10k.
    while len(paths[path_len]) > 0 and path_len < 10000:
        paths[path_len + 1] = []
        for l in paths[path_len]:
            # Check all four neighbors to see if they're unmapped 
            for coord in [(l[0], l[1] + m[0], l[2] + m[1]) for m in MOVES] + portal_exits(l):
                level = coord[0]
                next_coord = (coord[1], coord[2])
                if level not in levels: levels[level] = copy.deepcopy(maze)
                
                if TILE_PASSAGE == levels[level][next_coord]:
                    # Empty passageway; mark it
                    levels[level][next_coord] = path_len + 1
                    paths[path_len + 1].append((level, next_coord[0], next_coord[1]))
                elif isinstance(levels[level][next_coord], int) and levels[level][next_coord] > path_len + 1:
                    # Previously mapped, but we've discovered a shorter path
                    levels[level][next_coord] = path_len + 1
                    paths[path_len + 1].append((level, next_coord[0], next_coord[1]))
                elif levels[level][next_coord] in portal_names:
                    # Found a portal; jump to the other side
                    levels[level][next_coord] = path_len + 1
                    paths[path_len + 1].append((level, next_coord[0], next_coord[1]))
                elif ENDING_PORTAL[0] == levels[level][next_coord]:
                    # Found the exit!
                    levels[level][next_coord] = path_len + 1
                    paths[path_len + 1].append((level, next_coord[0], next_coord[1]))
                #print next_l
        path_len += 1
        #break

# Open input file
with open("day20.txt", "r") as f:
    y = 0
    for line in f:
        for x in range(len(line[:-1])):
            maze[(x, y)] = line[x]
        y += 1

    maze_x = x + 1
    maze_y = y

    # Replace 3-character portals with 1-character symbols.
    # Four Phase I passes required, one for N/W/E/S each.

    # West pass
    for y in range(maze_y):
        for x in range(maze_x - 2):
            if is_capital_letter(maze[(x, y)]) and \
               is_capital_letter(maze[(x + 1, y)]) and \
               TILE_PASSAGE == maze[(x + 2, y)]:
                #print "{0} {1} {2}".format(maze[(x, y)], maze[(x + 1, y)], maze[(x + 2, y)])
                portal_name = maze[(x, y)] + maze[(x + 1, y)]
                if portal_name not in portals: portals[portal_name] = []
                portals[portal_name].append((x + 2, y))
                maze[(x, y)] =  TILE_EMPTY
                maze[(x + 1, y)] = TILE_EMPTY

    # East pass
    for y in range(maze_y):
        for x in range(maze_x - 2):
            if TILE_PASSAGE == maze[(x, y)] and \
               is_capital_letter(maze[(x + 1, y)]) and \
               is_capital_letter(maze[(x + 2, y)]):
                #print "{0} {1} {2}".format(maze[(x, y)], maze[(x + 1, y)], maze[(x + 2, y)])
                portal_name = maze[(x + 1, y)] + maze[(x + 2, y)]
                if portal_name not in portals: portals[portal_name] = []
                portals[portal_name].append((x, y))
                maze[(x + 1, y)] =  TILE_EMPTY
                maze[(x + 2, y)] = TILE_EMPTY

    # North pass
    for x in range(maze_x):
        for y in range(maze_y - 2):
            if is_capital_letter(maze[(x, y)]) and \
               is_capital_letter(maze[(x, y + 1)]) and \
               TILE_PASSAGE == maze[(x, y + 2)]:
                #print "{0} {1} {2}".format(maze[(x, y)], maze[(x, y + 1)], maze[(x, y + 2)])
                portal_name = maze[(x, y)] + maze[(x, y + 1)]
                if portal_name not in portals: portals[portal_name] = []
                portals[portal_name].append((x, y + 2))
                maze[(x, y)] =  TILE_EMPTY
                maze[(x, y + 1)] = TILE_EMPTY

    # South pass
    for x in range(maze_x):
        for y in range(maze_y - 2):
            if TILE_PASSAGE == maze[(x, y)] and \
               is_capital_letter(maze[(x, y + 1)]) and \
               is_capital_letter(maze[(x, y + 2)]):
                #print "{0} {1} {2}".format(maze[(x, y)], maze[(x, y + 1)], maze[(x, y + 2)])
                portal_name = maze[(x, y + 1)] + maze[(x, y + 2)]
                if portal_name not in portals: portals[portal_name] = []
                portals[portal_name].append((x, y))
                maze[(x, y + 1)] =  TILE_EMPTY
                maze[(x, y + 2)] = TILE_EMPTY

    # Phase II pass: pair up portals and remove start/end symbols
    i = 0
    for p in portals:
        if STARTING_PORTAL == p:
            maze[portals[p][0]] = STARTING_PORTAL[0]
            starting_coord = (portals[p][0][0], portals[p][0][1])
        elif ENDING_PORTAL == p:
            maze[portals[p][0]] = ENDING_PORTAL[0]
            ending_coord = (portals[p][0][0], portals[p][0][1])
        else:
            portal_pairs[portals[p][0]] = portals[p][1]
            portal_pairs[portals[p][1]] = portals[p][0]
            for coord in portals[p]:
                portal_name = chr(ord('a') + i)
                portal_names.add(portal_name)
                maze[coord] = portal_name
            i += 1

    levels[0] = copy.deepcopy(maze)
    print_maze(0)

    find_paths()
    print "Shortest path out of the maze is {0} steps.".format(levels[0][(ending_coord[0], ending_coord[1])])
    