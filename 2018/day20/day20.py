import regex
import sys

DIRECTIONS = ['N', 'E', 'W', 'S']

MOVES = { 'N': ( 0,  1),
          'S': ( 0, -1),
          'W': (-1,  0),
          'E': ( 1,  0)}

USELESS_MOVES = ['NS', 'SN', 'EW', 'WE']

sys.setrecursionlimit(1500)

# Parse the regex
with open('day20_input.txt') as f:
    regex_main = f.readline().rstrip('\n')

regex_str1 = '^WNE$'
regex_str2 = '^ENWWW(NEEE|SSE(EE|N))$'
regex_str3 = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
regex_str4 = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
regex_str5 = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
regex_strmatt = '^(EEEEEEEEEEE|EEEEEEESWWWWNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN)$'
regex_strs = [regex_str1, regex_str2, regex_str3, regex_str4, regex_str5, regex_strmatt, regex_main]

for s in regex_strs:
    print '---'
    full_matches = []
    partial_matches = [('', (0, 0))]
    pattern = regex.compile(s)
    shortest_traversal = {}
    longest_path = 0

    # Do a "flood-style" search of the facility: add one move to the end
    # of the path and check if that is a "partial match" of the regex, aka,
    # it represents the beginning of a longer string that *could match*.
    #
    # Add that to the list of paths to check later. Don't worry about
    # exhaustively matching the whole regex.
    while len(partial_matches) > 0:
        partial_matches_next = []
        for pm in partial_matches:
            for c in DIRECTIONS:
                new_path = pm[0] + c
                new_move = MOVES[c]
                new_location = (pm[1][0] + new_move[0], pm[1][1] + new_move[1])
                m = pattern.fullmatch(new_path, partial=True)
                if m is not None:
                    # Match! Add a not-useless move and keep going.
                    # A useless move is one that immediately undoes the previous move.
                    if new_path[-2:] not in USELESS_MOVES:
                        partial_matches_next.append((new_path, new_location))
                    if new_location not in shortest_traversal:
                        shortest_traversal[new_location] = new_path


        partial_matches = partial_matches_next

    thousanders = 0
    longest_path = 0
    for location in shortest_traversal:
        path_len = len(shortest_traversal[location])
        if path_len >= 1000:
            thousanders += 1
        if path_len > longest_path:
            longest_path = path_len
    print longest_path
    print thousanders