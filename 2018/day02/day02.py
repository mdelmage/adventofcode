doubles_count = 0
triples_count = 0

with open('day02_input.txt') as f:
    box_ids = [line.rstrip('\n') for line in f]

for id in box_ids:
    map = {}
    for chr in id:
        map[chr] = map.get(chr, 0) + 1
    for key, value in map.iteritems():
        if value is 2:
            doubles_count = doubles_count + 1
            break
    for key, value in map.iteritems():
        if value is 3:
            triples_count = triples_count + 1
            break

print 'Doubles: %d' % doubles_count
print 'Triples: %d' % triples_count
print 'Checksum: %d' % (doubles_count * triples_count)

for id1 in box_ids:
    for id2 in box_ids:
        diff = 0
        combined_id = ''
        for chr in range(len(id1)):
            if abs(ord(id1[chr]) - ord(id2[chr])) > 0:
                diff = diff + 1
            else:
                combined_id += id1[chr]
        if diff is 1:
            print 'Combined ID: %s' % combined_id

