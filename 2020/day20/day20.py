#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

TILE_SIZE = 10

SIDE_TOP    = 0
SIDE_BOTTOM = 1
SIDE_LEFT   = 2
SIDE_RIGHT  = 3

# The problem never explicitly says whether '#' is an 'on' pixel or an 'off' pixel,
# but the sea monsters are made of these so let's consider them 'on'.
PIXEL_ON      = '#'
PIXEL_OFF     = '.'
PIXEL_MONSTER = 'O'

# We only want to allow tiles to align if it makes sense -- don't align a tile's
# left edge with another tile's bottom edge, for example.
valid_alignments = ((SIDE_TOP,    SIDE_BOTTOM),
                    (SIDE_BOTTOM,    SIDE_TOP),
                    (SIDE_LEFT,    SIDE_RIGHT),
                    (SIDE_RIGHT,    SIDE_LEFT))

# Because your image is monochrome, a sea monster will look like this:
'                  # '
'#    ##    ##    ###'
' #  #  #  #  #  #   '

# (generated programatically from the above)
sea_monster = [
(18, 0),
(0, 1),
(5, 1),
(6, 1),
(11, 1),
(12, 1),
(17, 1),
(18, 1),
(19, 1),
(1, 2),
(4, 2),
(7, 2),
(10, 2),
(13, 2),
(16, 2)]
 
class Tile(object):
    def __init__(self, number=0, size=TILE_SIZE):
        self.number = number
        self.size = size
        self.image = {}
        self.scores = {}
        self.location = None

    def __str__(self):
        s = ''
        for y in range(self.size):
            line = ''
            for x in range(self.size):
                line += self.image[(x, y)]
            s += line + '\n'
        return s

    def score(self):
        # Consider each edge row/column. Using the pixels as a 0/1 bitmask,
        # generate an integer and call it the 'score' for that edge.
        score = 0
        for x in range(self.size):
            if self.image[(x, 0)] == PIXEL_ON:
                score += (1 << (self.size - x - 1))
        self.scores[SIDE_TOP] = score

        score = 0
        for x in range(self.size):
            if self.image[(x, self.size - 1)] == PIXEL_ON:
                score += (1 << (self.size - x - 1))
        self.scores[SIDE_BOTTOM] = score
                
        score = 0
        for y in range(self.size):
            if self.image[(0, y)] == PIXEL_ON:
                score += (1 << (self.size - y - 1))
        self.scores[SIDE_LEFT] = score

        score = 0
        for y in range(self.size):
            if self.image[(self.size - 1, y)] == PIXEL_ON:
                score += (1 << (self.size - y - 1))
        self.scores[SIDE_RIGHT] = score

    def rotate(self):
        new_image = {}
        for (x, y) in self.image:
            new_image[(self.size - y - 1, x)] = self.image[(x, y)]
        self.image = new_image
        self.score()

    def hflip(self):
        new_image = {}
        for (x, y) in self.image:
            new_image[(self.size - x - 1, y)] = self.image[(x, y)]
        self.image = new_image
        self.score()

    def vflip(self):
        new_image = {}
        for (x, y) in self.image:
            new_image[(x, self.size - y - 1)] = self.image[(x, y)]
        self.image = new_image
        self.score()

    def matches(self, t):
        # In order for a tile to match another, they must be properly rotated/flipped and
        # the sides must make sense, e.g. top-to-bottom or left-to-right.
        # The gruntwork of iterating through the rotations/flips is handled outside of this method.
        #
        # This function has the side effect that the matched tile is placed onto the 'table'
        # in the appropriate location.
        for our_side in self.scores:
            for their_side in t.scores:
                if self.scores[our_side] == t.scores[their_side] and (our_side, their_side) in valid_alignments:
                    if our_side == SIDE_TOP:
                        new_location = (self.location[0], self.location[1] - 1)
                    elif our_side == SIDE_BOTTOM:
                        new_location = (self.location[0], self.location[1] + 1)
                    elif our_side == SIDE_LEFT:
                        new_location = (self.location[0] - 1, self.location[1])
                    elif our_side == SIDE_RIGHT:
                        new_location = (self.location[0] + 1, self.location[1])
                        
                    t.place(new_location)
                    return True
        return False

    def strip_borders(self):
        # Remove the edge rows/columns and recalculate the tile size.
        new_image = {}
        for (x, y) in self.image:
            if x != 0 and y != 0 and x != self.size - 1 and y != self.size - 1:
                new_image[(x - 1, y - 1)] = self.image[(x, y)]
        self.image = new_image
        self.size = int(math.sqrt(len(self.image)))

    def place(self, location):
        self.location = location
        table[location] = self
        
def place_tile(tile):
    for location in table:
        t = table[location]
        for i in range(4):
            tile.rotate()
            if t.matches(tile):
                return True
            tile.hflip()
            if t.matches(tile):
                return True
            tile.vflip()
            if t.matches(tile):
                return True
    return False

def hunt_for_monsters():
    # Scan through each pixel in the assembled image, looking for anywhere
    # that matches the entire monster pattern.
    for (x1, y1) in big_tile.image:
        match = True
        for (x2, y2) in sea_monster:
            if big_tile.image.get((x1+x2, y1+y2), PIXEL_OFF) != PIXEL_ON:
                match = False
                break
        if match:
            # Mark that monster! Highlight the pixels
            for (x2, y2) in sea_monster:
                big_tile.image[(x1+x2, y1+y2)] = PIXEL_MONSTER

# Parse the list of image tiles, and save each line
with open('day20_input.txt') as f:
    tile_list = [line.rstrip('\n') for line in f]

tiles = []
for line in tile_list:
    if 'Tile' in line:
        tile_num = int(line.replace(':', '').split()[1])
        tile = Tile(tile_num)
        tiles.append(tile)
        y = 0
    elif PIXEL_OFF in line or PIXEL_ON in line:
        for x in range(len(line)):
            tile.image[(x, y)] = line[x]
        y += 1

for t in tiles:
    t.score()

# Let's pretend we're putting together a puzzle.
# Take one puzzle piece out of the pile and place it onto the "table".
box = tiles
table = {}
first_piece = box.pop()
first_piece.place((0, 0))

# Now go through the rest of the pieces, turning and flipping them,
# until we find one that fits onto it. Place it onto the table with the others.
#
# Keep doing this until there are no more left in the "box"!
while len(box) > 0:
    for i in range(len(box)):
        if place_tile(box[i]):
            box.pop(i)
            break

# Find out where the edges of the puzzle are...
x_min = min(table)[0]
y_min = min(table)[1]
x_max = max(table)[0]
y_max = max(table)[1]

# Now multiply the IDs of the corner pieces together.
product = 1
for location in [(x, y) for x in [x_min, x_max] for y in [y_min, y_max]]:
    product *= table[location].number
print 'Part One: product of corner tiles is {0}.'.format(product)

# The borders of each tile are not part of the actual image; start by removing them.
for loc in table:
    table[loc].strip_borders()

# Now, let's make a mega-tile that is the concatenation of all the little tiles.
small_tile_size = table[(0, 0)].size
big_tile_size = (small_tile_size * (y_max - y_min + 1))
big_tile = Tile(size=big_tile_size)

# Populate the big tile by offsetting the pixels of each little tile.
for (x1, y1) in table:
    for (x2, y2) in table[(x1, y1)].image:
        x_new = (x1 - x_min) * small_tile_size + x2
        y_new = (y1 - y_min) * small_tile_size + y2
        big_tile.image[(x_new, y_new)] = table[(x1, y1)].image[(x2, y2)]

# Now just brute-force rotate/flip until we find some monsters!
# No optimizations are made for bailing out early when we discover
# the correct orientation, but it doesn't seem to be too slow.
for i in range(4):
    big_tile.rotate()
    hunt_for_monsters()
    big_tile.hflip()
    hunt_for_monsters()
    big_tile.vflip()
    hunt_for_monsters()
    
# Count the remaining '#' pixels to determine 'roughness'. Done!
roughness = 0
for loc in big_tile.image:
    if big_tile.image[loc] == PIXEL_ON: roughness += 1
print 'Part Two: roughness is {0}.'.format(roughness)
    