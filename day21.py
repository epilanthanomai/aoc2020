#!/usr/bin/env python3

import re
import sys
from copy import deepcopy

CONTENTS_RE = re.compile(r"([a-z ]+) \(contains ([a-z, ]+)\)")


def main(problem):
    contents = load_contents("data/day21-allergens.txt")
    allergen_map = identify_allergens(contents)
    print(problem(contents, allergen_map))


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


def get_dangerous_list(contents, allergen_map):
    unidentified_allergens = deepcopy(allergen_map)
    identified_allergens = {}

    while unidentified_allergens:
        singleton_allergens = {
            allergen: list(ingredients)[0]
            for (allergen, ingredients) in unidentified_allergens.items()
            if len(ingredients) == 1
        }
        assert len(singleton_allergens) > 0
        identified_allergens.update(singleton_allergens)
        for allergen in singleton_allergens.keys():
            del unidentified_allergens[allergen]
        identified_ingredients = set(singleton_allergens.values())
        for allergen in unidentified_allergens:
            unidentified_allergens[allergen] = unidentified_allergens[
                allergen
            ].difference(identified_ingredients)
        assert not any(
            len(ingredients) == 0 for ingredients in unidentified_allergens.values()
        )

    allergens_list = list(identified_allergens.items())
    dangerous_ingredients = [
        ingredient for (allergen, ingredient) in sorted(allergens_list)
    ]
    return ",".join(dangerous_ingredients)


if __name__ == "__main__":
    problem = {
        "safe": count_safe_ingredients,
        "dangerous": get_dangerous_list,
    }[sys.argv[1]]
    main(problem)
