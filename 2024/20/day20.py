file_path = "day20.txt"  # Path to the input file

with open(file_path, "r") as f:
    data = f.read()

grid = [[x for x in row] for row in data.split('\n')]
m = len(grid)
n = len(grid[0])
from heapq import heappush, heappop 

dirs = [[0, 1], [-1, 0], [0, -1], [1, 0]]

for i in range(m):
    for j in range(n):
        if grid[i][j] == 'S':
            si, sj = i, j
        elif grid[i][j] == 'E':
            ei, ej = i, j

def bfs(si, sj, ei, ej):
    pq = []
    heappush(pq, (0, si, sj)) # score, curri, currj
    d = {}
    best = None

    while pq:
        sc, ci, cj = heappop(pq)
        
        if (ci, cj) not in d: d[(ci, cj)] = sc
        else: continue

        if ci == ei and cj == ej: best = sc

        for dir in dirs:
            ni, nj = ci + dir[0], cj + dir[1]
            if 0<=ni<m and 0<=nj<n and grid[ni][nj] != '#':
                heappush(pq, (sc+1, ni, nj))
    return d, best

def step_distance(a, b): # manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

distances_start, best_no_cheat = bfs(si, sj, ei, ej)
distances_end, _ = bfs(ei, ej, si, sj)

def paths_with_cheat(cheat_threshold, save_seconds):
    res = 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] == '#' or (i, j) not in distances_start: continue
            for k in range(max(i-cheat_threshold, 0), min(i+cheat_threshold, m-1) + 1):
                for l in range(max(j-cheat_threshold, 0), min(j+cheat_threshold, n-1) + 1):
                    sd = step_distance((i, j), (k, l))
                    if (
                        sd > cheat_threshold or 
                        grid[k][l] == '#' or
                        (k, l) not in distances_end
                    ): 
                        continue
                    dist = distances_start[(i, j)] + distances_end[(k, l)] + sd
                    
                    if dist <= best_no_cheat-save_seconds:
                        res += 1
    
    return res
paths_with_cheat(2, 100)
paths_with_cheat(20, 100)
