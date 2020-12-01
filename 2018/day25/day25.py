class Point(object):
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return '(%d,%d,%d,%d)' % (self.w, self.x, self.y, self.z)

    def manhattan_distance(self, p):
        return abs(self.w - p.w) + \
               abs(self.x - p.x) + \
               abs(self.y - p.y) + \
               abs(self.z - p.z)

class Constellation(object):
    def __init__(self, points):
        self.points = points

    def __str__(self):
        print_str = ''
        for p in self.points:
            print_str += str(p)
        return print_str
    
    def merge(self, c):
        match = False
        for (p1, p2) in [(a, b) for a in self.points for b in c.points]:
            if p1.manhattan_distance(p2) <= 3:
                match = True
                break
        
        if match:
            self.points += c.points
        
        return match

constellations = []
merged_constellation = None

# Parse the input file
with open('day25_input.txt') as f:
    lines = [line.rstrip('\n') for line in f]
    for line in lines:
        p = [int(x) for x in line.split(',')]
        p = Point(p[0], p[1], p[2], p[3])
        c  = Constellation([p])
        constellations.append(c)

done = False
while not done:
    done = True
    if merged_constellation is not None:
        constellations.remove(merged_constellation)
        merged_constellation = None
        print '%d constellations remain.' % len(constellations)
    for (c, d) in [(a, b) for a in constellations for b in constellations]:
        if c is not d and c.merge(d):
            done = False
            merged_constellation = d
            break
