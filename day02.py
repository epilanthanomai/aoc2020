#!/usr/bin/env python3

import collections
import re
import sys


PASSWORD_LINE_RE = re.compile(
    r"(?P<first_number>\d+)-(?P<second_number>\d+)\s+(?P<char>\S):\s+(?P<password>.*)"
)

PasswordLine1 = collections.namedtuple(
    "PasswordLine1", ["low_bound", "high_bound", "char", "password"]
)
PasswordLine2 = collections.namedtuple(
    "PasswordLine2", ["first_index", "second_index", "char", "password"]
)


def main(parse_password_line, check_password_line):
    with open("data/day02-passwords.txt") as password_file:
        lines_valid = check_all_passwords(
            password_file, parse_password_line, check_password_line
        )
        valid_count = len([valid for valid in lines_valid if valid])
    print(valid_count)


def check_all_passwords(password_file, parse_password_line, check_password_line):
    for line in password_file:
        password_line = parse_password_line(line)
        yield check_password_line(password_line)


def parse_password_line_1(line):
    match = PASSWORD_LINE_RE.match(line)
    return PasswordLine1(
        int(match.group("first_number")),
        int(match.group("second_number")),
        match.group("char"),
        match.group("password"),
    )


def parse_password_line_2(line):
    match = PASSWORD_LINE_RE.match(line)
    return PasswordLine2(
        int(match.group("first_number")),
        int(match.group("second_number")),
        match.group("char"),
        match.group("password"),
    )


def check_password_line_1(parsed_line):
    count = len([c for c in parsed_line.password if c == parsed_line.char])
    return count >= parsed_line.low_bound and count <= parsed_line.high_bound


def check_password_line_2(parsed_line):
    first_char = parsed_line.password[parsed_line.first_index - 1]
    second_char = parsed_line.password[parsed_line.second_index - 1]
    chars = [first_char, second_char]
    count = len([c for c in chars if c == parsed_line.char])
    return count == 1


if __name__ == "__main__":
    password_schemes = {
        "1": (parse_password_line_1, check_password_line_1),
        "2": (parse_password_line_2, check_password_line_2),
    }
    scheme_string = sys.argv[1]
    parse_password_line, check_password_line = password_schemes[scheme_string]
    main(parse_password_line, check_password_line)
