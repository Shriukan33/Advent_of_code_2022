import re
from enum import Enum, auto
from typing import List, NamedTuple


with open("aoc_05_input.txt") as f:
    data = f.read().splitlines()


class State(Enum):
    IN_BRACKETS = auto()
    OUTSIDE_BRACKETS = auto()


class SupplyCrate(NamedTuple):
    letter: str
    column: int


class Instruction(NamedTuple):
    quantity_to_move: int
    origin_column: int
    destination_column: int


class SupplyStackParser:
    state = State.OUTSIDE_BRACKETS

    def parse_supply_stacks(self, line: str) -> List[SupplyCrate]:
        supply_crates = []
        # Columns numbers start at 1, we start at 0 to ease list
        # manipulation later.
        current_column = 0
        for index, char in enumerate(line, start=1):
            if char == "[":
                self.state = State.IN_BRACKETS
            elif char == "]":
                self.state = State.OUTSIDE_BRACKETS
            elif self.state == State.IN_BRACKETS and char.isalpha():
                supply_crates.append(
                    SupplyCrate(letter=char, column=current_column)
                )
            elif self.state == State.OUTSIDE_BRACKETS and char.isdigit():
                break
            elif (
                self.state == State.OUTSIDE_BRACKETS
                and char == " "
                # Each column is 4 characters wide '[A] '.
                and index % 4 == 0
            ):
                current_column += 1

        return supply_crates


def parse_instruction(line: str) -> List[Instruction]:
    instructions = []
    for match in re.finditer(r"move (\d+) from (\d+) to (\d+)", line):
        instructions.append(
            Instruction(
                quantity_to_move=int(match.group(1)),
                origin_column=int(match.group(2)) - 1,
                destination_column=int(match.group(3)) - 1,
            )
        )
    return instructions


if __name__ == "__main__":
    supply_stack_parser = SupplyStackParser()
    all_crates: List[SupplyCrate] = []
    all_instructions: List[Instruction] = []
    for line in data:
        if line.startswith("move"):
            all_instructions.extend(parse_instruction(line))
        elif line.startswith("["):
            all_crates.extend(supply_stack_parser.parse_supply_stacks(line))

    # We add +1 because we saved the column number starting at 0.
    number_of_stacks = max(crate.column for crate in all_crates) + 1
    all_stacks = [[] for _ in range(number_of_stacks)]
    # Because we created crates from top to bottom and I feel
    # more comfortable with the stacks from bottom to top, we
    # reverse the list.
    for crate in reversed(all_crates):
        all_stacks[crate.column].append(crate.letter)

    # # Part 1
    # for instruction in all_instructions:
    #     # Crates are moved one by one.
    #     crates_to_move = [
    #         all_stacks[instruction.origin_column].pop()
    #         for _ in range(instruction.quantity_to_move)
    #     ]
    #     for crate in crates_to_move:
    #         all_stacks[instruction.destination_column].append(crate)

    # print("".join(stack.pop() for stack in all_stacks))

    # Part 2
    for instruction in all_instructions:
        # Crates are moved in a single operation.
        crates_to_move = all_stacks[instruction.origin_column][
            -instruction.quantity_to_move :
        ]
        # We remove the crates from the origin stack.
        all_stacks[instruction.origin_column] = all_stacks[
            instruction.origin_column
        ][: -instruction.quantity_to_move]
        # We add the crates to the destination stack.
        all_stacks[instruction.destination_column].extend(crates_to_move)

    print("".join(stack.pop() for stack in all_stacks))
