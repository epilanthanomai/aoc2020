#!/usr/bin/env python3

import operator
import re
import sys
from functools import reduce


def main(problem):
    field_ranges, my_numbers, other_numbers = parse_input_file("data/day16-tickets.txt")
    field_masks = calculate_range_masks(field_ranges)
    all_valid_ranges = reduce(
        operator.or_,
        [mask for (field_name, mask) in field_masks],
    )
    print(problem(field_masks, all_valid_ranges, my_numbers, other_numbers))


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


def sum_invalid_numbers(field_masks, all_valid_ranges, my_numbers, other_numbers):
    return sum(invalid_numbers(all_valid_ranges, other_numbers))


def bit_in_mask(mask, number):
    return 2 ** number & mask


def invalid_numbers(all_valid_ranges, number_lists):
    return (
        number
        for row in number_lists
        for number in row
        if not bit_in_mask(all_valid_ranges, number)
    )


def field_is_collected(field_name):
    return field_name.startswith("departure")


def identify_and_multiply_fields(
    field_masks, all_valid_ranges, my_numbers, other_numbers
):
    # remove any ticket with invalid numbers
    other_numbers = filter(
        lambda number_list: all(
            bit_in_mask(all_valid_ranges, number) for number in number_list
        ),
        other_numbers,
    )

    # calculate a bitmask of valid fields for each number in each ticket
    my_valid_fields = calculate_valid_fields(field_masks, my_numbers)
    other_valid_fields = [
        calculate_valid_fields(field_masks, number_list)
        for number_list in other_numbers
    ]
    # match up tickets with fields
    field_matches = identify_fields(other_valid_fields + [my_valid_fields])
    # return the problem goal: the product of selected fields
    return reduce(
        operator.mul,
        (
            my_numbers[ticket_column_number]
            for (ticket_column_number, field_number) in field_matches
            if field_is_collected(field_masks[field_number][0])
        ),
        1,
    )


def calculate_valid_fields(field_masks, number_list):
    # calculate the mask of valid fields for each number in a ticket
    return [
        reduce(
            operator.or_,
            (
                (2 ** i)
                for (i, (field_name, field_mask)) in enumerate(field_masks)
                if bit_in_mask(field_mask, number)
            ),
        )
        for number in number_list
    ]


def identify_fields(ticket_validity_masks):
    # match up tickets with fields

    column_count = len(ticket_validity_masks[0])

    # collect the valid fields for each column across all tickets, and & them to figure out what fields are valid for
    # the entire column
    column_validity_masks = [
        reduce(
            operator.and_,
            (ticket[column] for ticket in ticket_validity_masks),
        )
        for column in range(column_count)
    ]

    # masks for the next calculation
    all_fields = reduce(operator.or_, (2 ** i for i in range(column_count)))
    unidentified_fields = all_fields

    # check how many fields are valid for each column. hopefully on each pass there will be at least one column that has
    # exactly one valid field. yield that as a match, and remove it from the unmatched ones. repeat until we have them
    # all.
    while unidentified_fields:
        # check each column for how many fields it could be
        for column in range(column_count):
            # calculate the fields this column could match among unmatched ones
            available_mask = column_validity_masks[column] & unidentified_fields
            available_fields = [
                i for i in range(column_count) if bit_in_mask(available_mask, i)
            ]
            available_field_count = len(available_fields)
            if available_field_count == 1:
                # there's only one field valid for this column. it's a match
                match_field = available_fields[0]
                break
        else:
            raise RuntimeError("no field matches")

        # we found a match (column, match_field). remove it from remaining checks
        field_remove_mask = all_fields ^ 2 ** match_field
        unidentified_fields &= field_remove_mask
        yield column, match_field


if __name__ == "__main__":
    problem = {
        "numbers": sum_invalid_numbers,
        "departures": identify_and_multiply_fields,
    }[sys.argv[1]]
    main(problem)
