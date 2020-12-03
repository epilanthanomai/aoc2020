#!/usr/bin/env python3

import files
import functools
import operator
import sys


def main(paths):
    terrain = load_terrain()
    tree_counts = [count_trees_in_path(terrain, *path) for path in paths]
    product = functools.reduce(operator.mul, tree_counts)
    print(product)


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
    problem_paths = {
        "1": [(3, 1)],
        "2": [
            (1, 1),
            (3, 1),
            (5, 1),
            (7, 1),
            (1, 2),
        ],
    }
    problem = sys.argv[1]
    paths = problem_paths[problem]
    main(paths)
