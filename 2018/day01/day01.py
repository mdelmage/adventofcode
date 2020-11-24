freqs = {}
current_freq = 0
first_freq = 0
repeat_freq = 0

with open('day01_input.txt') as f:
    freq_changes = [int(line.rstrip('\n').replace('+', '')) for line in f]

while repeat_freq is 0:
    for freq_change in freq_changes:
        current_freq += freq_change
        if current_freq in freqs and repeat_freq is 0:
            print '%d already seen!' % current_freq
            repeat_freq = 1
        else:
            freqs[current_freq] = 1
    if first_freq is 0:
        print 'final frequency = %d' % current_freq
        first_freq = 1

