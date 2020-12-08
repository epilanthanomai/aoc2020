#!/usr/bin/env python3

import functools
import operator
import os
import sys


def main(count):
    expenses = load_expenses()
    values = find_numbers_with_sum(expenses, 2020, count)
    if values[0] is None:
        sys.exit("No match.")
    product = functools.reduce(operator.mul, values)
    print(product)


def load_expenses():
    with open("data/day01-expenses.txt") as expenses_file:
        return {int(line) for line in expenses_file}


def find_numbers_with_sum(values, target, count):
    if count == 1:
        if target in values:
            return [target]
        else:
            return [None]
    else:
        for value in values:
            rest = values.difference({value})
            result = find_numbers_with_sum(rest, target - value, count - 1)
            if result[0] is not None:
                return [value] + result

        return [None] + result


if __name__ == "__main__":
    count = int(sys.argv[1])
    main(count)
