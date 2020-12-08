#!/usr/bin/env python3

import collections
import re
import sys


START_BAG = "shiny gold"


def main(op):
    with open("data/day07-luggagerules.txt") as rules_file:
        rules = [parse_rule(line.strip()) for line in rules_file]
    print(op(rules, START_BAG))


RULE_RE = re.compile(r"(.*?) bags contain (.*?)\.")
CONTAINER_RE = re.compile(r"(\d+) (.*?) bags?")


def parse_rule(line):
    rule_match = RULE_RE.match(line)
    container, full_contents = rule_match.groups()
    if full_contents == "no other bags":
        return container, []
    else:
        split_contents = full_contents.split(", ")
        matched_contents = [CONTAINER_RE.match(c) for c in split_contents]
        return container, [(int(m.group(1)), m.group(2)) for m in matched_contents]


def count_nested_containers(rules, bag):
    containers = invert_rules(rules)
    container_batch = containers[bag]
    result = container_batch
    while container_batch:
        container_step = set.union(*[containers[b] for b in container_batch])
        container_batch = container_step.difference(result)
        result = result.union(container_step)
    return len(result)


def invert_rules(rules):
    result = collections.defaultdict(set)
    for container, contents in rules:
        for _, content in contents:
            result[content].add(container)
    return result


def count_nested_contents(rules, bag):
    content_map = {container: content for container, content in rules}
    return _count_nested_contents(content_map, bag)


def _count_nested_contents(content_map, bag):
    direct_contents = content_map[bag]
    return sum(
        [
            count * (1 + _count_nested_contents(content_map, content))
            for count, content in direct_contents
        ]
    )


if __name__ == "__main__":
    op = {
        "1": count_nested_containers,
        "2": count_nested_contents,
    }[sys.argv[1]]
    main(op)
