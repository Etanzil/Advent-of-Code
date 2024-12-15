def get_input(day, test=False):

    filename = f"day{day}{'_test' if test else ''}.txt"
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None


# HELPERS

dirs = {
    "v": (1, 0),
    "^": (-1, 0),
    ">": (0, 1),
    "<": (0, -1)
}

def visualise_grid(grid, rows, cols): #Added rows and cols arguments
    for r in range(rows):
        row = ""
        for c in range(cols):
            row += grid[(r, c)]
        print(row)
    print()

def score_grid(grid, char, rows, cols):#Added rows and cols arguments
    score = 0
    for r in range(rows):
        for c in range(cols):
            if grid[(r, c)] == char:
                score += 100 * r + c
    return score

# PART 1

def get_grid(input_data):
    grid = dict()
    i = 0
    cols = len(input_data[0])
    robot = None
    while i < len(input_data):
        if input_data[i] == "":
            i += 1
            break
        for j in range(len(input_data[i])):
            if input_data[i][j] == "@":
                robot = (i, j)
            grid[(i, j)] = input_data[i][j]
        i += 1
    rows = i - 1
    return grid, i, rows, cols, robot

def try_move(grid, robot, dir):
    next_pos = (robot[0] + dir[0], robot[1] + dir[1])
    next_type = grid.get(next_pos, "#")
    if next_type == "#":
        return grid, robot
    elif next_type == ".":
        grid[robot] = "."
        grid[next_pos] = "@"
        return grid, next_pos
    else:
        # There is a box in the way, see if it is movable
        movable = False
        next_check_pos = (next_pos[0] + dir[0], next_pos[1] + dir[1])
        while True:
            next_check_type = grid.get(next_check_pos, "#")
            if next_check_type == "#":
                break
            elif next_check_type == "O":
                next_check_pos = (next_check_pos[0] + dir[0], next_check_pos[1] + dir[1])
            else:
                grid[next_check_pos] = "O"
                movable = True
                break
        if movable:
            grid[robot] = "."
            grid[next_pos] = "@"
            return grid, next_pos
        return grid, robot

input_data = get_input(15)  # Read from file
if input_data:
    grid, i, rows, cols, robot = get_grid(input_data)
    moves = "".join(input_data[i:])

    for move in moves:
        grid, robot = try_move(grid, robot, dirs[move])
        #visualise_grid(grid,rows,cols)

    print("Part 1:", score_grid(grid, "O",rows,cols))

# PART 2

def moveable(grid, dir, box):
    # Where box is the coordinates of the left side of the box
    next_left_pos = (box[0]+dir[0], box[1])
    next_right_pos = (next_left_pos[0], next_left_pos[1]+1)
    if grid[next_left_pos] == "." and grid[next_right_pos] == ".":
        return True
    if grid[next_left_pos] == "#" or grid[next_right_pos] == "#":
        return False
    if grid[next_left_pos] == "[":
        return moveable(grid, dir, next_left_pos)
    if grid[next_left_pos] == "." and grid[next_right_pos] == "[":
        return moveable(grid, dir, next_right_pos)
    if grid[next_left_pos] == "]" and grid[next_right_pos] == ".":
        return moveable(grid, dir, (next_left_pos[0], next_left_pos[1]-1))
    # Otherwise we have two boxes!!
    return moveable(grid, dir, (next_left_pos[0], next_left_pos[1]-1)) and moveable(grid, dir, next_right_pos)

def actually_move(grid, dir, box, moved):
    if box in moved:
        return grid
    next_left_pos = (box[0]+dir[0], box[1])
    next_right_pos = (next_left_pos[0], next_left_pos[1]+1)
    if grid[next_left_pos] == "." and grid[next_right_pos] == ".":
        grid[next_left_pos] = "["
        grid[next_right_pos] = "]"
        grid[box] = "."
        grid[(box[0],box[1]+1)] = "."
        moved.add(box)
        return grid
    if grid[next_left_pos] == "[":
        grid = actually_move(grid, dir, next_left_pos, moved)
    if grid[next_left_pos] == "]":
        grid = actually_move(grid, dir, (next_left_pos[0],next_left_pos[1]-1), moved)
    if grid[next_right_pos] == "[":
        grid = actually_move(grid, dir, next_right_pos, moved)
    grid[next_left_pos] = "["
    grid[next_right_pos] = "]"
    grid[box] = "."
    grid[(box[0], box[1]+1)] = "."
    moved.add(box)
    return grid
def try_move_2(grid, robot, dir):
    next_pos = (robot[0]+dir[0],robot[1]+dir[1])
    next_type = grid.get(next_pos, "#")
    if next_type == "#":
        return grid, robot
    elif next_type == ".":
        grid[robot] = "."
        grid[next_pos] = "@"
        return grid, next_pos
    else:
        # There is a box in the way, see if it is movable
        if dir in [(0,1),(0,-1)]:
            # Simple horizontal movement case
            movable = False
            next_check_pos = (next_pos[0]+dir[0],next_pos[1]+dir[1])
            while True:
                next_check_type = grid.get(next_check_pos, "#")
                if next_check_type == "#":
                    break
                elif next_check_type in "[]":
                    next_check_pos = (next_check_pos[0]+dir[0],next_check_pos[1]+dir[1])
                else:
                    movable = True
                    break
            if movable:
                grid[robot] = "."
                grid[next_pos] = "@"
                box_pos = (next_pos[0]+dir[0],next_pos[1]+dir[1])
                while True:
                    if grid[box_pos] == ".":
                        grid[box_pos] = "[" if dir == (0,-1) else "]"
                        break
                    else:
                        grid[box_pos] = "[" if grid[box_pos] == "]" else "]"
                        box_pos = (box_pos[0]+dir[0],box_pos[1]+dir[1])
                return grid, next_pos
            return grid, robot
        else:
            # Complicated vertical movement case
            left = next_pos if next_type == "[" else (next_pos[0],next_pos[1]-1)
            if moveable(grid, dir, left):
                grid = actually_move(grid, dir, left, set())
                grid[next_pos] = "@"
                grid[robot] = "."
                return grid, next_pos
            return grid, robot

def get_grid_2(input_data):
    grid = dict()
    i = 0
    cols = 2 * len(input_data[0])
    robot = None
    while i < len(input_data):
        if input_data[i] == "":
            i += 1
            break
        for j in range(len(input_data[i])):
            val = input_data[i][j]
            l = None
            r = None
            if val == ".":
                l = "."
                r = "."
            elif val == "O":
                l = "["
                r = "]"
            elif val == "#":
                l = "#"
                r = "#"
            else:
                l = "@"
                r = "."
                robot = (i, j * 2)
            grid[(i, j * 2)] = l
            grid[(i, j * 2 + 1)] = r
        i += 1
    rows = i - 1
    return grid, i, rows, cols, robot

input_data = get_input(15)  # Read from file
if input_data:
    grid, _, rows, cols, robot = get_grid_2(input_data)
    moves = "".join(input_data[i:])

    for move in moves:
        grid, robot = try_move_2(grid, robot, dirs[move])
        #visualise_grid(grid,rows,cols)

    print("Part 2:", score_grid(grid, "[",rows,cols))
