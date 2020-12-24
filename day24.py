#!/usr/bin/env python3

import sys
from collections import defaultdict
from dataclasses import dataclass


#           col      col
#             \        \
# row -      (-1, 0) - (-1, +1)
#                  \         \
# row -   (0, -1) - (0, 0) - (0, +1)
#              \         \
# row -      (+1, -1) - (+1, 0)

DIRECTIONS = {
    "nw": (-1, 0),
    "ne": (-1, +1),
    "w": (0, -1),
    "e": (0, +1),
    "sw": (+1, -1),
    "se": (+1, 0),
}


def main(iterations):
    tile_paths = load_tiles("data/day24-tiles.txt")
    tiles = set()
    flip_tiles(tiles, tile_paths)
    tiles = run_updates(tiles, iterations)
    print(len(tiles))


def load_tiles(file_name):
    with open(file_name) as tiles_file:
        return [list(generate_parsed_tile_path(line.strip())) for line in tiles_file]


def generate_parsed_tile_path(path):
    start = 0
    for (i, c) in enumerate(path, 1):
        if c in "ew":
            yield path[start:i]
            start = i


@dataclass
class CartesianPosition:
    # seems like there should be a standard library type that does this better
    row: int
    column: int

    def __add__(self, other):
        return type(self)(self.row + other.row, self.column + other.column)

    def freeze(self):
        return (self.row, self.column)


def flip_tiles(tiles, paths):
    for path in paths:
        flip_tile(tiles, path)


def flip_tile(tiles, path):
    target_position = sum(
        (CartesianPosition(*DIRECTIONS[move]) for move in path), CartesianPosition(0, 0)
    ).freeze()
    if target_position in tiles:
        tiles.remove(target_position)
    else:
        tiles.add(target_position)


def run_updates(tiles, iterations):
    for _ in range(iterations):
        tiles = update_once(tiles)
    return tiles


UPDATE_BLACK = {
    (True, 1),
    (True, 2),
    (False, 2),
}


def update_once(tiles):
    neighbors = defaultdict(int)
    for (row, column) in tiles:
        for (d_row, d_column) in DIRECTIONS.values():
            neighbors[row + d_row, column + d_column] += 1
    return set(t for (t, n) in neighbors.items() if (t in tiles, n) in UPDATE_BLACK)


if __name__ == "__main__":
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    main(iterations)
