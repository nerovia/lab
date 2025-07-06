def move(a, b):
    x = a[-1] if len(a) > 0 else float('inf') 
    y = b[-1] if len(b) > 0 else float('inf')
    if x < y: b.append(a.pop())
    if x > y: a.append(b.pop())


def solve(n):
    tower = list(range(n, 0, -1))
    towers = [tower.copy(), [], []]
    while towers[2] != tower:
        move(towers[0], towers[1])
        print(towers)
        move(towers[0], towers[2])
        print(towers)
        move(towers[1], towers[2])
        print(towers)


if __name__ == '__main__':
    solve(3)
