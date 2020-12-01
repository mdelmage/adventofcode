import regex
import sys

DIRECTIONS = ['N', 'E', 'W', 'S']

MOVES = { 'N': ( 0,  1),
          'S': ( 0, -1),
          'W': (-1,  0),
          'E': ( 1,  0)}

sys.setrecursionlimit(1500)

# Parse the regex
with open('day20_input.txt') as f:
    regex_main = f.readline().rstrip('\n')

regex_str1 = '^WNE$'
regex_str2 = '^ENWWW(NEEE|SSE(EE|N))$'
regex_str3 = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
regex_str4 = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
regex_str5 = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
regex_strs = [regex_str1, regex_str2, regex_str3, regex_str4, regex_str5, regex_main]

for s in regex_strs:
    print '---'
    full_matches = []
    partial_matches = [('', (0, 0))]
    pattern = regex.compile(s)
    traversal = {}
    longest_path = 0
    while len(partial_matches) > 0:
        #print '%d / %d' % (len(partial_matches[0][0]), len(partial_matches))
        #print partial_matches
        partial_matches_next = []
        for pm in partial_matches:
            for c in DIRECTIONS:
                new_path = pm[0] + c
                new_move = MOVES[c]
                new_location = (pm[1][0] + new_move[0], pm[1][1] + new_move[1])
                m = pattern.fullmatch(new_path, partial=True)
                if m is not None:
                    if m.partial:
                        if new_location not in traversal or len(traversal[new_location][0]) >= len(new_path):
                            partial_matches_next.append((new_path, new_location))
                            traversal[new_location] = new_path
                    else:
                        if new_location not in traversal or len(traversal[new_location][0]) >= len(new_path):
                            full_matches.append(new_path)
                            traversal[new_location] = new_path
                            if len(new_path) >= longest_path:
                                longest_path = len(new_path)
        partial_matches = partial_matches_next
    print longest_path