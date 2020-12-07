#!/usr/bin/env python3

import files


def main():
    with files.open_data("day06-answergroups.txt") as answer_file:
        answer_groups = list(parse_answer_groups(answer_file))
    group_answers = [get_group_answers(group) for group in answer_groups]
    print(sum(len(group) for group in group_answers))


def parse_answer_groups(lines):
    group = []
    for line in lines:
        line = line.strip()
        if line:
            group.append(line)
        else:
            yield group
            group = []
    if group:
        yield group


def get_group_answers(group):
    return set("".join(group))


if __name__ == "__main__":
    main()
