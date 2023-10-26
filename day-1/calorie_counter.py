with open("data.txt", "r") as fhandle:
    data = fhandle.readlines()

elf_calories = [[]]
for raw_line in data:
    line = raw_line.strip()  # remove \n
    if line != "":
        elf_calories[-1].append(int(line))
    else:
        elf_calories.append([])

# inline replacement of list to sum of calories
for i, elf in enumerate(elf_calories):
    elf_calories[i] = sum(elf_calories[i])


# output target of exercise part 1
max_calories = max(elf_calories)
print("answer part 1")
print(max_calories)

print("answer part 2")
sorted_elf_calories = sorted(elf_calories)
print(sum(sorted_elf_calories[-3:]))
