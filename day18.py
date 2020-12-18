#!/usr/bin/env python3

import operator
import re
import sys
from collections import namedtuple
from enum import Enum


def main(use_precedence):
    expressions = load_expressions("data/day18-math.txt", use_precedence)
    print(sum(evaluate(e) for e in expressions))


def load_expressions(file_name, use_precedence):
    with open(file_name) as expressions_file:
        return [parse_expression(e, use_precedence) for e in expressions_file]


# Flagrantly resisting the urge to use a Real Parsing library, but totally half-assing it


def parse_expression(expression, use_precedence):
    tokens = tokenize(expression)
    return parse_tokens(tokens, use_precedence)


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


# error checking lol
def parse_tokens(tokens, use_precedence):
    stack = [[None, None]]

    def push_expression(e):
        left, f = stack[-1]
        if f is None:
            stack[-1][0] = e
        # oh god im so sorry
        elif (
            use_precedence
            and f == operator.add
            and isinstance(left, list)
            and left[0] == "Operator"
            and left[2] == operator.mul
        ):
            op = left
            while (
                isinstance(op[3], list)
                and op[3][0] == "Operator"
                and op[3][2] == operator.mul
            ):
                op = op[3]
            new_right = ["Operator", op[3], f, e]
            op[3] = new_right
        else:
            stack[-1] = [["Operator", left, f, e], None]

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
        term, __ = stack.pop()
        push_expression(["Parentheses", term])

    for token, text in tokens:
        parse = locals()["parse_" + token.name]
        parse(text)

    return stack[-1][0]


def evaluate(expression):
    if isinstance(expression, list):
        if expression[0] == "Operator":
            _, left_expression, f, right_expression = expression
            left = evaluate(left_expression)
            right = evaluate(right_expression)
            return f(left, right)
        elif expression[0] == "Parentheses":
            return evaluate(expression[1])
    else:
        return expression


if __name__ == "__main__":
    use_precedence = bool(int(sys.argv[1]))
    main(use_precedence)
