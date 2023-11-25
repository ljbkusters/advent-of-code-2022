#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
@author Luc Kusters
@date 25-11-2023
"""

import collections


def get_marker_n_leading_characters(string,
                                    marker_nchars=4):
    assert len(string) >= marker_nchars
    chunk = collections.deque([], maxlen=marker_nchars)
    for i, char in enumerate(string):
        chunk.append(char)
        if len(set(chunk)) == marker_nchars:
            return i + 1


with open("input.txt", "r") as fhandle:
    message = fhandle.read().strip()


print("Part 1")
print("tests...")
print(get_marker_n_leading_characters("bvwbjplbgvbhsrlpgdmjqwftvncz"))
print(get_marker_n_leading_characters("nppdvjthqldpwncqszvftbrmjlhg"))
print(get_marker_n_leading_characters("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"))
print(get_marker_n_leading_characters("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"))
print("part 1 answer")
print(get_marker_n_leading_characters(message))


print("Part 2")
print("tests...")
print(get_marker_n_leading_characters(
    "bvwbjplbgvbhsrlpgdmjqwftvncz", marker_nchars=14))
print(get_marker_n_leading_characters(
    "nppdvjthqldpwncqszvftbrmjlhg", marker_nchars=14))
print(get_marker_n_leading_characters(
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", marker_nchars=14))
print(get_marker_n_leading_characters(
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), marker_nchars=14)
print("part 2 answer")
print(get_marker_n_leading_characters(message, marker_nchars=14))
