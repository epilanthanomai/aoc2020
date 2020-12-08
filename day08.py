#!/usr/bin/env python3


def main():
    with open("data/day08-instructions.txt") as instruction_file:
        instructions = parse_instructions(instruction_file)
    machine = LoopSafeMachine()
    machine.execute(instructions)
    print(machine.accumulator)


def parse_instructions(lines):
    return [parse_instruction(line.strip()) for line in lines]


def parse_instruction(line):
    instruction, raw_argument = line.split()
    return instruction, int(raw_argument)


class LoopSafeMachine:
    def __init__(self):
        self.program_counter = 0
        self.accumulator = 0
        self.visited = set()

    def execute(self, instructions):
        while self.program_counter_valid(instructions):
            self.step(*instructions[self.program_counter])

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


if __name__ == "__main__":
    main()
