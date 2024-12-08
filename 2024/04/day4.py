import numpy as np

ALL_DIRECTIONS = [(0, 1), (1, 1), (1, 0), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
DIAGONALS = [[(-1, -1), (0, 0), (1, 1)], [(-1, 1), (0, 0), (1, -1)]]


def parse_input(input: str) -> np.ndarray:
    return np.array([list(line) for line in input.splitlines()])


def letter_positions(grid: np.ndarray, letter: str) -> list[tuple[int, int]]:
    return list(zip(*np.where(grid == letter)))


def is_in_grid(grid: np.ndarray, coordinates: tuple[int, int]) -> bool:
    return all(0 <= coordinates[axis] < grid.shape[axis] for axis in (0, 1))


def count_xmas_spelled(grid: np.ndarray, coordinates: tuple[int, int]) -> int:
    return sum(spells_xmas(grid, coordinates, direction) for direction in ALL_DIRECTIONS)


def spells_xmas(grid: np.ndarray, coordinates: tuple[int, int], direction: tuple[int, int]) -> bool:
    target = "XMAS"
    for char in target:
        if not is_in_grid(grid, coordinates) or grid[coordinates] != char:
            return False
        coordinates = tuple(map(sum, zip(coordinates, direction)))
    return True


def is_x_shaped_mas(grid: np.ndarray, coordinates: tuple[int, int]) -> bool:
    target = "MAS"
    for diagonal in DIAGONALS:
        diagonal_coords = [(coordinates[0] + d[0], coordinates[1] + d[1]) for d in diagonal]
        if not all(is_in_grid(grid, c) for c in diagonal_coords):
            return False
        if "".join(grid[c] for c in diagonal_coords) not in [target, target[::-1]]:
            return False
    return True


def part1(grid: np.ndarray) -> int:
    return sum(count_xmas_spelled(grid, pos) for pos in letter_positions(grid, "X"))


def part2(grid: np.ndarray) -> int:
    return sum(1 for pos in letter_positions(grid, "A") if is_x_shaped_mas(grid, pos))


def solve(puzzle_input: str) -> tuple[int, int]:
    grid = parse_input(puzzle_input)
    return part1(grid), part2(grid)


# Usage example (with your input file "day4.txt"):
if __name__ == "__main__":
    with open("day4.txt", "r") as f:
        puzzle_input = f.read()

    part_one, part_two = solve(puzzle_input)
    print(f"Part one: {part_one}")
    print(f"Part two: {part_two}")
