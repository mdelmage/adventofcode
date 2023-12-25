#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Find a path from 'start' to 'end' with the minimum number of edges.
# This implementation is similar to a tile flood, but we do need to remember
# all possible paths along the way.
#
# It doesn't matter which path we end up discovering first, only that it's
# of minimum length.
def find_a_shortest_path(start, end):
    # Organize a list of paths, ordered by path length.
    path_length = 0
    paths = {0: [[start]]}

    while True:
        path_length += 1
        paths[path_length] = []

        # Take every path of length L, and find all the possible ones for length L+1.
        for path in paths[path_length - 1]:
            loc = path[-1]
            for loc_next in [l for l in lookup[loc] if l not in path]:
                paths[path_length].append(path + [loc_next])
                if loc_next == end:
                    # Got to our target node! Bail out.
                    return paths[path_length][-1]
    # Unreachable.
    return []

# Parse the wiring diagram.
with open('day25_input.txt') as f:
    rows = [line.rstrip('\n').split(': ') for line in f]

nodes = []
lookup = {}
for node in rows:
    node1 = node[0]
    for node2 in node[1].split(' '):
        # Generate a simple list of nodes.
        if node1 not in nodes: nodes.append(node1)
        if node2 not in nodes: nodes.append(node2)

        # Connections aren't directional; abc: xyz and xyz:
        # abc both represent the same configuration.
        if node1 not in lookup: lookup[node1] = []
        if node2 not in lookup[node1]: lookup[node1].append(node2)
        if node2 not in lookup: lookup[node2] = []
        if node1 not in lookup[node2]: lookup[node2].append(node1)

# You have nowhere near that many stars - you need to find a way to disconnect at least
# half of the equipment here, but it's already Christmas! You only have time to disconnect three wires.
#
# The crux of this problem is selecting the three wires. It's trivial to test whether, for a given
# selection of wires to cut, the components are divided into two separate groups. The brute-force
# solution is possible, but annoyingly long to calculate.
#
# One clever method to reduce the search space:
#
# Take a sampling of paths between random node pairs, and build a history of edges encountered.
# Because of the nature of the graph being able to be split into two halves by removing
# just three edges, it will be "dumbbell shaped". The three special edges will be highly
# overrepresented in a random sampling of edges, since you need to cross one of them
# to get from one half of the graph to the other.
#
# Here we sample only a small percentage of the total possible edges. You can tune this
# for speed vs. accuracy.
edges = {}
for i in range(len(nodes) // 10):
    path = find_a_shortest_path(nodes[i], nodes[i + 1])
    for n in range(len(path) - 1):
        node1 = path[n]
        node2 = path[n + 1]
        pair = (min(node1, node2), max(node1, node2))
        edges[pair] = edges.get(pair, 0) + 1

# Okay, now we likely have our edges in the top three, but take the top ten or so just to be sure.
sorted_edges = [e for (e, s) in sorted(edges.items(), key=lambda x:x[1], reverse=True)[:10]]

product = 1
for w1, w2, w3 in [(w1, w2, w3) for w1 in sorted_edges for w2 in sorted_edges for w3 in sorted_edges]:
    # Ensure that we have 3 distinct wires.
    if w1 == w2 or w2 == w3 or w1 == w3: continue

    # "Cut" the wires by making a deep copy of the wiring lookup table, and removing those entries.
    lookup_custom = {}
    for edge in lookup:
        lookup_custom[edge] = [x for x in lookup[edge]]
    lookup_custom[w1[0]].remove(w1[1])
    lookup_custom[w1[1]].remove(w1[0])
    lookup_custom[w2[0]].remove(w2[1])
    lookup_custom[w2[1]].remove(w2[0])
    lookup_custom[w3[0]].remove(w3[1])
    lookup_custom[w3[1]].remove(w3[0])

    # Exhaustively visit all nodes in the graph.
    # If we find a group smaller than the size of the full graph, we've succeeeded in splitting
    # the graph.
    unexplored = set([node for node in lookup_custom])
    while len(unexplored) > 0:
        start = unexplored.pop()
        paths = set()
        explore = set([start])
        while len(explore) > 0:
            paths |= explore
            explore_next = set()
            for node in explore:
                nodes = lookup_custom[node]
                for n in nodes:
                    if n not in paths: explore_next.add(n)
            explore = explore_next

        # Remove the explored areas from our search.
        unexplored -= paths

        # We found a group smaller than the whole, so we've split the graph!
        # Determine what the product of the two groups sizes is.
        if len(paths) < len(lookup):
            product = len(paths) * (len(lookup) - len(paths))
            break

    # We found our edges! Bail out.
    if product > 1:
        break

# Find the three wires you need to disconnect in order to divide the components
# into two separate groups. What do you get if you multiply the sizes of these two groups together?
print('Part One: The product of the two group sizes is {0}.'.format(product))