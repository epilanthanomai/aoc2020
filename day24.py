#!/usr/bin/env python3

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


def main():
    tile_paths = load_tiles("data/day24-tiles.txt")
    tiles = defaultdict(bool)
    flip_tiles(tiles, tile_paths)
    print(len([t for (t, flipped) in tiles.items() if flipped]))


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
    )
    tiles[target_position.freeze()] = not tiles[target_position.freeze()]


if __name__ == "__main__":
    main()
