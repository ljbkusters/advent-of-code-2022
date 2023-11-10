#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
@author Luc Kusters
@date 10-11-2023
"""

import os.path
import typing

import collections

Task = collections.namedtuple("Task", ("low", "high"))
TaskPair = collections.namedtuple("TaskPair", ("t1", "t2"))


def load_data(path: os.PathLike) -> list[str]:
    with open(path, "r") as fhandle:
        lines: list[str] = fhandle.readlines()
    return lines


def parse_data(lines: list[str]) -> list[TaskPair]:
    parsed_data = []
    for line in lines:
        task1, task2 = line.split(",")
        t1 = Task(*list(int(lim) for lim in task1.split("-")))
        t2 = Task(*list(int(lim) for lim in task2.split("-")))
        parsed_data.append(TaskPair(t1, t2))
    return parsed_data 


def fully_contained(task_pair: TaskPair) -> bool:
    t1, t2 = task_pair
    t1_contains_t2 = (t1.low >= t2.low) and (t1.high <= t2.high)
    t2_contains_t1 = (t1.low <= t2.low) and (t1.high >= t2.high)
    if t1_contains_t2 or t2_contains_t1:
        return True
    return False


def argmax(iter_: typing.Iterable):
    return max(zip(iter_, range(len(iter_))))[1]


def overlap(task_pair: TaskPair) -> bool:
    """
    t1 = 6-8
    t2 = 3-4

    t_high = argmax(t1.high, t2.high)
    """
    # sort tasks by max high range value
    idx_high = argmax(tuple(t.high for t in task_pair))
    idx_low = not idx_high
    t_low = task_pair[idx_low]
    t_high = task_pair[idx_high]
    print(t_low, t_high, t_low.high >= t_high.low)
    return t_low.high >= t_high.low


def part_1(parsed_data: list[TaskPair]) -> int:
    num_fully_contained = sum(fully_contained(task_pair)
                              for task_pair in parsed_data
                              )
    return num_fully_contained


def part_2(parsed_data: list[TaskPair]):
    return sum(overlap(task) for task in parsed_data)

def main():
    data = load_data("data.txt")
    parsed_data = parse_data(data)
    print("part 1:", part_1(parsed_data))
    print("part_2:", part_2(parsed_data))

if __name__ == "__main__":
    main()

