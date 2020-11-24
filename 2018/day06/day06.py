import sys

coords = []
distances = {}
upper_left = (sys.maxint, sys.maxint)
lower_right = (-1, -1)

# Manhattan Distance
# https://en.wikipedia.org/wiki/Taxicab_geometry
def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

with open('day06_input.txt') as f:
    input = [line.rstrip('\n') for line in f]

for line in input:
    x = int(line.split(',')[0])
    y = int(line.split(',')[1])
    
    if x < upper_left[0]: upper_left = (x, upper_left[1])
    if x > lower_right[0]: lower_right = (x, lower_right[1])
    
    if y < upper_left[1]: upper_left = (upper_left[0], y)
    if y > lower_right[1]: lower_right = (lower_right[0], y)
    coords.append((x, y))


# Part 2: Safe Region
safe_region_size = 0
for x in range(upper_left[0], lower_right[0] + 1):
    for y in range(upper_left[1], lower_right[1] + 1):
        total_dist = 0
        grid_point = (x, y)
        for coord in coords:
            total_dist += dist(grid_point, coord)
        if total_dist < 10000:
            safe_region_size += 1

# Part 1A: Small grid
for x in range(upper_left[0], lower_right[0] + 1):
    for y in range(upper_left[1], lower_right[1] + 1):
        grid_point = (x, y)
        dists = {}
        for coord in coords:
            grid_dist = dist(grid_point, coord)
            if grid_dist in dists:
                dists[grid_dist].append(coord)
            else:
                dists[grid_dist] = [coord]

        shortest_dists = dists[min(dists.keys())]
        if len(shortest_dists) == 1:
            closest_coord = shortest_dists[0]
            distances[closest_coord] = distances.get(closest_coord, 0) + 1

# Part 1B: Bigger grid
distances2 = {}
upper_left = (upper_left[0] - 10, upper_left[1] - 10)
lower_right = (lower_right[0] + 10, lower_right[1] + 10)
for x in range(upper_left[0], lower_right[0] + 1):
    for y in range(upper_left[1], lower_right[1] + 1):
        grid_point = (x, y)
        dists = {}
        for coord in coords:
            grid_dist = dist(grid_point, coord)
            if grid_dist in dists:
                dists[grid_dist].append(coord)
            else:
                dists[grid_dist] = [coord]

        shortest_dists = dists[min(dists.keys())]
        if len(shortest_dists) == 1:
            closest_coord = shortest_dists[0]
            distances2[closest_coord] = distances2.get(closest_coord, 0) + 1

# Now consider only areas that have not grown as the grid grew (aka not infinite!)
biggest_areas = sorted(distances, key=distances.get, reverse=True)
for coord in biggest_areas:
    if distances[coord] == distances2[coord]:
        print "%s: %d" % (coord, distances[coord])
        break
    else:
        print "%s: %d (ignored)" % (coord, distances[coord])

print "safe region size: %d" % safe_region_size