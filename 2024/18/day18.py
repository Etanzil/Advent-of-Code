from time import perf_counter_ns
from typing import Any

def profiler(method):

    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        time_len = min(9, ((len(str(perf_counter_ns() - start_time))-1)//3)*3)
        time_conversion = {9: 'seconds', 6: 'milliseconds',
                             3: 'microseconds', 0: 'nanoseconds'}
        print(f"Method {method.__name__} took : {(perf_counter_ns() - start_time) / (10**time_len)} {time_conversion[time_len]}")
        return ret

    return wrapper_method


def maze(pts, grid_size=71):
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)

    seen = set()
    to_visit = [(start, 0)]

    while to_visit:
        cp, cd = to_visit.pop(0)

        if cp in seen:
            continue

        if cp == end:
            return True

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            np = (cp[0] + dx, cp[1] + dy)
            if 0 <= np[0] < grid_size and 0 <= np[1] < grid_size and np not in seen and np not in pts:
                to_visit.append((np, cd + 1))

        seen.add(cp)

    return False


@profiler
def part_1():
    with open("input.txt", "r") as f: 
        pts = [tuple(map(int, l.strip().split(","))) for l in f]
    if maze(pts[:1024]):
        print("Path to exit exists after 1024 bytes")
    else:
        print("Path to exit is blocked after 1024 bytes")


@profiler
def part_2():
    with open("input.txt", "r") as f:
        pts = [tuple(map(int, l.strip().split(","))) for l in f]

    left = 0
    right = len(pts) - 1

    while left < right:
        mid = (left + right) // 2
        if maze(pts[:mid + 1]):
            left = mid + 1
        else:
            right = mid

    print(f"Blocking byte coordinates: {pts[left][0]},{pts[left][1]}")


if __name__ == "__main__":
    part_1()
    part_2()
