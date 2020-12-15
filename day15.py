#!/usr/bin/env python3

import sys
from itertools import islice

STARTING_SEQUENCE = [9, 3, 1, 0, 8, 4]


def main(index):
    sequence = age_or_zero(STARTING_SEQUENCE)
    print(iterindex(sequence, index))


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
    index = int(sys.argv[1]) - 1  # input index is 1-based
    main(index)
