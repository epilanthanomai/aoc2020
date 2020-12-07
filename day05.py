#!/usr/bin/env python3

import files


def main():
    with files.open_data("day05-boardingpasses.txt") as passes_file:
        passes = [parse_pass_seat(line.strip()) for line in passes_file]
    seat_ids = [seat_id(row, column) for (row, column) in passes]
    print(max(seat_ids))


ROW_PATH_TO_BIT = {
    "F": "0",
    "B": "1",
    "L": "0",
    "R": "1",
}


def parse_pass_seat(path):
    row_path, column_path = path[:7], path[7:]
    return path_to_number(row_path), path_to_number(column_path)


def path_to_number(path):
    bits = "".join(ROW_PATH_TO_BIT[c] for c in path)
    return int(bits, 2)


def seat_id(row, column):
    return row * 8 + column


if __name__ == "__main__":
    main()
