#!/usr/bin/env python3


def main():
    with open("data/day11-ferryseats.txt") as seat_file:
        seats = list(line.strip() for line in seat_file)
    stable = stabilize(step_seats, seats)
    occupied = "".join(stable).count("#")
    print(occupied)


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


def step_seats(state):
    return [
        "".join(
            next_for_seat(seat, get_neighbors(state, i, j))
            for (j, seat) in enumerate(row)
        )
        for (i, row) in enumerate(state)
    ]


def next_for_seat(seat, neighbors):
    if seat == "L":
        return "#" if neighbors.count("#") == 0 else "L"
    elif seat == "#":
        return "L" if neighbors.count("#") >= 4 else "#"
    elif seat == ".":
        return "."


NEIGHBOR_CANDIDATES = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def get_neighbors(state, i, j):
    return "".join(
        state[i + ni][j + nj]
        for (ni, nj) in NEIGHBOR_CANDIDATES
        if 0 <= i + ni < len(state) and 0 <= j + nj < len(state[i + ni])
    )


if __name__ == "__main__":
    main()
