from itertools import combinations
from collections import defaultdict

FILENAME = "day8.txt"
EMPTY = "."


def parse_input(filename):
    with open(filename, "r") as input_file:
        return input_file.read().split("\n")


def parse_scan(scan):
    antennas = defaultdict(list)
    entire_map = {
        complex(i, j) for i, row in enumerate(scan) for j, char in enumerate(row)
    }
    for i, row in enumerate(scan):
        for j, char in enumerate(row):
            if char != EMPTY:
                antennas[char].append(complex(i, j))
    return entire_map, antennas


def get_antipodes_for_pair(first_antenna, second_antenna):
    delta = first_antenna - second_antenna
    return {
        first_antenna - delta,
        first_antenna + delta,
        second_antenna - delta,
        second_antenna + delta,
    } - {first_antenna, second_antenna}


def get_all_antenna_pairs(antennas):
    return [
        pair
        for coordinates in antennas.values()
        for pair in combinations(coordinates, 2)
    ]


def part_one(scan):
    entire_map, antennas = parse_scan(scan)
    antenna_pairs = get_all_antenna_pairs(antennas)
    antipodes = {
        antipode
        for first_antenna, second_antenna in antenna_pairs
        for antipode in get_antipodes_for_pair(first_antenna, second_antenna)
    }
    return antipodes & entire_map


def is_aligned(coordinate, first_antenna, second_antenna):
    delta = second_antenna - first_antenna
    vector = coordinate - first_antenna
    return delta != 0 and (vector / delta).imag == 0


def part_two(scan):
    entire_map, antennas = parse_scan(scan)
    antenna_pairs = get_all_antenna_pairs(antennas)
    return sum(
        any(is_aligned(coordinate, a1, a2) for a1, a2 in antenna_pairs)
        for coordinate in entire_map
    )


def main():
    scan = parse_input(FILENAME)
    print(len(part_one(scan)))
    print(part_two(scan))


if __name__ == "__main__":
    main()
