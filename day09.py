#!/usr/bin/env python3

import collections
import itertools
import operator
import sys


def main(find_range):
    with open("data/day09-windowsums.txt") as input_file:
        numbers = [int(line) for line in input_file]
    target_number = first_not_in_windowed_sums(numbers, 25)
    if find_range:
        match_range = find_range_with_sum(numbers, target_number)
        print(min(match_range) + max(match_range))
    else:
        print(target_number)


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


def find_range_with_sum(numbers, target):
    start = 0
    end = 0
    total = 0

    while True:
        if total < target:
            if end == len(numbers):
                return
            total += numbers[end]
            end += 1
        else:
            total -= numbers[start]
            start += 1
        if total == target:
            return numbers[start:end]


if __name__ == "__main__":
    find_range = bool(int(sys.argv[1]))
    main(find_range)
