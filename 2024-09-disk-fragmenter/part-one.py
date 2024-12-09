with open("2024-09-disk-fragmenter/input.txt", "r") as file:
    input = [int(x) for x in next(file).strip()]

files, spaces = list(enumerate(input[::2])), input[1::2]
result = []
while files:
    if not files[0][1] and not spaces[0]:
        files, spaces = files[1:], spaces[1:]
        continue

    if files[0][1]:
        result.append(files[0])
        files[0] = (files[0][0], 0)
    else:
        taken = min(spaces[0], files[-1][1])
        spaces[0] -= taken
        files[-1] = (files[-1][0], files[-1][1] - taken)
        result.append((files[-1][0], taken))
        if files[-1][1] == 0:
            files.pop()


i, checksum = 0, 0
for file_id, l in result:
    checksum += file_id * (i + i + l - 1) * l // 2
    i += l


print(checksum)
