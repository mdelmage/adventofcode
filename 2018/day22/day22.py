DEPTH = 3558
TARGET = (15,740)
MODULO = 20183

TOOL_CHANGE_TIME = 7

TORCH         = 'T'
CLIMBING_GEAR = 'C'
NONE          = 'N'

ROCKY         = '.'
WET           = '='
NARROW        = '|'

UP            = 'U'
DOWN          = 'D'
LEFT          = 'L'
RIGHT         = 'R'

directions = [UP, DOWN, LEFT, RIGHT]
direction_to_coords = { UP     : ( 0, -1),
                        DOWN   : ( 0,  1),
                        LEFT   : (-1,  0),
                        RIGHT  : ( 1,  0)}

tools = { TORCH, CLIMBING_GEAR, NONE }

tool_usability = { ROCKY:  (TORCH, CLIMBING_GEAR),
                   WET:    (NONE, CLIMBING_GEAR),
                   NARROW: (NONE, TORCH)}

risk_to_ground_type = { 0: ROCKY,
                        1: WET,
                        2: NARROW }

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

current_tool = TORCH
erosion_level_history = {}
paths_by_len = {}
paths_by_loc = {}
map = {}

def geologic_index(x, y):
    index = None
    if x == 0 and y == 0:
        index = 0
    elif x == TARGET[0] and y == TARGET[1]:
        index = 0
    elif x == 0:
        index = y * 48271
    elif y == 0:
        index = x * 16807
    else:
        index = erosion_level(x - 1, y) * erosion_level(x, y - 1)

    return index

def erosion_level(x, y):
    if (x, y) in erosion_level_history:
        erosion = erosion_level_history[(x, y)]
        #print 'new erosion @ (%d, %d): %d' % (x, y, erosion_level)
    else:
        erosion = ((geologic_index(x, y) + DEPTH) % MODULO)
        erosion_level_history[(x, y)] = erosion

    return erosion

def risk(x, y):
    erosion = erosion_level(x, y)
    risk = erosion % 3
    ground_type = risk_to_ground_type[risk]
    map[(x, y)] = ground_type
    return risk

def record_path(x, y, tool, path):
    # Switch to torch if we've arrived and not already so equipped
    if (x, y) == TARGET and tool != TORCH:
        tool = TORCH
        path = path + (TOOL_CHANGE_TIME * tool)

    path_len = len(path)
    if path_len not in paths_by_len: paths_by_len[path_len] = {}

    if (x, y, tool) in paths_by_loc:
        recorded_path_len = len(paths_by_loc[(x, y, tool)])
        if path_len >= recorded_path_len:
            return
        else:
            print 'path shortened from %d to %d' % (recorded_path_len, path_len)

    # Record the new path
    paths_by_loc[(x, y, tool)] = path
    paths_by_len[path_len][(x, y, tool)] = path


def discover_paths(path_len):
    if path_len not in paths_by_len: paths_by_len[path_len] = {}
    # First, find all the paths that are one shorter than the specified one,
    # and try to extend the path without switching tools
    one_shorter_paths = paths_by_len[path_len - 1]
    for tup in one_shorter_paths:
        x, y, tool = tup
        path = one_shorter_paths[(x, y, tool)]
        for dir in directions:
            x_next = x + direction_to_coords[dir][0]
            y_next = y + direction_to_coords[dir][1]
            if (x_next, y_next) in map and tool in tool_usability[map[(x_next, y_next)]]:
                #print '%s: going %d,%d-->%d,%d with tool %s: %s' % (path, loc[0], loc[1], x_next, y_next, tool, one_shorter_paths[loc][tool] + dir)
                record_path(x_next, y_next, tool, path + dir)


    # Then, find all the paths that are TOOL_CHANGE_TIME shorter,
    # and try to extend the path by switching tools
    tool_shorter_paths = paths_by_len.get(path_len - (TOOL_CHANGE_TIME + 1), {})
    for tup in tool_shorter_paths:
        x, y, tool = tup
        path = tool_shorter_paths[(x, y, tool)]
        for new_tool in tools:
            if tool != new_tool:
                for dir in directions:
                    x_next = x + direction_to_coords[dir][0]
                    y_next = y + direction_to_coords[dir][1]
                    if (x_next, y_next) in map and new_tool in tool_usability[map[(x, y)]] and new_tool in tool_usability[map[(x_next, y_next)]]:
                        record_path(x_next, y_next, new_tool, path + (TOOL_CHANGE_TIME * new_tool) + dir)


for y in range(TARGET[1] + TOOL_CHANGE_TIME + 1):
    for x in range(TARGET[0] + 35):
        risk(x, y)

total_risk = 0
for y in range(TARGET[1] + 1):
    for x in range(TARGET[0] + 1):
        total_risk += risk(x, y)

print 'Risk to reach target at %s with depth %d: %d' % (TARGET, DEPTH, total_risk)

# Part 2: Initial paths state
initial_state = (0, 0, TORCH)
final_state = (TARGET[0], TARGET[1], TORCH)

paths_by_len[0] = { initial_state: ''}
paths_by_loc[initial_state] = ''

path_length = 1
while final_state not in paths_by_loc:
    discover_paths(path_length)
    path_length += 1

# Could go up to TOOL_CHANGE_TIME beyond the target coordinates
for i in range(TOOL_CHANGE_TIME):
    discover_paths(path_length)
    path_length += 1
'''
loc = (0, 0)
traveled = []
tool_changes = []
tool = TORCH
for chr in paths_by_loc[final_state]:
    if chr in tools:
        tool = chr
        tool_changes.append(loc)
        continue
    loc = (loc[0] + direction_to_coords[chr][0], loc[1] + direction_to_coords[chr][1])
    traveled.append(loc)

print ''
for y in range(TARGET[1] + TOOL_CHANGE_TIME + 1):
    row_str = ''
    for x in range(TARGET[0] + 35):
        if (x, y) in tool_changes:
            row_str += color.RED + map[(x, y)] + color.END
        elif (x, y) in traveled:
            row_str += color.BOLD + map[(x, y)] + color.END
        else:
            row_str += map[(x, y)]
    print row_str
print ''
'''
print 'Target path is len %d' % len(paths_by_loc[final_state])
