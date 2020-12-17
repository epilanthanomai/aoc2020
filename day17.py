#!/usr/bin/env python3

from collections import defaultdict


def main():
    state = load_state("data/day17-3dlife.txt")
    state = repeat(6, step_state, state)
    print(len(state))


def load_state(file_name):
    with open(file_name) as state_file:
        return parse_state(state_file)


def parse_state(lines):
    return set(
        (row, column, 0)
        for (row, line) in enumerate(lines)
        for (column, point) in enumerate(line.strip())
        if point == "#"
    )


def repeat(n, f, state):
    for _ in range(n):
        state = f(state)
    return state


NEIGHBORS = set(
    (drow, dcolumn, dheight)
    for drow in range(-1, 2)
    for dcolumn in range(-1, 2)
    for dheight in range(-1, 2)
).difference(set([(0, 0, 0)]))


def step_state(state):
    neighbor_counts = count_neighbors(state)
    return calculate_new_state(state, neighbor_counts)


def count_neighbors(state):
    neighbor_counts = defaultdict(int)
    for row, column, height in state:
        for (drow, dcolumn, dheight) in NEIGHBORS:
            neighbor_counts[row + drow, column + dcolumn, height + dheight] += 1
    return neighbor_counts


ACTIVE = set(
    (
        (True, 2),
        (True, 3),
        (False, 3),
    )
)


def calculate_new_state(state, neighbor_counts):
    return set(
        (row, column, height)
        for ((row, column, height), neighbors) in neighbor_counts.items()
        if ((row, column, height) in state, neighbors) in ACTIVE
    )


if __name__ == "__main__":
    main()
