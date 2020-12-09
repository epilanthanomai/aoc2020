#!/usr/bin/env python3

import collections
import itertools
import operator


def main():
    with open("data/day09-windowsums.txt") as input_file:
        numbers = (int(line) for line in input_file)
        print(first_not_in_windowed_sums(numbers, 25))


def first_not_in_windowed_sums(iterable, window_size):
    numbers_i, sum_numbers_i = itertools.tee(iter(iterable))
    sums_i = windowed_combinations_with(sum_numbers_i, window_size, operator.add)

    # We need to skip the first window_size numbers. But sum[n-1] is used to check number[n], so we need to capture one
    # fewer of those.
    next(numbers_i)
    i = zip(numbers_i, sums_i)
    for _ in range(window_size - 1):
        next(i)

    for number, sums in i:
        if number not in sums:
            return number


def windowed_combinations_with(iterator, window_size, op):
    d = collections.deque(maxlen=window_size)
    s = collections.defaultdict(int)
    d.append(next(iterator))
    yield s.keys()

    for v in iterator:
        if len(d) == window_size:
            remove = d.popleft()
            for remain in d:
                collect_remove = op(remove, remain)
                if s[collect_remove] == 1:
                    del s[collect_remove]
                else:
                    s[collect_remove] + 1

        for remain in d:
            collect_add = op(remain, v)
            s[collect_add] += 1

        d.append(v)
        yield s.keys()


if __name__ == "__main__":
    main()
