#!/usr/bin/env python3

import sys
import re

import files


def main(validate_values):
    validate = all_values_valid if validate_values else required_fields_present
    with files.open_data("day04-passports.txt") as passport_file:
        valid = len(
            [
                chunk
                for chunk in parse_chunks(passport_file)
                if validate(chunk, validate_values)
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


def required_fields_present(fields, validate_values):
    field_names = {k for (k, v) in fields}
    return field_names.issuperset(REQUIRED_FIELDS)


def all_values_valid(fields, validate_values):
    for field_name in REQUIRED_FIELDS:
        values = [v for (k, v) in fields if k == field_name]
        if len(values) != 1:
            return False
        if not value_valid(field_name, values[0]):
            return False
    return True


def value_valid(field_name, value):
    validate = VALIDATORS[field_name]
    try:
        return validate(value)
    except:
        return False


HGT_RE = re.compile(r"^(?P<count>\d+)(?P<unit>cm|in)$")
HCL_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
PID_RE = re.compile(r"^[0-9]{9}$")
ECL_VALUES = set("amb blu brn gry grn hzl oth".split())


def validate_byr(value):
    i = int(value)
    return 1920 <= i <= 2002


def validate_iyr(value):
    i = int(value)
    return 2010 <= i <= 2020


def validate_eyr(value):
    i = int(value)
    return 2020 <= i <= 2030


def validate_hgt(value):
    match = HGT_RE.match(value)
    count = int(match.group("count"))
    unit = match.group("unit")
    if unit == "cm":
        return 150 <= count <= 193
    else:
        return 59 <= count <= 76


def validate_hcl(value):
    return HCL_RE.match(value)


def validate_ecl(value):
    return value in ECL_VALUES


def validate_pid(value):
    return PID_RE.match(value)


VALIDATORS = {
    "byr": validate_byr,
    "iyr": validate_iyr,
    "eyr": validate_eyr,
    "hgt": validate_hgt,
    "hcl": validate_hcl,
    "ecl": validate_ecl,
    "pid": validate_pid,
}
REQUIRED_FIELDS = set(VALIDATORS)


if __name__ == "__main__":
    validate_values = bool(int(sys.argv[1])) if len(sys.argv) > 1 else False
    main(validate_values)
