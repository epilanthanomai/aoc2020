#!/usr/bin/env python3

import collections
import re

from files import open_data

PASSWORD_LINE_RE = re.compile(
    r"(?P<low_bound>\d+)-(?P<high_bound>\d+)\s+(?P<char>\S):\s+(?P<password>.*)"
)

PasswordLine = collections.namedtuple(
    "PasswordLine", ["low_bound", "high_bound", "char", "password"]
)


def main():
    with open_data("day02-passwords.txt") as password_file:
        lines_valid = check_all_passwords(password_file)
        valid_count = len([valid for valid in lines_valid if valid])
    print(valid_count)


def check_all_passwords(password_file):
    for line in password_file:
        password_line = parse_password_line(line)
        yield check_password_line(password_line)


def parse_password_line(line):
    match = PASSWORD_LINE_RE.match(line)
    return PasswordLine(
        int(match.group("low_bound")),
        int(match.group("high_bound")),
        match.group("char"),
        match.group("password"),
    )


def check_password_line(parsed_line):
    count = len([c for c in parsed_line.password if c == parsed_line.char])
    return count >= parsed_line.low_bound and count <= parsed_line.high_bound


if __name__ == "__main__":
    main()
