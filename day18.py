#!/usr/bin/env python3

import operator
import re
from collections import namedtuple
from enum import Enum


def main():
    expressions = load_expressions("data/day18-math.txt")
    print(sum(evaluate(e) for e in expressions))


def load_expressions(file_name):
    with open(file_name) as expressions_file:
        return [parse_expression(e) for e in expressions_file]


# Flagrantly resisting the urge to use a Real Parsing library, but totally half-assing it


def parse_expression(expression):
    tokens = tokenize(expression)
    return parse_tokens(tokens)


class Token(Enum):
    space = r"\s+"
    number = r"\d+"
    operator = r"[*+]"
    left = r"\("
    right = r"\)"


def tokenize(expression):
    all_token_re = re.compile(
        "(?:" + "|".join((f"(?P<{t.name}>{t.value})") for t in Token) + ")"
    )
    pos = 0
    while pos < len(expression):
        match = all_token_re.match(expression, pos)
        groups = match.groupdict().items()
        name, text = [(n, t) for (n, t) in groups if t is not None][0]
        pos = match.end()
        yield (Token[name], text)


Operator = namedtuple("Operator", ["left", "f", "right"])

# error checking lol
def parse_tokens(tokens):
    stack = [[None, None]]

    def push_expression(e):
        left, f = stack[-1]
        if f is None:
            stack[-1][0] = e
        else:
            stack[-1] = [Operator(left, f, e), None]

    def parse_space(text):
        pass

    def parse_number(text):
        push_expression(int(text))

    def parse_operator(text):
        f = {
            "*": operator.mul,
            "+": operator.add,
        }[text]
        stack[-1][1] = f

    def parse_left(text):
        stack.append([None, None])

    def parse_right(text):
        term, _ = stack.pop()
        push_expression(term)

    for token, text in tokens:
        parse = locals()["parse_" + token.name]
        parse(text)

    return stack[-1][0]


def evaluate(expression):
    if isinstance(expression, Operator):
        left = evaluate(expression.left)
        right = evaluate(expression.right)
        return expression.f(left, right)
    else:
        return expression


if __name__ == "__main__":
    main()
