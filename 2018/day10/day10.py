with open('day10_input.txt') as f:
    input = [line.rstrip('\n') for line in f]

lights = []
for light in input:
    tokens = light.replace(' ', '').replace('<', ',').replace('>', ',').split(',')
    lights.append([int(tokens[1]), int(tokens[2]), int(tokens[4]), int(tokens[5])])

iteration = 0
while True:
    min_x = 100000
    max_x = -100000
    min_y = 100000
    max_y = -100000
    for light in lights:
        light[0] += light[2]
        light[1] += light[3]
        min_x = min(min_x, light[0])
        max_x = max(max_x, light[0])
        min_y = min(min_y, light[1])
        max_y = max(max_y, light[1])
    iteration += 1
    if max_y - min_y < 10: break

message = {}
for light in lights:
    message[(light[0], light[1])] = 1
    
print iteration
for y in range(min_y, max_y + 1):
    line = ""
    for x in range(min_x, max_x + 1):
        if (x, y) in message:
            line += '*'
        else:
            line += ' '
    print line