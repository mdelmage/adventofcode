with open('day07_input.txt') as f:
    input = [line.rstrip('\n') for line in f]

reqs = {}
for idx in range(ord('A'), ord('Z') + 1):
    reqs[chr(idx)] = []

for line in input:
    tokens = line.split()
    #  0    1 2    3  4        5      6    7 8   9
    # 'Step A must be finished before step B can begin.'
    reqs[tokens[7]].append(tokens[1])

# Part A
done = False
steps = ''
while len(reqs) > 0:
    # Scan requirements for the next step to take
    for key in sorted(reqs.keys()):
        if len(reqs[key]) is 0:
            # No requirements; hit it
            steps += key
            del reqs[key]
            for removal_key in sorted(reqs.keys()):
                if key in reqs[removal_key]:
                    reqs[removal_key].remove(key)
            break

print steps

# Part B
time = 0
workers = {}
reqs = {}
for idx in range(ord('A'), ord('Z') + 1):
    reqs[chr(idx)] = []

for line in input:
    tokens = line.split()
    #  0    1 2    3  4        5      6    7 8   9
    # 'Step A must be finished before step B can begin.'
    reqs[tokens[7]].append(tokens[1])

while len(reqs) > 0 or len(workers) > 0:
    # Process workers/jobs
    finished_jobs = []
    for key in workers:
        workers[key] -= 1
        if workers[key] is 0:
            finished_jobs.append(key)
    for key in finished_jobs:
        print "Time %d: worker finished step %s" % (time, key)
        del workers[key]
        for removal_key in sorted(reqs.keys()):
            if key in reqs[removal_key]:
                reqs[removal_key].remove(key)

    ready = False
    while len(reqs) > 0 and len(workers) < 5 and not ready:
        ready = True
        # Scan requirements for the next step to take
        for key in sorted(reqs.keys()):
            if len(reqs[key]) is 0 and len(workers) < 5:
                workers[key] = ord(key) - ord('A') + 61
                print "Time %d: worker assigned step %s for %d time" % (time, key, workers[key])
                ready = False
                del reqs[key]
    time += 1