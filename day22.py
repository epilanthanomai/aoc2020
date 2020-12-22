#!/usr/bin/env python3

import sys
from collections import deque
from copy import deepcopy

RECURSION_DEFAULT_WINNER = 0


def main(play):
    decks = load_decks("data/day22-cards.txt")
    winner = play(*decks)
    print(score(decks[winner]))


def load_decks(file_name):
    with open(file_name) as deck_file:
        data = deck_file.read()
    players_data = data.split("\n\n")
    return [
        deque([int(line) for line in player_data.splitlines()[1:]])
        for player_data in players_data
    ]


def play_until_won(deck_a, deck_b):
    while deck_a and deck_b:
        play_one_round(deck_a, deck_b)

    return 0 if deck_a else 1


def play_one_round(deck_a, deck_b):
    card_a = deck_a.popleft()
    card_b = deck_b.popleft()
    if card_a > card_b:
        deck_a.extend([card_a, card_b])
    else:
        deck_b.extend([card_b, card_a])


def play_recursively_until_won(deck_a, deck_b):
    decks_cache = set()
    is_initial_deck = True
    while deck_a and deck_b:
        hashable_decks = tuple(deck_a), tuple(deck_b)
        deck_hash = hash(hashable_decks)
        if deck_hash in decks_cache:
            return RECURSION_DEFAULT_WINNER
        decks_cache.add(deck_hash)

        is_initial_deck = False
        play_one_recursive_round(deck_a, deck_b)

    winner = 0 if deck_a else 1
    return winner


def play_one_recursive_round(deck_a, deck_b):
    card_a = deck_a.popleft()
    card_b = deck_b.popleft()
    if len(deck_a) >= card_a and len(deck_b) >= card_b:
        sub_deck_a = deque(list(deck_a)[:card_a])
        sub_deck_b = deque(list(deck_b)[:card_b])
        winner = play_recursively_until_won(sub_deck_a, sub_deck_b)
    else:
        winner = 0 if card_a > card_b else 1

    if winner == 0:
        deck_a.extend([card_a, card_b])
    else:
        deck_b.extend([card_b, card_a])


def score(deck):
    return sum(
        position * card for (position, card) in enumerate(reversed(deck), start=1)
    )


if __name__ == "__main__":
    play = (
        play_recursively_until_won
        if len(sys.argv) > 1 and sys.argv[1] == "recursive"
        else play_until_won
    )
    main(play)
