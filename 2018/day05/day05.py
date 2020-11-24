with open('day05_input.txt') as f:
    polymer = f.read().rstrip('\n')

done = False

while not done:
    done = True
    idx = 0
    while idx < len(polymer) - 1:
        if polymer[idx] != polymer[idx+1] and polymer[idx].lower() == polymer[idx+1].lower():
            polymer = polymer[:idx] + polymer[idx+2:]
            done = False
        idx += 1

print polymer
print len(polymer)

with open('day05_input.txt') as f:
    polymer = f.read().rstrip('\n')

shortestPolymer = None
shortestPolymerLen = len(polymer)

for letter in range(ord('a'), ord('z') + 1):
    lowercase = chr(letter)
    uppercase = chr(letter).upper()
    shortPolymer = polymer.replace(lowercase, '').replace(uppercase, '')
    print "trying %s..." % lowercase

    done = False
    while not done:
        done = True
        idx = 0
        while idx < len(shortPolymer) - 1:
            if shortPolymer[idx] != shortPolymer[idx+1] and shortPolymer[idx].lower() == shortPolymer[idx+1].lower():
                shortPolymer = shortPolymer[:idx] + shortPolymer[idx+2:]
                done = False
            idx += 1

    if len(shortPolymer) < shortestPolymerLen:
        shortestPolymerLen = len(shortPolymer)
        shortestPolymer = shortPolymer

print shortestPolymer
print shortestPolymerLen

