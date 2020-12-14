#!/usr/bin/env python3

import operator
import re
import sys
from collections import defaultdict
from functools import reduce


def main(machine):
    with open("data/day14-docking.txt") as instructions_file:
        instructions = [parse_instruction(line.strip()) for line in instructions_file]
    for (target, value) in instructions:
        if target is None:
            machine.set_mask(value)
        else:
            machine.set_memory(target, value)
    print(sum_all_memory_values(machine))


def parse_instruction(line):
    raw_target, _, raw_value = line.partition(" = ")
    if raw_target == "mask":
        return (None, raw_value)
        return parse_mask_instruction(raw_value)
    else:
        return parse_set_instruction(raw_target, raw_value)


SET_RE = re.compile(r"^mem\[(\d+)\]")


def parse_set_instruction(raw_target, raw_value):
    m = SET_RE.match(raw_target)
    address = int(m.group(1))
    value = int(raw_value)
    return (address, value)


class MachineV1:
    MASK_BITMASK_TABLE = {
        ord("X"): "1",
        ord("1"): "0",
        ord("0"): "0",
    }
    MASK_FORCE_TABLE = {
        ord("X"): "0",
        ord("1"): "1",
        ord("0"): "0",
    }

    def __init__(self):
        self.bitmask = None
        self.force = None
        self.memory = defaultdict(int)

    def set_mask(self, mask):
        self.bitmask = int(mask.translate(self.MASK_BITMASK_TABLE), 2)
        self.force = int(mask.translate(self.MASK_FORCE_TABLE), 2)

    def set_memory(self, target, value):
        masked_value = (value & self.bitmask) | self.force
        self.memory[target] = masked_value


class MachineV2:
    MASK_INVERSE_FLOAT_TABLE = {
        ord("X"): "0",
        ord("1"): "1",
        ord("0"): "1",
    }
    MASK_FORCE_TABLE = {
        ord("X"): "0",
        ord("1"): "1",
        ord("0"): "0",
    }

    def __init__(self):
        self.memory = defaultdict(int)
        self.floating_bits = []
        self.inverse_float_mask = None
        self.force = None

    def set_mask(self, mask):
        self.floating_bits = [i for (i, bit) in enumerate(reversed(mask)) if bit == "X"]
        self.inverse_float_mask = int(mask.translate(self.MASK_INVERSE_FLOAT_TABLE), 2)
        self.force = int(mask.translate(self.MASK_FORCE_TABLE), 2)

    def set_memory(self, target, value):
        forced_address = target & self.inverse_float_mask | self.force
        for float_bits in self.generate_float_bits():
            address = forced_address | float_bits
            self.memory[address] = value

    def generate_float_bits(self):
        bit_count = len(self.floating_bits)
        for i in range(2 ** bit_count):
            # take the bits of i and expand them into the bits of the float_bits
            input_bit_flags = (1 << j for j in range(bit_count))
            output_bit_flags = (1 << self.floating_bits[j] for j in range(bit_count))
            bit_pairs = zip(input_bit_flags, output_bit_flags)
            yield reduce(
                operator.or_,
                (out_flag for (in_flag, out_flag) in bit_pairs if i & in_flag),
                0,
            )


def sum_all_memory_values(machine):
    return sum(machine.memory.values())


if __name__ == "__main__":
    Machine = {
        "1": MachineV1,
        "2": MachineV2,
    }[sys.argv[1]]
    main(Machine())
