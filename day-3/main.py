import rucksack

with open("data.txt", "r") as fhandle:
    data = [l.strip() for l in fhandle.readlines()]

common_values = [rucksack.find_common_character_value(rucksack_str)
                 for rucksack_str in data]
print('part 1')
print(sum(common_values))

badge_values = rucksack.find_badge_values(data)
print('part 2')
print(sum(badge_values))
