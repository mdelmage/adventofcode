#!/usr/bin/env python
# -*- coding: utf-8 -*-

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class Range:
    def __init__(self):
        self.subranges = []

    def add(self, l, h):
        # Add the new subrange, which may partially or completely overlap others.
        self.subranges.append((l, h))

        # Loop through the subranges, identifying single pairs that can be consolidated,
        # and repeat until we make it all the way through the list once without needing to consolidate.
        done = False
        sorted_subranges = sorted(self.subranges)
        while not done:
            done = True

            for i in range(len(sorted_subranges) - 1):
                sr1 = sorted_subranges[i]
                sr2 = sorted_subranges[i + 1]

                if sr2[0] <= sr1[1] and sr1[1] >= sr2[1]:
                    # sr1 fully overlaps sr2, so consolidate by deleting sr2
                    sorted_subranges = sorted_subranges[:i] + [sr1] + sorted_subranges[i + 2:]
                    done = False
                    break
                elif sr2[0] - 1 <= sr1[1]:
                    # sr1 and sr2 partially overlap, or are adjacent -- consolidate into sr1+sr2
                    sorted_subranges = sorted_subranges[:i] + [(sr1[0], sr2[1])] + sorted_subranges[i + 2:]
                    done = False
                    break

        self.subranges = sorted_subranges

    def __len__(self):
        length = 0
        for subrange in self.subranges:
            length += subrange[1] - subrange[0]

        return length

# Parse the sensor report file
with open('day15_input.txt') as f:
    sensors_and_beacons = [line.rstrip('\n') for line in f]

excluded_ranges = {}

for sensor in sensors_and_beacons:
    # Cut down the static text to get to the sensor/beacon coordinates.
    sensor = sensor.replace('Sensor at x=', '')
    sensor = sensor.replace(' y=', '')
    sensor = sensor.replace(': closest beacon is at x=', ',')
    (sx, sy, bx, by) = [int(n) for n in sensor.split(',')]
    s = (sx, sy)
    b = (bx, by)

    # Using the distance to the found beacon, create a diamond-shaped exclusion zone
    # near the sensor where there can't be any beacons.
    # 
    dist = manhattan_distance(s, b)
    for row in range(s[1] - dist, s[1] + dist + 1):
        x_min = s[0] - (dist - abs(s[1] - row))
        x_max = s[0] + (dist - abs(s[1] - row))

        if row not in excluded_ranges:
            excluded_ranges[row] = Range()
        excluded_ranges[row].add(x_min, x_max)

# Consult the report from the sensors you just deployed.
# In the row where y=2000000, how many positions cannot contain a beacon?
row = 2000000
excluded_range_len = len(excluded_ranges[row])
print('Part One: {0} positions cannot contain a beacon.'.format(excluded_range_len))

# None of the detected beacons seem to be producing the distress signal, so you'll need
# to work out where the distress beacon is by working out where it isn't. For now,
# keep things simple by counting the positions where a beacon cannot possibly be along
# just a single row.
#
# Your handheld device indicates that the distress signal is coming from a beacon nearby.
# The distress beacon is not detected by any sensor, but the distress beacon must have x and y
# coordinates each no lower than 0 and no larger than 4000000.
row = 0
while len(excluded_ranges[row].subranges) == 1:
    # The beacon can only be in one row -- the one with more than one excluded region.
    row += 1

# The beacon can only be in one column -- the one between the two excluded regions.
col = excluded_ranges[row].subranges[0][1] + 1

# To isolate the distress beacon's signal, you need to determine its tuning frequency,
# which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.
tuning_freq = (4000000 * col) + row
print('Part Two: distress beacon tuning frequency is {0}.'.format(tuning_freq))
