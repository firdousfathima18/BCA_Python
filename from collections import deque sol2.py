from collections import deque
import sys


def solve():
  input_data = [
      line.strip() for line in sys.stdin.read().splitlines() if line.strip()
  ]
  if not input_data:
    return

  # Read grid dimensions M and N
  first_line = input_data[0].split()
  M, N = int(first_line[0]), int(first_line[1])

  # Read the grid (supports both space-separated and contiguous characters)
  grid = []
  for i in range(1, M + 1):
    if ' ' in input_data[i]:
      grid.append(input_data[i].split())
    else:
      grid.append(list(input_data[i]))

  src_cells = []
  dst_cells = []

  for r in range(M):
    for c in range(N):
      if grid[r][c] == 'I':
        src_cells.append((r, c))
      elif grid[r][c] == 'L':
        dst_cells.append((r, c))

  if not src_cells or not dst_cells:
    print('Impossible')
    return

  src_cells.sort()
  dst_cells.sort()
  K = len(src_cells)

  # State format: (top_left_r, top_left_c, orientation)
  # orientation: 0 = Horizontal, 1 = Vertical
  src_orient = 0 if src_cells[0][0] == src_cells[-1][0] else 1
  dst_orient = 0 if dst_cells[0][0] == dst_cells[-1][0] else 1

  start_state = (src_cells[0][0], src_cells[0][1], src_orient)
  target_state = (dst_cells[0][0], dst_cells[0][1], dst_orient)

  if start_state == target_state:
    print(0)
    return

  def is_valid_ladder(r, c, orient):
    if orient == 0:  # Horizontal
      if r < 0 or r >= M or c < 0 or c + K > N:
        return False
      for dc in range(K):
        if grid[r][c + dc] == 'B':
          return False
    else:  # Vertical
      if r < 0 or r + K > M or c < 0 or c >= N:
        return False
      for dr in range(K):
        if grid[r + dr][c] == 'B':
          return False
    return True

  def is_square_free(sq_r, sq_c):
    if sq_r < 0 or sq_r + K > M or sq_c < 0 or sq_c + K > N:
      return False
    for dr in range(K):
      for dc in range(K):
        if grid[sq_r + dr][sq_c + dc] == 'B':
          return False
    return True

  queue = deque([(start_state[0], start_state[1], start_state[2], 0)])
  visited = {start_state}

  while queue:
    r, c, orient, steps = queue.popleft()

    # 1. Move 1 cell in 4 directions (Up, Down, Left, Right)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      nr, nc = r + dr, c + dc
      next_state = (nr, nc, orient)
      if next_state not in visited and is_valid_ladder(nr, nc, orient):
        if next_state == target_state:
          print(steps + 1)
          return
        visited.add(next_state)
        queue.append((nr, nc, orient, steps + 1))

    # 2. Rotate 90 degrees within a completely empty K x K square area
    if orient == 0:  # Horizontal -> Vertical
      for sq_r in (r - K + 1, r):
        if is_square_free(sq_r, c):
          for nc in range(c, c + K):
            next_state = (sq_r, nc, 1)
            if next_state not in visited:
              if next_state == target_state:
                print(steps + 1)
                return
              visited.add(next_state)
              queue.append((sq_r, nc, 1, steps + 1))
    else:  # Vertical -> Horizontal
      for sq_c in (c - K + 1, c):
        if is_square_free(r, sq_c):
          for nr in range(r, r + K):
            next_state = (nr, sq_c, 0)
            if next_state not in visited:
              if next_state == target_state:
                print(steps + 1)
                return
              visited.add(next_state)
              queue.append((nr, sq_c, 0, steps + 1))

  print('Impossible')


if __name__ == '__main__':
  solve()