#!/usr/bin/env python3

import sys
from collections import defaultdict
from functools import partial


def main(dimensions):
    state = load_state("data/day17-3dlife.txt", dimensions)
    state = repeat(6, partial(step_state, dimensions=dimensions), state)
    print(len(state))


def load_state(file_name, dimensions):
    with open(file_name) as state_file:
        plane = parse_state_plane(state_file)
    return set(tuple([row, column] + [0] * (dimensions - 2)) for (row, column) in plane)


def parse_state_plane(lines):
    return set(
        (row, column)
        for (row, line) in enumerate(lines)
        for (column, point) in enumerate(line.strip())
        if point == "#"
    )


def repeat(n, f, state):
    for _ in range(n):
        state = f(state)
    return state


def step_state(state, dimensions):
    neighbor_counts = count_neighbors(state)
    return calculate_new_state(state, neighbor_counts)


def count_neighbors(state):
    neighbor_counts = defaultdict(int)
    for point in state:
        for neighbor in get_neighbors(point):
            neighbor_counts[neighbor] += 1
    return neighbor_counts


def get_region(position):
    if len(position) == 0:
        return [[]]
    else:
        x, rest = position[0], position[1:]
        lower_dimension = get_region(rest)
        return [[d] + ld for d in (x - 1, x, x + 1) for ld in lower_dimension]


def get_neighbors(position):
    tuples = [tuple(p) for p in get_region(position)]
    return [p for p in tuples if p != position]


ACTIVE = set(
    (
        (True, 2),
        (True, 3),
        (False, 3),
    )
)


def calculate_new_state(state, neighbor_counts):
    return set(
        point
        for (point, neighbors) in neighbor_counts.items()
        if (point in state, neighbors) in ACTIVE
    )


if __name__ == "__main__":
    main(int(sys.argv[1]))
