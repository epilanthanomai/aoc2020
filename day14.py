#!/usr/bin/env python3

import re
from collections import defaultdict


def main():
    with open("data/day14-docking.txt") as instructions_file:
        instructions = [parse_instruction(line.strip()) for line in instructions_file]
    machine = Machine()
    machine.execute_all(instructions)
    print(sum_all_memory_values(machine))


def parse_instruction(line):
    raw_target, _, raw_value = line.partition(" = ")
    if raw_target == "mask":
        return parse_mask_instruction(raw_value)
    else:
        return parse_set_instruction(raw_target, raw_value)


def parse_mask_instruction(raw_mask):
    mask = int(
        raw_mask.translate(
            {
                ord("X"): "1",
                ord("1"): "0",
                ord("0"): "0",
            }
        ),
        2,
    )
    force = int(
        raw_mask.translate(
            {
                ord("X"): "0",
                ord("1"): "1",
                ord("0"): "0",
            }
        ),
        2,
    )
    return (None, (mask, force))


SET_RE = re.compile(r"^mem\[(\d+)\]")


def parse_set_instruction(raw_target, raw_value):
    m = SET_RE.match(raw_target)
    address = int(m.group(1))
    value = int(raw_value)
    return (address, value)


class Machine:
    def __init__(self):
        self.mask = None
        self.force = None
        self.memory = defaultdict(int)

    def execute_all(self, instructions):
        for instruction in instructions:
            self.execute(instruction)

    def execute(self, instruction):
        target, value = instruction
        if target is None:
            self.set_mask(*value)
        else:
            self.set_memory(target, value)

    def set_mask(self, mask, force):
        self.mask = mask
        self.force = force

    def set_memory(self, target, value):
        masked_value = (value & self.mask) | self.force
        self.memory[target] = masked_value


def sum_all_memory_values(machine):
    return sum(machine.memory.values())


if __name__ == "__main__":
    main()
