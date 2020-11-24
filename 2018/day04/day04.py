minutes_sleeping = {}
minutes = {}

with open('day04_input.txt') as f:
    log = [line.rstrip('\n') for line in f]

log.sort()
sleep_start = 0
sleeping = False

for event in log:
    tokens = event.replace(' ', '').replace(':', ',').replace(']', ',').replace('#', ',').replace('begins', ',').split(',')
    if 'begins shift' in event:
        current_guard = int(tokens[3])
    elif 'sleep' in event:
        sleep_start = int(tokens[1])
    elif 'wake' in event:
        sleep_end = int(tokens[1])
        for minute in range(sleep_start, sleep_end):
            minutes_sleeping[current_guard] = minutes_sleeping.get(current_guard, 0) + 1
            minutes[current_guard, minute] = minutes.get((current_guard, minute), 0) + 1

sleepiest_guard = max(minutes_sleeping, key=minutes_sleeping.get)
print 'Sleepiest guard=%d, %d minutes asleep' % (sleepiest_guard,
                                                 max(minutes_sleeping.values()))
sleep_minutes = {}
for minute in range(60):
    sleep_minutes[minute] = minutes.get((sleepiest_guard, minute), 0)
    print ":%02d = %d" % (minute, minutes.get((sleepiest_guard, minute), 0))
sleepiest_part1_minute = max(sleep_minutes, key=sleep_minutes.get)

print 'Part 1 Answer = %d' % (sleepiest_guard * sleepiest_part1_minute)

sleepiest_minute = max(minutes, key=minutes.get)
print 'Sleepiest minute: guard=%d, %d minutes asleep' % (sleepiest_minute[0], sleepiest_minute[1])
print 'Part 2 Answer = %d' % (sleepiest_minute[0] * sleepiest_minute[1])