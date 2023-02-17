from collections import namedtuple
from typing import Tuple
import string

with open("aoc_03_input.txt") as f:
    data = f.read().splitlines()


class Rugsack:
    priorities_order = string.ascii_lowercase + string.ascii_uppercase
    priorities = {
        letter: index for index, letter in enumerate(priorities_order, start=1)
    }
    Duplicate = namedtuple("Duplicate", ["item", "priority"])

    def __init__(self, items: list) -> None:
        self.items = items
        self.compartment_A, self.compartment_B = self.split_items(items)

    def split_items(self, items: list) -> Tuple[list, list]:
        """Split items in two equal parts.

        Args:
            items (list): List of items.

        Returns:
            Tuple[list, list]: Tuple of two lists.
        """
        # Split items in two equal parts
        half = len(items) // 2
        return items[:half], items[half:]

    @property
    def duplicate_item(self) -> Duplicate:
        """Find duplicate item.

        Returns:
            Duplicate: Duplicate item.
        """
        duplicate = (
            set(self.compartment_A).intersection(set(self.compartment_B)).pop()
        )
        return self.Duplicate(
            item=duplicate, priority=self.priorities[duplicate]
        )

    def __str__(self) -> str:
        return (
            f"Compartment A: {self.compartment_A} - "
            f"Compartment B: {self.compartment_B}"
        )

    def __repr__(self) -> str:
        return self.__str__()


class ElvenGroup:

    priorities_order = string.ascii_lowercase + string.ascii_uppercase
    priorities = {
        letter: index for index, letter in enumerate(priorities_order, start=1)
    }

    def __init__(self, rugsacks: Tuple[Rugsack]) -> None:
        self.badge = self.get_badge(rugsacks)

    @property
    def priority(self) -> int:
        """Get priority.

        Returns:
            int: Priority.
        """
        return self.priorities[self.badge]

    def get_badge(self, rugsacks: Tuple[Rugsack]) -> str:
        """Get badge. Badge is the only item that is present in all 3 rugsacks.

        Args:
            rugsacks (tuple): Tuple of rugsacks.

        Returns:
            str: Badge.
        """
        # Get items from all rugsacks
        items = [rugsack.items for rugsack in rugsacks]
        # Get items that are present in all rugsacks
        badge = set(items[0]).intersection(*items[1:])
        return badge.pop()


def get_group_of_elves(rugsack_list: list, size=3) -> tuple:
    """Get group of size rugsacks.

    Args:
        rugsack_list (list): List of rugsacks.

    Returns:
        tuple: Tuple of size rugsacks.
    """
    # Split list of rugsacks in groups of 3
    current_index = 0
    for _ in rugsack_list:
        yield tuple(rugsack_list[current_index : current_index + size]) # noqa
        current_index += size


if __name__ == "__main__":
    # Part 1
    # all_rugsacks = [Rugsack(items) for items in data]
    # duplicate_items = [rugsack.duplicate_item for rugsack in all_rugsacks]
    # print(sum(item.priority for item in duplicate_items))

    # Part 2
    all_rugsacks = [Rugsack(items) for items in data]
    group_generator = get_group_of_elves(all_rugsacks)
    sum_of_priorities = 0
    for group in group_generator:
        if group:
            elven_group = ElvenGroup(group)
            sum_of_priorities += elven_group.priority

    print(sum_of_priorities)
