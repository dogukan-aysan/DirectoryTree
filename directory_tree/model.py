"""This module contains the code that supports the app’s main functionalities. """

import os
from colored import Style, style, back, fore
from dataclasses import dataclass


def generate(path, max_depth, colorless) -> str:
    my_data_class = DataClass(
        path=path,
        current_item=None,
        last_item_states={"0": False},
        max_depth=max_depth,
        colorless=colorless,
    )
    my_traverser = Traverser(my_data_class)
    my_traverser.traverse()
    return my_data_class.tree


@dataclass
class DataClass:
    path: str
    current_item: os.DirEntry | None
    last_item_states: dict
    max_depth: int
    colorless: bool = False
    tree: str = ""
    is_last_item: bool = False
    current_level: int = 0


class Traverser:
    def __init__(self, data):
        self.data = data
        if self.data.colorless:
            self.my_line_generator = _ColorlessLineGenerator(self.data)
        else:
            self.my_line_generator = _LineGenerator(self.data)

    def traverse(self):
        items = self._get_items()
        if not len(items) == 0:
            for item in items:
                self.data.current_item = item
                self.data.is_last_item = items.index(item) == len(items) - 1
                self._add_line_to_tree()
                if item.is_dir():
                    if self._is_max_depth_reached():
                        continue
                    else:
                        self._increase_level()
                        self.data.path = self.data.current_item.path
                        self.traverse()
                        self.data.current_level -= 1

    def _add_line_to_tree(self):
        line = self.my_line_generator.generate_line()
        self.data.tree += line

    def _get_items(self) -> list:
        generator_obj_of_directory = os.scandir(self.data.path)
        items = []
        if generator_obj_of_directory:
            while True:
                try:
                    item = next(generator_obj_of_directory)
                    items.append(item)
                except StopIteration:
                    break
        return items

    def _is_max_depth_reached(self) -> bool:
        if self.data.current_level + 1 >= self.data.max_depth:
            return True
        return False

    def _increase_level(self):
        self.data.current_level += 1
        self.data.last_item_states[str(self.data.current_level)] = False


class _LineGenerator:
    def __init__(self, data) -> None:
        self.data = data
        self.line = ""
        self.space_prefix = "    "
        self.pipe_prefix = "│   "
        self.tee = "├──"
        self.elbow = "└──"
        self.directory_color = f"{style(1)}{back(18)}"
        self.file_color = f"{style(1)}{fore(40)}"
        self.symlink_color = f"{style(1)}{fore(84)}{back(43)}"

    def generate_line(self) -> str:
        self.line = ""
        self._write_prefix()
        self._write_tee_or_elbow()
        self._write_item()
        return self.line

    def _write_prefix(self) -> None:
        for last_item_state in range(self.data.current_level):
            if self.data.last_item_states[str(last_item_state)]:
                self.line += self.space_prefix
            else:
                self.line += self.pipe_prefix

    def _write_tee_or_elbow(self) -> None:
        if self.data.is_last_item:
            self.data.last_item_states[str(self.data.current_level)] = True
            self.line += self.elbow
        else:
            self.line += self.tee

    def _write_item(self) -> None:
        if self.data.current_item.is_dir(follow_symlinks=False):
            self.line += (
                f" {self.directory_color}{self.data.current_item.name}{Style.reset}"
                + "\n"
            )
        elif self.data.current_item.is_file(follow_symlinks=False):
            self.line += (
                f" {self.file_color}{self.data.current_item.name}{Style.reset}" + "\n"
            )
        elif self.data.current_item.is_symlink():
            self.line += (
                f" {self.symlink_color}{self.data.current_item.name}{Style.reset}"
                + "\n"
            )

        else:
            raise TypeError("unknown item type")


class _ColorlessLineGenerator(_LineGenerator):
    def __init__(self, data) -> None:
        super().__init__(data)

    def _write_item(self) -> None:
        self.line += self.data.current_item.name + "\n"
