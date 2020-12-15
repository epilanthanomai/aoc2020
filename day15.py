#!/usr/bin/env python3

from itertools import islice

STARTING_SEQUENCE = [9, 3, 1, 0, 8, 4]
YEAR = 2020


def main():
    sequence = age_or_zero(STARTING_SEQUENCE)
    print(iterindex(sequence, YEAR - 1))


def age_or_zero(starting_sequence):
    # seems like there should be a cleaner way...
    last = None
    step = 0
    seen = {}

    for i in starting_sequence:
        seen[last] = step - 1
        step += 1
        last = i
        yield i

    while True:
        result = 0 if last not in seen else step - seen[last] - 1
        seen[last] = step - 1
        step += 1
        last = result
        yield result


def iterindex(i, n):
    return next(islice(i, n, n + 1))


if __name__ == "__main__":
    main()
