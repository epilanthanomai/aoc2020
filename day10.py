#!/usr/bin/env python3

from collections import defaultdict


def main():
    with open("data/day10-joltage.txt") as jolts_file:
        jolts = [int(line) for line in jolts_file]
    adapters = collect_adaptor_counts(sorted(jolts))
    print(adapters[1] * adapters[3])


def collect_adaptor_counts(jolts):
    current = 0
    adapters = defaultdict(int)
    for jolt in jolts:
        adapter = jolt - current
        adapters[adapter] += 1
        current = jolt
    # Final jolt is current+3
    adapters[3] += 1
    return adapters


if __name__ == "__main__":
    main()
