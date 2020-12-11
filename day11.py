#!/usr/bin/env python3

import sys
from functools import partial


def main(neighbor_strategy, neighbor_tolerance):
    with open("data/day11-ferryseats.txt") as seat_file:
        seats = list(line.strip() for line in seat_file)
    neighbors = calculate_neighbors(seats, neighbor_strategy)
    step = partial(step_seats, neighbors, neighbor_tolerance)
    stable = stabilize(step, seats)
    occupied = "".join(stable).count("#")
    print(occupied)


def calculate_neighbors(seats, strategy):
    return [
        [strategy(seats, i, j) for j in range(len(seats[i]))] for i in range(len(seats))
    ]


DIRECTIONS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def adjacent_seats(seats, i, j):
    return [
        (i + ni, j + nj)
        for (ni, nj) in DIRECTIONS
        if 0 <= i + ni < len(seats) and 0 <= j + nj < len(seats[i])
    ]


def visible_seats(seats, i, j):
    raw_result = [
        visible_seat_in_direction(seats, i, j, ni, nj) for (ni, nj) in DIRECTIONS
    ]
    return [seat for seat in raw_result if seat is not None]


def visible_seat_in_direction(seats, i, j, si, sj):
    ni, nj = si, sj
    while 0 <= i + ni < len(seats) and 0 <= j + nj < len(seats[i]):
        if seats[i + ni][j + nj] != ".":
            return i + ni, j + nj
        ni, nj = ni + si, nj + sj


def stabilize(f, start):
    last = start
    for seats in iteratively_apply(f, start):
        if seats == last:
            return seats
        last = seats


def iteratively_apply(f, state):
    while True:
        state = f(state)
        yield state


def step_seats(neighbors, neighbor_tolerance, state):
    return [
        "".join(
            next_for_seat(
                neighbor_tolerance, seat, get_neighbor_state(neighbors, state, i, j)
            )
            for (j, seat) in enumerate(row)
        )
        for (i, row) in enumerate(state)
    ]


def next_for_seat(neighbor_tolerance, seat, neighbors):
    if seat == "L":
        return "#" if neighbors.count("#") == 0 else "L"
    elif seat == "#":
        return "L" if neighbors.count("#") >= neighbor_tolerance else "#"
    elif seat == ".":
        return "."


def get_neighbor_state(neighbors, state, i, j):
    return "".join(state[ni][nj] for (ni, nj) in neighbors[i][j])


if __name__ == "__main__":
    neighbor_strategy, neighbor_tolerance = {
        "near": (adjacent_seats, 4),
        "far": (visible_seats, 5),
    }[sys.argv[1]]
    main(neighbor_strategy, neighbor_tolerance)
