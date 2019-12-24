#!/usr/bin/python
# coding: utf-8

import copy
import sys
import time

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
TILE_PASSAGE  = '.'
TILE_WALL     = '#'
TILE_ENTRANCE = '@'

keys = []
key_locations = {}
doors = []
stats = {'i': 0, 'r':0}
shortest_path = None
shortest_dist = sys.maxint

vault_map = {}
paths = []
location = None

key_paths = {}

solutions = {}

def map_keys(key, location, doors_entered, dist_traveled):
    global key_paths

    # Start at the current location (l) and map what we can see
    paths = {0: [location]}
    path_len = 0

    m = copy.deepcopy(vault_map)

    while len(paths[path_len]) > 0:
        paths[path_len + 1] = []
        for l in paths[path_len]:
            if m[l] in keys and m[l] != key:
                if key not in key_paths: key_paths[key] = {}
                if m[l] not in key_paths[key] or (key_paths[key][m[l]][0] > dist_traveled + path_len):
                    key_paths[key][m[l]] = (dist_traveled + path_len, set([x.lower() for x in doors_entered]))
                #print "Mapped {0}<-->{1} at dist {2} with doors {3}!".format(key, m[l], dist_traveled + path_len, doors_entered)
            m[l] = path_len
            for next_l in [(l[0] + d[0], l[1] + d[1]) for d in DIRECTIONS]:
                if next_l in m and m[next_l] in keys + doors + [TILE_PASSAGE, TILE_ENTRANCE]:
                    if m[next_l] in doors:
                        if m[next_l] not in doors_entered:
                            #print "Found a door at dist {0}!".format(dist_traveled + path_len + 1)
                            beyond_door = (l[0] + 2* (next_l[0] - l[0]), l[1] + 2 * (next_l[1] - l[1]))
                            map_keys(key, beyond_door, doors_entered + [m[next_l]], dist_traveled + path_len + 2)
                    else:
                        paths[path_len + 1].append(next_l)

        path_len += 1

    return

def explore(location, keys_collected, dist_traveled, history, max_depth):
    #print "{0} {1} {2} {3}".format(location, keys_collected, dist_traveled, history)
    global stats
    global shortest_path
    global shortest_dist
    global solutions

    stats['i'] += 1
    if 0 == stats['i'] % 10000000: print "{0}".format(stats['i'])

    if max_depth < len(keys) and len(keys_collected) == max_depth:
        if dist_traveled not in solutions: solutions[dist_traveled] = []
        solutions[dist_traveled].append(history)

    if len(keys_collected) == max_depth:#len(keys):
        if dist_traveled < shortest_dist:
            shortest_dist = dist_traveled
            shortest_path = history
            print "{0} Shortest path now {1}: {2}".format(stats['i'], shortest_dist, history)
        return

    # Recursive dive into possible next locations, sorted by ascending distance
    for k in key_paths[location]:
        if k not in keys_collected:
            kc = set(keys_collected)
            kr = key_paths[location][k][1]
            dist_to_travel = key_paths[location][k][0]
            if (max_depth < len(keys) or dist_traveled + dist_to_travel < shortest_dist) and kr.issubset(kc):
                new_keys_collected = copy.deepcopy(keys_collected)
                new_keys_collected.add(k)
                explore(k, new_keys_collected, dist_traveled + dist_to_travel, history + [k], max_depth)
    return

# Open input file
with open("day18.txt", "r") as f:
    # Build the map, recording keys as we see them
    y = 0
    for line in f:
        x = 0
        for c in line.strip():
            vault_map[(x, y)] = c
            if c in [TILE_ENTRANCE] + [chr(key) for key in range(ord('a'), ord('z') + 1)]:
                keys.append(c)
                key_locations[c] = (x, y)
            x += 1
            print c,
        print ""
        y += 1

    doors = [k.upper() for k in keys]

    # Build a mapping of every key to each other so we can do more abstract pathfinding
    for key in sorted(key_locations):
        print "Mapping key {0}...".format(key)
        map_keys(key, key_locations[key], [], 0)

    # Report what we've built before pathfinding
    for key in sorted(key_paths):
        print "Key {0}:".format(key)
        for other_key in sorted(key_paths[key]):
            print "\t{0} at dist {1} with keyrequisites {2}".format(other_key, key_paths[key][other_key][0], key_paths[key][other_key][1])

    # Explore the paths, yo.
    # Split the task into exhaustive search of the first X elements, then
    # a shortest-first search of those X-length paths.
    print "starting location = {0}".format(key_locations[TILE_ENTRANCE])
    explore(TILE_ENTRANCE, set(TILE_ENTRANCE), 0, [], 9)
    print "Shortest path was {0}: {1}".format(shortest_dist, shortest_path)
    print "{0} iterations.".format(stats['i'])
    print len(solutions)

    shortest_path = None
    shortest_dist = sys.maxint
    
    for path_len in sorted(solutions):
        print "{0}: {1}".format(path_len, len(solutions[path_len]))
        for s in solutions[path_len]:
            #print "Trying shortest pathlet {0} {1}...".format(path_len, s)
            explore(s[-1:][0], set([TILE_ENTRANCE] + s), path_len, s, len(keys))
    print "Shortest path was {0}: {1}".format(shortest_dist, shortest_path)
    print "{0} iterations.".format(stats['i'])
