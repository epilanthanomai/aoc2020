#!/usr/bin/env python3

import collections
import sys


def main(try_modification):
    with open("data/day08-instructions.txt") as instruction_file:
        instructions = parse_instructions(instruction_file)
    # We could brute force this in quadratic time, but instead let's use linear time static analysis.
    instruction_filter = None
    if try_modification:
        chunk_ids, terminating_chunks = analyze_chunks(instructions)
        instruction_filter = InstructionFixer(chunk_ids, terminating_chunks)
    machine = LoopSafeMachine()
    machine.execute(instructions, instruction_filter)
    print(machine.accumulator)


def parse_instructions(lines):
    return [parse_instruction(line.strip()) for line in lines]


def parse_instruction(line):
    instruction, raw_argument = line.split()
    return instruction, int(raw_argument)


def analyze_chunks(instructions):
    chunk_ids, chunks = chunk_instructions(instructions)
    targets = calculate_jump_targets(instructions, chunks)
    terminating_chunks = identify_terminating_chunks(
        instructions, chunk_ids, chunks, targets
    )
    return chunk_ids, terminating_chunks


def chunk_instructions(instructions):
    chunk_ids, chunks = [], []
    start = None
    chunk_id = 0
    for i, (instruction, argument) in enumerate(instructions):
        chunk_ids.append(chunk_id)
        if start is None:
            start = i
        if instruction == "jmp":
            chunks.append((start, i - start + 1, i + argument))
            start = None
            chunk_id += 1
    return chunk_ids, chunks


def calculate_jump_targets(instructions, chunks):
    result = collections.defaultdict(list)
    for i, (instruction, argument) in enumerate(instructions):
        if instruction == "jmp":
            target = i + argument
            result[target].append(i)
    return result


def identify_terminating_chunks(instructions, chunk_ids, chunks, targets):
    result = set(
        chunk_id
        for (chunk_id, (_, _, jump_target)) in enumerate(chunks)
        if jump_target >= len(instructions)
    )
    new_chunks = result
    while new_chunks:
        next_chunks = set()
        for chunk_id in new_chunks:
            start, length, _ = chunks[chunk_id]
            for instruction_id in range(start, start + length):
                for from_instruction_id in targets[instruction_id]:
                    from_chunk_id = chunk_ids[from_instruction_id]
                    next_chunks.add(from_chunk_id)
        next_chunks = next_chunks.difference(result)
        new_chunks = next_chunks.difference(result)
        result = result.union(next_chunks)
    return result


class LoopSafeMachine:
    def __init__(self):
        self.program_counter = 0
        self.accumulator = 0
        self.visited = set()

    def execute(self, instructions, instruction_filter):
        filter_used = False
        while self.program_counter_valid(instructions):
            instruction = instructions[self.program_counter]
            if instruction_filter and not filter_used:
                instruction, changed = instruction_filter.filter_instruction(
                    instructions, self.program_counter
                )
                if changed:
                    filter_used = True
            self.step(*instruction)

    def program_counter_valid(self, instructions):
        return (
            self.program_counter >= 0
            and self.program_counter < len(instructions)
            and self.program_counter not in self.visited
        )

    def step(self, instruction, argument):
        do_instruction = getattr(self, "instruction_" + instruction)
        self.visited.add(self.program_counter)
        do_instruction(argument)
        if not getattr(do_instruction, "sets_pc", False):
            self.program_counter += 1

    def instruction_acc(self, argument):
        self.accumulator += argument

    def instruction_jmp(self, argument):
        self.program_counter += argument

    instruction_jmp.sets_pc = True

    def instruction_nop(self, _):
        pass


class InstructionFixer:
    def __init__(self, chunk_ids, terminating_chunks):
        self.chunk_ids = chunk_ids
        self.terminating_chunks = terminating_chunks

    def filter_instruction(self, instructions, program_counter):
        instruction, argument = instructions[program_counter]
        do_filter = getattr(self, "filter_" + instruction)
        return do_filter(instructions, program_counter)

    def filter_acc(self, instructions, program_counter):
        return instructions[program_counter], False

    def filter_jmp(self, instructions, program_counter):
        # Consider changing this to a nop. In that case, execution will flow into the next chunk. If that chunk
        # terminates then this updated instruction set terminates.
        _, argument = instructions[program_counter]
        if self.chunk_ids[program_counter + 1] in self.terminating_chunks:
            return ("nop", argument), True
        else:
            return instructions[program_counter], False

    def filter_nop(self, instructions, program_counter):
        # Consider changing this to a jmp. In that case, if the target is part of a terminating branch then this
        # updated instruction set terminates.
        _, argument = instructions[program_counter]
        jump_target = program_counter + argument
        target_chunk_id = self.chunk_ids[jump_target]
        if target_chunk_id in self.terminating_chunks:
            return ("jmp", argument), True
        else:
            return instructions[program_counter], False


if __name__ == "__main__":
    try_modification = len(sys.argv) > 1 and bool(int(sys.argv[1]))
    main(try_modification)
