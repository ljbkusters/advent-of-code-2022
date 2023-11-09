def __compartmentalise_input_string(input_string: str) -> tuple[str, 2]:
    """Returns compartment substrings for a given input string

    Since each rucksack contains the same number of items
    in each compartment, we simple take split the input string
    at half the length of the input_string.

    arguments:
        input_string (str): input string (rucksack contents)
    returns:
        compartment contents: tuple of length 2 of parital input strings 
    """
    if len(input_string) % 2 != 0:
        raise RuntimeError("Input string must be of even length"
                           " but you provided an odd length string")
    split_idx = len(input_string)//2
    compartments = (input_string[:split_idx], input_string[split_idx:])
    return compartments


def __hash_map_input_string(input_str: str) -> dict[str, bool]:
    """returns a has"""
    return {char: True for char in input_str}


def __value_of_char(char: str) -> int:
    """Return value of char by aoc counting

    aoc requires
    a~z : 1~26
    A~Z : 27~52 

    ASCII values
    a~z: 97~122
    A~Z: 65~90

    Input is assumed to be one of [a-z][A-Z]

    argumentns:
        char (str): input char
    returns:
        value (int): AOC value of input char
    """
    ascii_value = ord(char)
    if ascii_value >= 97:
        return ascii_value - 97 + 1
    else:
        return ascii_value - 65 + 26 + 1


def __find_common_character(rucksack_str: str) -> str:
    """Returns common character in rucksack str

    arguments:
        rucksack_str (str): input string
    returns:
        common character (str)
    """
    compartment_1, compartment_2 = __compartmentalise_input_string(rucksack_str)
    hash_map_1 = __hash_map_input_string(compartment_1)
    hash_map_2 = __hash_map_input_string(compartment_2)
    for key in hash_map_1.keys():
        if hash_map_2.get(key, False):
            return key

def find_common_character_value(rucksack_str: str) -> int:
    """Find the common character in the two compartment rucksack

    answer to part 1 of day 3

    arguments:
        rucksack_str (str): full string of rucksack contents
    returns:
        common item value (int)
    """
    return __value_of_char(__find_common_character(rucksack_str))

def __hash_rucksack_contents_by_item(rucksack_strings: tuple[str]) -> dict[str, list[int]]:
    rucksack_mapping = {}
    for i, contents in enumerate(rucksack_strings):
        for char in contents:
            if char not in rucksack_mapping:
                rucksack_mapping[char] = set()
            rucksack_mapping[char].add(i)
    return rucksack_mapping


def __count_rucksack_hash_elf_occurences(__rucksack_hash: dict[str: int]):
    return {char: len(elfs) for char, elfs in __rucksack_hash.items()}


# public function
count_rucksack_hash_occurences = __count_rucksack_hash_elf_occurences


def __get_badge(rucksack_hash: dict[str: int]) -> str:
    for char, num_elfs in rucksack_hash.items():
        if num_elfs == 3:
            return char


def __split_to_groups(rucksack_strings: tuple[str], group_size: int=3) -> tuple[tuple[str]]:
    """Split rucksack_strings (Iterable of strings) into groups of size group_size"""
    return tuple(rucksack_strings[i:i+group_size] 
                 for i in range(0, len(rucksack_strings), group_size))


def __find_badge_chars(rucksack_strings: tuple[str]) -> tuple[str]:
    """find which items occur three times

    """
    groups = __split_to_groups(rucksack_strings)
    badges = []
    for group in groups:
        group_hash = __hash_rucksack_contents_by_item(group)
        counted_rucksack_hash = __count_rucksack_hash_elf_occurences(group_hash)
        badges.append(__get_badge(counted_rucksack_hash))
    return badges

def find_badge_values(rucksack_strings: tuple[str]) -> tuple[int]:
    """find which items occur three times

    """
    badges = __find_badge_chars(rucksack_strings)
    return tuple(__value_of_char(badge) for badge in badges)

if __name__ == "__main__":
    # test __compartmentalise_input_string
    assert __compartmentalise_input_string("aaaAAA") == ("aaa", "AAA")
    assert __compartmentalise_input_string("abaABA") == ("aba", "ABA")
    try:
        __compartmentalise_input_string("abABA")
    except RuntimeError:
        pass # OK
    except Exception as e:
        raise AssertionError("The function should have thrown a RuntimeError but"
                             f" threw an error of type {type(e)} instead.")
    
    # check if __value_of_char maps correctly to AOC requirements
    assert __value_of_char("a") == 1
    assert __value_of_char("z") == 26
    assert __value_of_char("A") == 27
    assert __value_of_char("Z") == 52

    # check __hashmap_input_string
    assert __hash_map_input_string("aaAB") == {"a": True, "A": True, "B": True}
    assert __hash_map_input_string("aaAABBCCC") == {"a": True, "A": True, "B": True, "C": True}

    # check __check_find_common_characters
    assert __find_common_character("aAaB") == "a"
    assert __find_common_character("aAbA") == "A"
    # AOC examples
    assert __find_common_character("vJrwpWtwJgWrhcsFMMfFFhFp") == "p"
    assert __find_common_character("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL") == "L"
    assert __find_common_character("PmmdzqPrVvPwwTWBwg") == "P"
    assert __find_common_character("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn") == "v"
    assert __find_common_character("ttgJtRGJQctTZtZT") == "t"
    assert __find_common_character("CrZsJsPPZsGzwwsLwLmpwMDw") == "s"

    # problem 2 tests
    assert __split_to_groups(("a", "b", "c", "d", "e", "f")) == (("a", "b", "c"), ("d", "e", "f"))
    test_1 = {
        "input": (
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
            ),
        "ans": "r",
        }
    test_2 = {
        "input": (
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw",
            ),
        "ans": "Z",
        }
    assert __find_badge_chars(test_1["input"])[0] == test_1["ans"]
    assert find_badge_values(test_1["input"])[0] == __value_of_char(test_1["ans"])
    assert __find_badge_chars(test_2["input"])[0] == test_2["ans"]
    assert find_badge_values(test_2["input"])[0] == __value_of_char(test_2["ans"])