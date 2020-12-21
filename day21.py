#!/usr/bin/env python3

import re

CONTENTS_RE = re.compile(r"([a-z ]+) \(contains ([a-z, ]+)\)")


def main():
    contents = load_contents("data/day21-allergens.txt")
    allergen_map = identify_allergens(contents)
    print(count_safe_ingredients(contents, allergen_map))


def load_contents(file_name):
    with open(file_name) as contents_file:
        return [parse_contents(line.strip()) for line in contents_file]


def parse_contents(line):
    match = CONTENTS_RE.match(line)
    raw_ingredients, raw_allergens = match.groups()
    return set(raw_ingredients.split()), set(raw_allergens.split(", "))


def identify_allergens(contents):
    all_allergens = set.union(*[allergens for (ingredients, allergens) in contents])
    return {
        allergen: set.intersection(
            *[
                ingredients
                for (ingredients, allergens) in contents
                if allergen in allergens
            ]
        )
        for allergen in all_allergens
    }


def count_safe_ingredients(contents, allergen_map):
    possible_allergens = set.union(*list(allergen_map.values()))
    return sum(
        len(ingredients.difference(possible_allergens)) for (ingredients, _) in contents
    )


if __name__ == "__main__":
    main()
