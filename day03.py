#!/usr/bin/env python3

import files


def main():
    terrain = load_terrain()
    trees = count_trees_in_path(terrain, 3, 1)
    print(trees)


def load_terrain():
    with files.open_data("day03-trees.txt") as terrain_file:
        return [line.strip() for line in terrain_file]


def count_trees_in_path(terrain, right, down):
    path = "".join(follow_path(terrain, right, down))
    return path.count("#")


def follow_path(terrain, right, down):
    line = 0
    column = 0
    height = len(terrain)
    width = len(terrain[0])

    while line < height:
        yield terrain[line][column]
        line += down
        column = (column + right) % width


if __name__ == "__main__":
    main()
