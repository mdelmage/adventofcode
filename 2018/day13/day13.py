track = []
carts = {}
collision = False
ticks = 0

chr_to_vel = { '>': ( 1,  0),
               '<': (-1,  0),
               'v': ( 0,  1),
               '^': ( 0, -1)}

cart_swaps = { '>': '-',
               '<': '-',
               'v': '|',
               '^': '|'}

curve_vel = { ('\\', (-1,  0)): ( 0, -1),
              ('\\', ( 1,  0)): ( 0,  1),
              ('\\', ( 0, -1)): (-1,  0),
              ('\\', ( 0,  1)): ( 1,  0),
              ( '/', (-1,  0)): ( 0,  1),
              ( '/', ( 1,  0)): ( 0, -1),
              ( '/', ( 0, -1)): ( 1,  0),
              ( '/', ( 0,  1)): (-1,  0)}

int_vel = { (0, (-1,  0)): ( 0,  1),
            (0, ( 1,  0)): ( 0, -1),
            (0, ( 0, -1)): (-1,  0),
            (0, ( 0,  1)): ( 1,  0),

            (1, (-1,  0)): (-1,  0),
            (1, ( 1,  0)): ( 1,  0),
            (1, ( 0, -1)): ( 0, -1),
            (1, ( 0,  1)): ( 0,  1),

            (2, (-1,  0)): ( 0, -1),
            (2, ( 1,  0)): ( 0,  1),
            (2, ( 0, -1)): ( 1,  0),
            (2, ( 0,  1)): (-1,  0)}

class Cart:
    def __init__(self, x, y, chr):
        self._pos = (x, y)
        self._vel = chr_to_vel[chr]
        self._int_count = 0

    def __str__(self):
        return 'Cart at %s vel %s int_count %d' % (self._pos, self._vel, self._int_count)

    def track_pos(self):
        # Carts are indexed by (y,x) so they sort nicely into movement-order
        return (self._pos[1], self._pos[0])

    def move(self):
        global carts

        #print 'Moving cart at %s to %s' % (self._pos, tuple(map(sum, zip(self._pos, self._vel))))
        del carts[self.track_pos()]
        self._pos = tuple(map(sum, zip(self._pos, self._vel)))

        if self.track_pos() in carts:
            # Collision!
            print 'Collision at (%d, %d)!' % (self._pos)
            del carts[self.track_pos()]
            return False
        elif self.inCurve():
            self._vel = curve_vel[track[self._pos[1]][self._pos[0]], self._vel]
        elif self.inIntersection():
            self._vel = int_vel[self._int_count, self._vel]
            self._int_count = (self._int_count + 1) % 3

        carts[self.track_pos()] = self
        return True

    def at(self, x, y):
        return self._pos == (x, y)

    def inCurve(self):
        return track[self._pos[1]][self._pos[0]] in ['\\', '/']

    def inIntersection(self):
        return track[self._pos[1]][self._pos[0]] is '+'


# Build the track and add carts
with open('day13_input.txt') as f:
    input = [line.rstrip('\n') for line in f]
    y = 0
    for line in input:
        row = []
        x = 0
        for chr in line:
            if chr in chr_to_vel:
                row.append(cart_swaps[chr])
                # Carts are indexed by (y,x) so they sort nicely into movement-order
                carts[(y, x)] = Cart(x, y, chr)
            else:
                row.append(chr)

            x += 1
        track.append(row)
        y += 1
        

while len(carts) > 1:
    ticks += 1
    for cart in sorted(carts):
        # Could have crashed already, check!
        if cart in carts: carts[cart].move()

print 'Simulation ended on Tick %d.' % ticks

# Okay so there's only one in there but...
for cart in carts:
    print carts[cart]
