#!/usr/bin/env python3

PUZZLE_INPUT = [int(c) for c in "315679824"]
ITERATIONS = 100


def main(cups):
    finished = play_cup_game(cups, ITERATIONS)
    print(cups_after_one(finished))


def play_cup_game(cups, iterations):
    for i in range(iterations):
        cups = cup_game_round(cups)
    return cups


def cup_game_round(cups):
    current_value = cups[0]

    removed_cups = cups[1:4]
    cups = cups[:1] + cups[4:]

    destination_candidates = [c for c in cups if c < current_value] or cups
    destination_value, destination_location = max(
        (c, i) for (i, c) in enumerate(cups) if c in destination_candidates
    )
    cups = (
        cups[: destination_location + 1]
        + removed_cups
        + cups[destination_location + 1 :]
    )

    cups = cups[1:] + cups[:1]
    return cups


def cups_after_one(cups):
    one = cups.index(1)
    selected = cups[one + 1 :] + cups[:one]
    return "".join(str(i) for i in selected)


if __name__ == "__main__":
    main(PUZZLE_INPUT)
