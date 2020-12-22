#!/usr/bin/env python3

from collections import deque


def main():
    decks = load_decks("data/day22-cards.txt")
    play_until_won(*decks)
    print(score(winner(*decks)))


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


def play_one_round(deck_a, deck_b):
    card_a = deck_a.popleft()
    card_b = deck_b.popleft()
    if card_a > card_b:
        deck_a.extend([card_a, card_b])
    else:
        deck_b.extend([card_b, card_a])


def winner(deck_a, deck_b):
    return deck_a if deck_a else deck_b


def score(deck):
    return sum(
        position * card for (position, card) in enumerate(reversed(deck), start=1)
    )


if __name__ == "__main__":
    main()
