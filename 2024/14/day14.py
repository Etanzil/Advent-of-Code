from re import findall
from statistics import variance

def parse_input(filename):
    data = open(filename).read()
    return [[int(n) for n in findall(r"(-?\d+)", item)] for item in data.split("\n")]

def simulate(robots, t, W, H):
    return [((sx + t * vx) % W, (sy + t * vy) % H) for (sx, sy, vx, vy) in robots]

def calculate_safety_factor(positions, W, H):
    mid_x, mid_y = W // 2, H // 2
    q1 = q2 = q3 = q4 = 0
    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue
        if x < mid_x and y < mid_y:
            q1 += 1
        elif x >= mid_x and y < mid_y:
            q2 += 1
        elif x < mid_x and y >= mid_y:
            q3 += 1
        elif x >= mid_x and y >= mid_y:
            q4 += 1
    return q1 * q2 * q3 * q4

def find_easter_egg_time(robots, W, H):
    bx, bxvar, by, byvar = 0, 10 * 100, 0, 10 * 1000
    for t in range(max(W, H)):
        xs, ys = zip(*simulate(robots, t, W, H))
        if (xvar := variance(xs)) < bxvar:
            bx, bxvar = t, xvar
        if (yvar := variance(ys)) < byvar:
            by, byvar = t, yvar
    return bx + ((pow(W, -1, H) * (by - bx)) % H) * W

def main():
    filename = "day14.txt"
    W, H = 101, 103
    robots = parse_input(filename)
    positions = simulate(robots, 100, W, H)
    print(calculate_safety_factor(positions, W, H))
    print(find_easter_egg_time(robots, W, H))

if __name__ == "__main__":
    main()
