with open("2024-22-monkey-market/input.txt", "r") as f:
    numbers = [int(line.strip()) for line in f]


def prune(x):
    return x % 16777216


def mix(secret, other):
    return secret ^ other


def next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret


def skip_steps(numbers, steps):
    for n in numbers:
        s = n
        for _ in range(steps):
            s = next_secret(s)
        yield s


print(sum(skip_steps(numbers, 2000)))
