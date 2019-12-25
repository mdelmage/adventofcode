#!/usr/bin/python
# coding: utf-8

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

def is_capital_letter(l):
    return (ord(l) >= ord('A')) and (ord(l) <= ord('Z'))

def print_maze(m):
    x = 0
    y = 0

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
    if l in portal_pairs: return [portal_pairs[l]]
    return []
    
def find_paths():
    global maze
    path_len = 0
    paths = {path_len: [starting_coord]}

    # Flood-style pathfinding:
    # Find all grid squares at a distance of 1, then 2, 3...
    while len(paths[path_len]) > 0:
        paths[path_len + 1] = []
        for l in paths[path_len]:
            maze[l] = path_len
            # Check all four neighbors to see if they're unmapped 
            for next_l in [(l[0] + m[0], l[1] + m[1]) for m in MOVES] + portal_exits(l):
                if TILE_PASSAGE == maze[next_l]:
                    # Empty passageway; mark it
                    maze[next_l] = path_len + 1
                    paths[path_len + 1].append(next_l)
                elif isinstance(maze[next_l], int) and maze[next_l] > path_len + 1:
                    # Previously mapped, but we've discovered a shorter path
                    maze[next_l] = path_len + 1
                    paths[path_len + 1].append(next_l)
                elif maze[next_l] in portal_names:
                    # Found a portal; jump to the other side
                    maze[next_l] = path_len + 1
                    paths[path_len + 1].append(next_l)
                elif ENDING_PORTAL[0] == maze[next_l]:
                    # Found the exit!
                    maze[next_l] = path_len + 1
                    paths[path_len + 1].append(next_l)
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
            starting_coord = portals[p][0]
        elif ENDING_PORTAL == p:
            maze[portals[p][0]] = ENDING_PORTAL[0]
            ending_coord = portals[p][0]
        else:
            portal_pairs[portals[p][0]] = portals[p][1]
            portal_pairs[portals[p][1]] = portals[p][0]
            for coord in portals[p]:
                portal_name = chr(ord('a') + i)
                portal_names.add(portal_name)
                maze[coord] = portal_name
            i += 1

    print_maze(maze)

    find_paths()
    print_maze(maze)
    print "Shortest path out of the maze is {0} steps.".format(maze[ending_coord])
    