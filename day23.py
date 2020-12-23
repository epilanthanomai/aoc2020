#!/usr/bin/env python3

import sys
from dataclasses import dataclass

PUZZLE_INPUT = [int(c) for c in "315679824"]
EXTENDED_SIZE = 1_000_000
ITERATIONS = 100
EXTENDED_ITERATIONS = 10_000_000


def main(cups, game):
    print(game(cups))


def simple_cup_game(cups):
    nodes = link_cups(cups)
    current = nodes[cups[0]]
    finished = play_cup_game(current, nodes, ITERATIONS)
    selected = list(cups_after_one(nodes, len(cups) - 1))
    return "".join(str(i) for i in selected)


def extended_cup_game(cups):
    nodes = link_cups(cups, extend=EXTENDED_SIZE)
    current = nodes[cups[0]]
    finished = play_cup_game(current, nodes, EXTENDED_ITERATIONS)
    a, b = cups_after_one(nodes, 2)
    return a * b


@dataclass
class LinkNode:
    label: int
    counterclockwise: "LinkNode"
    clockwise: "LinkNode"


def link_cups(cups, extend=None):
    length = extend if extend is not None else len(cups)
    nodes = [LinkNode(None, None, None) for _ in range(length + 1)]

    for c in cups:
        nodes[c].label = c
    for i, c in enumerate(cups[1:], 1):
        nodes[c].counterclockwise = nodes[cups[i - 1]]
    for i, c in enumerate(cups[:-1]):
        nodes[c].clockwise = nodes[cups[i + 1]]
    nodes[cups[0]].counterclockwise = nodes[cups[-1] if extend is None else -1]
    nodes[cups[-1]].clockwise = nodes[cups[0] if extend is None else len(cups) + 1]

    for c, node in enumerate(nodes[len(cups) + 1 :], len(cups) + 1):
        nodes[c].label = c
    for c, node in enumerate(nodes[len(cups) + 2 :], len(cups) + 2):
        nodes[c].counterclockwise = nodes[c - 1]
    for c, node in enumerate(nodes[len(cups) + 1 : -1], len(cups) + 1):
        nodes[c].clockwise = nodes[c + 1]
    if extend is not None:
        nodes[len(cups) + 1].counterclockwise = nodes[cups[-1]]
        nodes[-1].clockwise = nodes[cups[0]]

    return nodes


def play_cup_game(current, nodes, iterations):
    for i in range(iterations):
        current = cup_game_round(current, nodes)
    return current


def cup_game_round(current, nodes):
    removed_nodes = list(next_nodes(current, 3))
    removed_labels = [node.label for node in removed_nodes]
    current.clockwise = removed_nodes[-1].clockwise
    current.clockwise.counterclockwise = current

    destination_label = bound_range(1, current.label - 1, len(nodes))
    while destination_label in removed_labels:
        destination_label = bound_range(1, destination_label - 1, len(nodes))
    destination_node = nodes[destination_label]

    removed_nodes[-1].clockwise = destination_node.clockwise
    removed_nodes[-1].clockwise.counterclockwise = removed_nodes[-1]
    removed_nodes[0].counterclockwise = destination_node
    destination_node.clockwise = removed_nodes[0]

    return current.clockwise


def next_nodes(current, count):
    for _ in range(count):
        current = current.clockwise
        yield current


def bound_range(low, i, high):
    span = high - low
    return (i - low) % span + low


def cups_after_one(nodes, count):
    current = nodes[1]
    for _ in range(count):
        current = current.clockwise
        yield current.label


def dump_cups(current):
    start = current
    yield current.label
    current = current.clockwise
    while current != start:
        yield current.label
        current = current.clockwise


if __name__ == "__main__":
    game = (
        extended_cup_game
        if len(sys.argv) > 1 and sys.argv[1] == "extended"
        else simple_cup_game
    )
    main(PUZZLE_INPUT, game)
