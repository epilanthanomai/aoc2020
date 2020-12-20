#!/usr/bin/env python3

from collections import namedtuple


def main():
    rules, messages = load_rules("data/day19-seamonster.txt")
    matches = [message for message in messages if match_any_rule(message, rules)]
    print(len(matches))


def load_rules(file_name):
    with open(file_name) as input_file:
        input_data = input_file.read()
        rules_text, messages_text = input_data.split("\n\n")

        rule_strings = rules_text.splitlines()
        rules = dict(parse_rule(rule_string) for rule_string in rule_strings)
        messages = messages_text.splitlines()
        return rules, messages


def parse_rule(rule_string):
    rule_number_string, raw_patterns = rule_string.split(":")
    rule_number = int(rule_number_string)

    raw_patterns = raw_patterns.strip()
    if raw_patterns[0] == '"' and raw_patterns[-1] == '"':
        match = raw_patterns[1:-1]
    else:
        split_patterns = raw_patterns.split("|")
        match = [
            [int(target) for target in pattern.strip().split()]
            for pattern in split_patterns
        ]
    return rule_number, match


Candidate = namedtuple("Candidate", ["pattern", "string_position"])


def match_any_rule(message, rules):
    candidates = [Candidate(pattern, 0) for pattern in rules[0]]
    while candidates:
        (current_pattern, position), candidates = candidates[0], candidates[1:]
        remaining_message = message[position:]
        if current_pattern == []:
            if remaining_message == "":
                return True
            else:
                continue
        rule_reference, rest = current_pattern[0], current_pattern[1:]
        rule = rules[rule_reference]
        if isinstance(rule, str):
            if remaining_message.startswith(rule):
                candidates.append(Candidate(rest, position + len(rule)))
        else:
            candidates.extend([Candidate(pattern + rest, position) for pattern in rule])
    return False


if __name__ == "__main__":
    main()
