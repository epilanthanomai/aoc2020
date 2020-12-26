#!/usr/bin/env python3

PUBLIC_KEYS = [
    18356117,
    5909654,
]

START_SUBJECT = 7
START_TRANSFORM = 1
MAGIC_MOD = 20201227


def main():
    key_a, key_b = PUBLIC_KEYS
    key_loop_pairs = crack_loop_size(*PUBLIC_KEYS)
    loop_size_b = key_loop_pairs[key_b]
    print(subject_transform(key_a, loop_size_b))


# card_key = subject_transform(7, card_loop)
# door_key = subject_transfor(7, door_loop)
# shared_key == subject_transform(door_key, card_loop)
# shared_key == subject_transform(card_key, door_loop)


def crack_loop_size(*public_keys):
    identified = {}
    unidentified = set(public_keys)
    for (loop, key) in enumerate(generate_loop_keys()):
        if key in unidentified:
            identified[key] = loop
            unidentified.remove(key)
            if not unidentified:
                return identified


def generate_loop_keys():
    n = START_TRANSFORM
    while True:
        yield n
        n = subject_transform_once(n, START_SUBJECT)


def subject_transform(subject, loop):
    n = START_TRANSFORM
    for _ in range(loop):
        n = subject_transform_once(n, subject)
    return n


def subject_transform_once(n, subject):
    return (n * subject) % MAGIC_MOD


if __name__ == "__main__":
    main()
