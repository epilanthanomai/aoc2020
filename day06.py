#!/usr/bin/env python3

import sys
import files


def main(combine):
    with files.open_data("day06-answergroups.txt") as answer_file:
        answer_groups = list(parse_answer_groups(answer_file))
    group_answers = [get_group_answers(group, combine) for group in answer_groups]
    print(sum(len(group) for group in group_answers))


def parse_answer_groups(lines):
    group = []
    for line in lines:
        line = line.strip()
        if line:
            group.append(set(line))
        else:
            yield group
            group = []
    if group:
        yield group


def get_group_answers(group, combine):
    return combine(*group)


if __name__ == "__main__":
    combine = {
        "any": set.union,
        "all": set.intersection,
    }[sys.argv[1]]
    main(combine)
