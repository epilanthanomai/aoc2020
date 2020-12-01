#!/usr/bin/env python3

import os
import sys

ROOT = os.path.dirname(__file__)


def main():
    expenses = load_expenses()
    value_1, value_2 = find_pair_with_sum(expenses, 2020)
    if value_1 is None:
        sys.exit("No match.")
    print(value_1 * value_2)


def load_expenses():
    with open_data("day01-expenses.txt") as expenses_file:
        return {int(line) for line in expenses_file}


def open_data(filename):
    path = os.path.join(ROOT, "data", filename)
    return open(path)


def find_pair_with_sum(values, target):
    for value in values:
        if target - value in values:
            return value, target - value
    return None, None


if __name__ == "__main__":
    main()
