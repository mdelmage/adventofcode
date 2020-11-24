NUM_PLAYERS = 423
NUM_MARBLES = 7194400 # 100x larger than 72061 from Part A. Woof.

circle = [0]
scores = {}
current_pos = 0

for marble in range(1, NUM_MARBLES + 1):
    if marble % 100000 == 0: print marble
    if marble % 23 is 0:
        scores[marble % NUM_PLAYERS] = scores.get(marble % NUM_PLAYERS, 0) + marble
        remove_pos = (current_pos - 7) % len(circle)
        scores[marble % NUM_PLAYERS] += circle.pop(remove_pos)
        current_pos = remove_pos
    else:
        insert_pos = (current_pos + 2) % len(circle)
        circle.insert(insert_pos, marble)
        current_pos = insert_pos

winning_player = max(scores, key=scores.get)
print "Winning player is %d with score: %d" % (winning_player, scores[winning_player])
