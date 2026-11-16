def solve():
    n, m = map(int, input().split())

    grid = []
    for _ in range(n):
        row = input().replace(" ", "").strip()
        grid.append(row)

    horizontal = {}
    vertical = {}

    for i in range(n):
        for j in range(m):

            if grid[i][j] == '.':
                continue

            left = j > 0 and grid[i][j-1] != '.'
            right = j < m-1 and grid[i][j+1] != '.'
            up = i > 0 and grid[i-1][j] != '.'
            down = i < n-1 and grid[i+1][j] != '.'

            # Check whether this cell is an intersection
            if (left or right) and (up or down):

                h = int(left) + int(right)
                v = int(up) + int(down)

                # Determine the rod direction
                hr = 0
                vr = 0

                if left:
                    hr += grid[i][j-1] == 'R'
                if right:
                    hr += grid[i][j+1] == 'R'
                if up:
                    vr += grid[i-1][j] == 'R'
                if down:
                    vr += grid[i+1][j] == 'R'

                if hr >= vr:
                    key = ('H', i)
                else:
                    key = ('V', j)

                if key not in horizontal:
                    horizontal[key] = [0, 0]

                if grid[i][j] == 'R':
                    horizontal[key][0] += 1
                else:
                    horizontal[key][1] += 1

    answer = 0

    for r, c in horizontal.values():
        answer += min(r, c)

    print(answer)


if __name__ == "__main__":
    solve()