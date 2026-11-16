import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx])
    M = int(input_data[idx + 1])
    idx += 2
    
    grid = []
    for _ in range(N):
        row = [int(x) for x in input_data[idx:idx + M]]
        grid.append(row)
        idx += M
        
    # Convert 1-based indexing to 0-based indexing
    sr, sc = int(input_data[idx]) - 1, int(input_data[idx + 1]) - 1
    idx += 2
    dr, dc = int(input_data[idx]) - 1, int(input_data[idx + 1]) - 1
    idx += 2
    
    K = int(input_data[idx])
    idx += 1
    
    blocked = set()
    for _ in range(K):
        br, bc = int(input_data[idx]) - 1, int(input_data[idx + 1]) - 1
        blocked.add((br, bc))
        idx += 2
        
    # 8 possible movement directions
    dirs = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    # Dijkstra's Algorithm
    INF = float('inf')
    dist = [[INF] * M for _ in range(N)]
    dist[sr][sc] = 0
    pq = [(0, sr, sc)]
    
    while pq:
        d, r, c = heapq.heappop(pq)
        
        if d > dist[r][c]:
            continue
        if (r, c) == (dr, dc):
            print(d)
            return
            
        # Gather all valid unblocked 8-neighbors of current cell (r, c)
        neighbors = []
        for dr_step, dc_step in dirs:
            nr, nc = r + dr_step, c + dc_step
            if 0 <= nr < N and 0 <= nc < M and (nr, nc) not in blocked:
                neighbors.append((nr, nc))
                
        curr_val = grid[r][c]
        
        # Calculate transition cost to each valid neighbor (nr, nc)
        for nr, nc in neighbors:
            max_other = curr_val
            for or_cell, oc_cell in neighbors:
                if (or_cell, oc_cell) != (nr, nc):
                    if grid[or_cell][oc_cell] > max_other:
                        max_other = grid[or_cell][oc_cell]
                        
            required_val = max_other + 1
            step_cost = max(0, required_val - grid[nr][nc])
            
            if d + step_cost < dist[nr][nc]:
                dist[nr][nc] = d + step_cost
                heapq.heappush(pq, (dist[nr][nc], nr, nc))

if _name_ == '_main_':
    solve()