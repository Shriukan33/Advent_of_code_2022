import re
from typing import Dict, List, Set, Union

with open("aoc_07_input.txt") as f:
    data = f.read().splitlines()


class Directory:
    # "/absolute/path/to/dir" : Directory
    _dir_dict: Dict[str, "Directory"] = {}

    def __init__(
        self, name: str, parent_dir: Union["Directory", None] = None
    ) -> None:
        self.name = name
        self.parent_dir = parent_dir
        self._sub_dirs: Set["Directory"] = set()
        self._files: Set["File"] = set()
        Directory._dir_dict[self.absolute_path] = self

    @property
    def absolute_path(self) -> str:
        if not self.parent_dir:
            return "/"
        if self.parent_dir and self.parent_dir.absolute_path == "/":
            return f"/{self.name}"
        else:
            return f"{self.parent_dir.absolute_path}/{self.name}"

    @property
    def sub_dirs(self) -> List["Directory"]:
        return self._sub_dirs

    @property
    def files(self) -> List["File"]:
        return self._files

    @property
    def size(self) -> int:
        size = 0
        for file in self.files:
            size += file.size
        for sub_dir in self.sub_dirs:
            size += sub_dir.size
        return size

    def add_sub_dir(self, sub_dir: "Directory") -> None:
        self._sub_dirs.add(sub_dir)

    def add_file(self, file: "File") -> None:
        self._files.add(file)

    @sub_dirs.getter
    def get_sub_dirs(self) -> List["Directory"]:
        return "\n".join([str(sub_dir) for sub_dir in self.sub_dirs])

    @files.getter
    def get_files(self) -> List["File"]:
        return "\n".join([str(file) for file in self.files])

    def __in__(self, other: "Directory") -> bool:
        if not isinstance(other, Directory):
            return False
        return self.absolute_path in other.absolute_path

    def __lte__(self, other: "Directory") -> bool:
        if not isinstance(other, Directory):
            return False
        return self.size <= other.size

    def __lt__(self, other: "Directory") -> bool:
        if not isinstance(other, Directory):
            return False
        return self.size < other.size


class File:
    def __init__(self, name: str, size: int, parent_dir: "Directory") -> None:
        self.name = name
        self.extention = name.split(".")[-1]
        self.size = size
        self.parent_dir = parent_dir

    @property
    def absolute_path(self) -> str:
        if (
            self.parent_dir and self.parent_dir.absolute_path == "/"
        ) or not self.parent_dir:
            return f"/{self.name}"
        return f"{self.parent_dir.absolute_path}/{self.name}"


class State:
    current_dir = None
    root_dir = Directory(name="/")

    @classmethod
    def pwd(cls) -> Directory:
        return cls.current_dir or cls.root_dir

    @classmethod
    def set_current_dir(cls, new_dir: Directory) -> None:
        cls.current_dir = new_dir


class Parser:
    state = State()

    def read_line(self, line: str) -> None:
        if line.startswith("$"):
            self.handle_commands(line)
        elif line.startswith("dir"):
            return self.handle_dir(line)
        elif re.match(r"^\d+", line):
            return self.handle_file(line)

    def handle_commands(self, line: str) -> None:
        # ls has no effect, and doesn't need to be handled
        if line.startswith("$ cd"):
            self.handle_cd(line)

    def handle_cd(self, line: str) -> None:
        dir_name = line.split()[-1]
        if dir_name == "..":
            self.state.set_current_dir(self.state.pwd().parent_dir)
        else:
            for sub_dir in self.state.pwd().sub_dirs:
                if sub_dir.name == dir_name:
                    self.state.set_current_dir(sub_dir)
                    break

    def handle_dir(self, line: str) -> None:
        dir_name = line.split()[-1]
        dir_ = Directory(name=dir_name, parent_dir=self.state.pwd())
        self.state.pwd().add_sub_dir(dir_)

    def handle_file(self, line: str) -> None:
        size, file_name = line.split()
        file = File(
            name=file_name, size=int(size), parent_dir=self.state.pwd()
        )
        self.state.pwd().add_file(file)


def get_dir_size(path: str) -> int:
    return getattr(Directory._dir_dict.get(path), "size", 0)


if __name__ == "__main__":
    parser = Parser()

    for line in data:
        parser.read_line(line)

    # Part 1
    size_of_dirs_under_100000 = sum(
        dir_.size
        for dir_ in Directory._dir_dict.values()
        if dir_.size < 100000
    )
    print("Part 1:", size_of_dirs_under_100000)

    # Part 2
    FILESYSTEM_SIZE = 70_000_000
    TARGETED_AVAILABLE_SPACE = 30_000_000
    CURRENT_AVAILABLE_SPACE = FILESYSTEM_SIZE - get_dir_size("/")
    DIR_TO_DELETE_MIN_SIZE = TARGETED_AVAILABLE_SPACE - CURRENT_AVAILABLE_SPACE

    smallest_dir_to_hit_target = min(
        dir_
        for dir_ in Directory._dir_dict.values()
        if dir_.size >= DIR_TO_DELETE_MIN_SIZE
    )
    print("Part 2:\nMinimal size of dir to delete:", DIR_TO_DELETE_MIN_SIZE)
    print(
        "Found: ", smallest_dir_to_hit_target.size
    )
