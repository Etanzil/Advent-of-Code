from collections import defaultdict, deque

# Read the input data from the file
with open("day10.txt", "r") as file:
    lines = file.read().splitlines()

# Parse the grid
def grid(lines):
    g = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            g[x + y * 1j] = int(char)
    return g

g = {c: int(i) for c, i in grid(lines).items()}
max_height = max(g.values())

# first_coord, last_coord
trails = deque((coord, coord) for coord, height in g.items() if not height)

ratings = 0
trailheads = defaultdict(set)
directions = [-1, 1, -1j, 1j]

while trails:
    fc, lc = trails.popleft()

    for d in directions:
        if (h := g.get(lc + d, -1)) == g.get(lc) + 1:
            if h == max_height:
                trailheads[fc].add(lc + d)
                ratings += 1
            else:
                trails.append((fc, lc + d))

answer_a = sum(len(score) for score in trailheads.values())
answer_b = ratings

# Print the answers
print(f"Answer A: {answer_a}")
print(f"Answer B: {answer_b}")
