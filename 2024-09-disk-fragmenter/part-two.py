with open("2024-09-disk-fragmenter/input.txt", "r") as file:
    input = [int(x) for x in next(file).strip()]

files, spaces = list(enumerate(input[::2])), input[1::2]

result = sum(([i // 2 if i % 2 == 0 else -1] * val for i, val in enumerate(input)), [])
end = len(result)
for i in range(len(result) - 1, -1, -1):
    if i == 0 or result[i - 1] != result[i]:
        if result[i] != -1:
            for start in range(i):
                if result[start] != -1:
                    continue
                if all(x == -1 for x in result[start : start + end - i]):
                    result[start : start + end - i] = [result[i]] * (end - i)
                    result[i:end] = [-1] * (end - i)
                    break
        end = i

# print("".join({**{i: str(i) for i in range(10)}, -1: "."}[x] for x in result))
print(sum(i * x for i, x in enumerate(result) if x != -1))
