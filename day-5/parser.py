#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parser.py
@author Luc Kusters
@date 11-11-2023
"""

import os

import stack


def split_at_empty_line(raw_data: list[str]) -> tuple[list[str], list[str]]:
    split_index = None
    for idx, line in enumerate(raw_data):
        if line == "":
            split_index = idx
            break
    if split_index is None:
        raise RuntimeError("No empty line found")
    return raw_data[:split_index], raw_data[split_index+1:]


def __parse_drawing_line(line: str, stacks: list[stack.Stack]) -> None:
    """In place parsing of one line to stacks

    Loops over string, checks if previous char was a '[' and if so
    pushes the current char to the corresponding stack. Each stack has a
    spacing of 4 characters, so we know which stack to push to by taking
    the char_idx of the current char and (integer) deviding by 4
    """
    last_char = None
    for idx, char in enumerate(line):
        if last_char == "[":
            stacks[idx//4].push(char)
        last_char = char


def __get_num_stacks(stacks_counter_line: str) -> int:
    return sum(1 if char not in (" ",) else 0
               for char in stacks_counter_line)


def drawing_parser(drawing_lines: list[str]) -> list[stack.Stack]:
    num_stacks = __get_num_stacks(drawing_lines[-1])
    stacks = [stack.Stack() for _ in range(num_stacks)]
    for line in reversed(drawing_lines[:-1]):
        __parse_drawing_line(line, stacks)
    return stacks


def __parse_command_line(command_line: str) -> tuple[int]:
    split_line = command_line.split(" ")
    n_moves = int(split_line[1])
    from_stack = int(split_line[3]) - 1  # account for 0 indexation
    to_stack = int(split_line[5]) - 1
    return (n_moves, from_stack, to_stack)


def __execute_command(cmd: tuple[int], stacks: list[stack.Stack]) -> None:
    """In place execution of move command"""
    n_moves, from_stack, to_stack = cmd
    for _ in range(n_moves):
        char = stacks[from_stack].pop()
        stacks[to_stack].push(char)

def __execute_9001_command(cmd: tuple[int], stacks: list[stack.Stack]) -> None:
    """In place executeion of 9001 command

    the 9001 model can pick up multiple crates at once
    """
    n_moves, from_stack, to_stack = cmd
    picked_up_crates = []
    for _ in range(n_moves):
        char = stacks[from_stack].pop()
        picked_up_crates.append(char)
    # reverse push order to simulate multi-crate lifting
    for char in reversed(picked_up_crates):
        stacks[to_stack].push(char)


def load_data(path: os.PathLike):
    with open(path, "r") as fhandle:
        raw_data = [l.strip() for l in fhandle.readlines()]
    return raw_data


def __check_top_layer(stacks: list[stack.Stack]) -> str:
    top_layer = ""
    for _, _stack in enumerate(stacks):
        top_layer += _stack.head()
    return top_layer


def part_1() -> str:
    raw_data = load_data("input.txt")
    drawing, commands = split_at_empty_line(raw_data)
    stacks = drawing_parser(drawing)
    for command_line in commands:
        command = __parse_command_line(command_line)
        __execute_command(command, stacks)
    top_layer = __check_top_layer(stacks)
    return top_layer


def part_2():
    raw_data = load_data("input.txt")
    drawing, commands = split_at_empty_line(raw_data)
    stacks = drawing_parser(drawing)
    for command_line in commands:
        command = __parse_command_line(command_line)
        __execute_9001_command(command, stacks)
    top_layer = __check_top_layer(stacks)
    return top_layer



def main():
    print("-- PART 1 --")
    print(part_1())
    print("-- PART 2 --")
    print(part_2())


if __name__ == "__main__":
    print("======== START TEST ========")
    test_drawing = [
        "    [D]    ",
        "[N] [C]    ",
        "[Z] [M] [P]",
        " 1   2   3 ",
    ]
    test_commands = [
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2",
    ]
    stacks = drawing_parser(test_drawing)
    print(stacks)
    for cmd_line in test_commands:
        cmd = __parse_command_line(cmd_line)
        __execute_command(cmd, stacks)
        print(stacks)
    print("======== END TEST ========")

    main()
