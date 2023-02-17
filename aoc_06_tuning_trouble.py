with open("aoc_06_input.txt") as f:
    data = f.read()


def find_marker(data, marker_size):
    accumulator = ""
    for index, char in enumerate(data):
        if len(accumulator) == marker_size:
            print(accumulator, "at index", index)
            break
        if char not in accumulator and len(accumulator) < marker_size:
            accumulator += char
        elif char in accumulator:
            accumulator = accumulator[accumulator.index(char)+1:] + char


if __name__ == "__main__":
    find_marker(data, 4)
    find_marker(data, 14)
