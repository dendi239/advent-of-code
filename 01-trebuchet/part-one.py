with open("01-trebuchet/input.txt") as f:
    print(sum(
        int(d[0] + d[-1])
        for line in f
        if len((d := [c for c in line if c.isdigit()])) >= 1
    ))
