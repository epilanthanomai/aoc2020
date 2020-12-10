#!/usr/bin/env python3

import sys
from collections import defaultdict, deque

MAX_ADAPTER = 3


def main(calculate_paths):
    with open("data/day10-joltage.txt") as jolts_file:
        jolts = list(sorted(int(line) for line in jolts_file))
    final_jolts = jolts[-1] + MAX_ADAPTER
    jolts = jolts + [final_jolts]
    adapters = collect_adaptor_counts(jolts, 0, final_jolts)
    if calculate_paths:
        print(count_adapter_paths(jolts, 0, final_jolts))
    else:
        print(adapters[1] * adapters[3])


def collect_adaptor_counts(jolts, start, final):
    current = start
    adapters = defaultdict(int)
    for jolt in jolts:
        adapter = jolt - current
        adapters[adapter] += 1
        current = jolt
    return adapters


def count_adapter_paths(jolts, start, final):
    path_counts = defaultdict(int)

    for i in range(0, MAX_ADAPTER + 1):
        path_counts[start + i] += 1

    for jolt in jolts:
        paths = path_counts[jolt]
        for i in range(1, MAX_ADAPTER + 1):
            path_counts[jolt + i] += paths
    return path_counts[final]


if __name__ == "__main__":
    calculate_paths = len(sys.argv) > 1 and sys.argv[1] == "paths"
    main(calculate_paths)
