import operator
import sys

CHR_HEADER = '^'
CHR_FOOTER = '$'
CHR_OPTION = '|'

directions = {'N': (0, 1),
              'S': (0, -1),
              'W': (-1, 0),
              'E': (1, 0)}

# Parse the regex
with open('day20_input.txt') as f:
    regex_main = f.readline().rstrip('\n')

regex_str1 = '^WNE$'
regex_str2 = '^ENWWW(NEEE|SSE(EE|N))$'
regex_str3 = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
regex_str4 = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
regex_str5 = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
regex_strs = [regex_main]

def regex_bare_string(str):
    paren_pos = str.find('(')
    if paren_pos > 0:
        return (str[:paren_pos], str[paren_pos:])
    else:
        return (str, '')

def regex_options_string(str):
    CHR_OPTION_SEPARATOR = '!'
    paren_level = 1

    # Find the Level 1 separators and change them to another symbol,
    # so it is easy to tokenize just those (and not all the Level 2+ ones).
    for idx in range(1, len(str)):
        if str[idx] is ('('): paren_level += 1
        if str[idx] is (')'): paren_level -= 1
        if paren_level is 1 and str[idx] is CHR_OPTION:
            #print '%s-->%s' % (str, str[:idx] + CHR_OPTION_SEPARATOR + str[idx+1:])
            str = str[:idx] + CHR_OPTION_SEPARATOR + str[idx+1:]
        if paren_level is 0:
            options = ()
            for option_str in str[1:idx].split(CHR_OPTION_SEPARATOR):
                #print 'option %s' % option_str
                options += (string_to_regex(option_str),)
            #print '%s and %s' % (options, str[idx+1:])
            return (options, str[idx+1:])
    print "whoops: %s" % str
    return ((), '')


def string_to_regex(str):
    if len(str) is 0:
        return ''
    elif str[0] in directions:
        # Generate a list of regex items
        regex = []
    else:
        # Generate a tuple of regex options
        regex = ()

    while len(str) > 0:
        if str[0] in directions:
            (regex_str, leftover_str) = regex_bare_string(str)
        else:
            (regex_str, leftover_str) = regex_options_string(str)

        regex.append(regex_str)
        str = leftover_str

    #print regex
    return regex

def regex_to_strings(regex, level=0):
    # tuples return a logical OR of child strings
    if type(regex) is tuple:
        strings = []
        for item in regex:
            for child_string in regex_to_strings(item, level + 1):
                strings.append(child_string)
        #print 'Level %d: tuple %s-->%s' % (level, regex, strings)
        return strings

    # lists return a logical AND of child strings
    if type(regex) is list:
        strings = ['']
        for part in regex:
            new_strings = []
            for string in strings:
                for child_string in regex_to_strings(part, level + 1):
                    new_strings.append(string + child_string)
            strings = new_strings
        #print 'Level %d: list %s-->%s' % (level, regex, strings)
        return strings

    # bare strings just return themselves
    #print 'Level %d: string %s-->%s' % (level, regex, [regex])
    return [regex]

# Calculate the (x, y) coordinates of the room we'd be in
# if we followed the directions, starting from room (0, 0).
def coordinates(string):
    loc = (0, 0)

    for chr in string:
        loc = tuple(map(operator.add, loc, directions[chr]))

    return loc

# Calculate the (x, y) coordinates of the room we'd be in
# if we followed the directions, starting from given room
def move(loc, chr):
    loc = tuple(map(operator.add, loc, directions[chr]))
    return loc

# Strip out all the options that end up going nowhere.
def cleanup_for_shortest_length(str):
    str = str.lstrip(CHR_HEADER).rstrip(CHR_FOOTER)

    done = False
    repl = 0
    while not done:
        done = True
        last_open_paren = None
        for idx in range(len(str) - 1):
            if str[idx] == '(': last_open_paren = idx
            if str[idx:idx+2] == '|)':
                if coordinates(str[last_open_paren+1:idx]) == (0, 0):
                    str = str[:last_open_paren] + str[idx+2:]
                    done = False
                    repl += 1
                    break
    #print '%d replacements made!' % repl
    return (str, repl)

# Only make the specified amount of shortest paths,
# then start using the long way around.
# We do this to discover new rooms that were optimized out.
def cleanup_for_completeness(str, num_short_paths):
    str = str.lstrip(CHR_HEADER).rstrip(CHR_FOOTER)
    num_short_paths_remaining = num_short_paths
    done = False

    while not done:
        done = True
        last_open_paren = None
        for idx in range(len(str) - 1):
            if str[idx] == '(': last_open_paren = idx
            if str[idx:idx+2] == '|)':
                if coordinates(str[last_open_paren+1:idx]) == (0, 0):
                    if num_short_paths_remaining > 0:
                        str = str[:last_open_paren] + str[idx+2:]
                    else:
                        str = str[:last_open_paren] + str[last_open_paren+1:idx] + str[idx+2:]
                    num_short_paths_remaining -= 1
                    done = False
                    break
    #print '%d replacements made!' % num_short_paths
    return str

for str in regex_strs:
    (clean_str, short_paths) = cleanup_for_shortest_length(str)
    regex = string_to_regex(clean_str)
    rooms = {}

    strings = regex_to_strings(regex)
    for i in range(len(strings)):
        string = strings[i]
        loc = (0, 0)
        for j in range(len(string)):
            loc = move(loc, string[j])
            if j + 1 < rooms.get(loc, sys.maxint):
                rooms[loc] = j + 1

    print 'minmax path: %d' % max(rooms.values())

    # lol i'm so tired of Day 20
    # The paths have to be optimized from the back, one at a time,
    # and then the rooms need to be rechecked for shortest path.
    # Number of times is by inspection of cleanup_for_shortest_length() above.
    while short_paths >= 0:
        clean_str = cleanup_for_completeness(str, short_paths)
        regex = string_to_regex(clean_str)

        strings = regex_to_strings(regex)
        for i in range(len(strings)):
            string = strings[i]
            loc = (0, 0)
            for j in range(len(string)):
                loc = move(loc, string[j])
                if j + 1 < rooms.get(loc, sys.maxint):
                    rooms[loc] = j + 1

        short_paths -= 1


    thousanders = 0
    for path_length in sorted(rooms.values()):
        if path_length >= 1000: thousanders += 1
    print '%d thousanders in this %d-sized map' % (thousanders, len(rooms))
