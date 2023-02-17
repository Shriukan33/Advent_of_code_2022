from collections import namedtuple

with open("aoc_04_input.txt") as f:
    data = f.read().splitlines()

ElvenPair = namedtuple("ElvenPair", ["elf_1", "elf_2"])
all_pairs = [ElvenPair(*line.split(",")) for line in data if line]


class Elf:
    def __init__(self, sections_to_clean: str):
        self.sections_to_clean = sections_to_clean
        self.sections_list = self._get_sections_list(sections_to_clean)

    @property
    def section_count(self) -> int:
        return len(self.sections_list)

    def _get_sections_list(self, sections_to_clean: str) -> set:
        sections_limits = sections_to_clean.split("-")
        return set(range(int(sections_limits[0]), int(sections_limits[1]) + 1))

    def __contains__(self, item):
        return item in self.sections_list


if __name__ == "__main__":
    number_of_overlaps = 0
    for pair in all_pairs:
        elf_1 = Elf(pair.elf_1)
        elf_2 = Elf(pair.elf_2)
        bigger_elf = (
            elf_1 if elf_1.section_count >= elf_2.section_count else elf_2
        )
        smaller_elf = elf_1 if elf_2 is bigger_elf else elf_2

        # Part 1
        if all(
            section in bigger_elf.sections_list
            for section in smaller_elf.sections_list
        ):
            number_of_overlaps += 1

        # # Part 2
        # if any(
        #     section in bigger_elf.sections_list
        #     for section in smaller_elf.sections_list
        # ):
        #     number_of_overlaps += 1

    print(number_of_overlaps)
