#!/usr/bin/env python3

import files

REQUIRED_FIELDS = set("byr iyr eyr hgt hcl ecl pid".split())


def main():
    with files.open_data("day04-passports.txt") as passport_file:
        valid = len(
            [
                chunk
                for chunk in parse_chunks(passport_file)
                if valid_passport_fields(chunk)
            ]
        )
        print(valid)


def parse_chunks(lines):
    fields = []
    for line in lines:
        raw_fields = line.split()
        if raw_fields:
            new_fields = [field.split(":", 1) for field in raw_fields]
            fields += new_fields
        else:
            if fields:
                yield fields
                fields = []
    if fields:
        yield fields


def valid_passport_fields(fields):
    field_names = {k for (k, v) in fields}
    return field_names.issuperset(REQUIRED_FIELDS)


if __name__ == "__main__":
    main()
