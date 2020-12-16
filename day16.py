#!/usr/bin/env python3

import operator
import re
from functools import reduce


def main():
    field_ranges, my_numbers, other_numbers = parse_input_file("data/day16-tickets.txt")
    field_masks = calculate_range_masks(field_ranges)
    print(sum(invalid_numbers(field_masks, other_numbers)))


def parse_input_file(file_name):
    with open(file_name) as input_file:
        return parse_file_data(input_file.read())


def parse_file_data(file_data):
    ranges_s, my_numbers_s, other_numbers_s = file_data.split("\n\n")

    field_ranges = [parse_field_range(line) for line in ranges_s.split("\n")]

    _, _, my_numbers_line = my_numbers_s.partition("\n")
    my_numbers = [int(n) for n in my_numbers_line.split(",")]

    _, _, other_numbers_lines = other_numbers_s.partition("\n")
    other_numbers = [
        [int(n) for n in line.split(",")]
        for line in other_numbers_lines.split("\n")
        if line
    ]

    return field_ranges, my_numbers, other_numbers


FIELD_RANGE_RE = re.compile("(.*): (\d+)-(\d+) or (\d+)-(\d+)")


def parse_field_range(field_line):
    match = FIELD_RANGE_RE.match(field_line)
    field_name, low_1, high_1, low_2, high_2 = match.groups()
    return (field_name, [(int(low_1), int(high_1)), (int(low_2), int(high_2))])


def calculate_range_masks(fields):
    result = []
    for field_name, bounds in fields:
        mask = 0
        for low, high in bounds:
            for i in range(low, high + 1):
                mask |= 2 ** i
        result.append((field_name, mask))
    return result


def invalid_numbers(field_masks, number_lists):
    all_valid_ranges = reduce(
        operator.or_,
        [mask for (field_name, mask) in field_masks],
    )
    return (
        number
        for row in number_lists
        for number in row
        if not 2 ** number & all_valid_ranges
    )


if __name__ == "__main__":
    main()
