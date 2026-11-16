import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    E = int(input_data[0])
    idx = 1
    
    init_edges = []
    nodes = set()
    for _ in range(E):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        idx += 2
        init_edges.append((min(u, v), max(u, v)))
        nodes.add(u)
        nodes.add(v)
        
    target_edges = []
    for _ in range(E):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        idx += 2
        target_edges.append((min(u, v), max(u, v)))
        
    start_state = tuple(sorted(init_edges))
    goal_state = tuple(sorted(target_edges))
    
    if start_state == goal_state:
        print(0)
        return

    # Build adjacency list to find all simple cycles in the graph structure
    adj = {u: [] for u in nodes}
    for u, v in start_state:
        adj[u].append(v)
        adj[v].append(u)

    # Find all unique simple cycles (length >= 3)
    cycles = set()
    
    def find_cycles(start_node, curr_node, path, visited):
        for neighbor in adj[curr_node]:
            if neighbor == start_node and len(path) >= 3:
                # Normalize cycle representation to avoid duplicates
                min_idx = path.index(min(path))
                norm_path = path[min_idx:] + path[:min_idx]
                rev_path = [norm_path[0]] + norm_path[1:][::-1]
                canonical = min(tuple(norm_path), tuple(rev_path))
                cycles.add(canonical)
            elif neighbor not in visited and neighbor > start_node:
                visited.add(neighbor)
                path.append(neighbor)
                find_cycles(start_node, neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)

    for node in sorted(nodes):
        find_cycles(node, node, [node], {node})

    # Convert each undirected cycle into both clockwise and counter-clockwise permutations
    permutations = []
    for c in cycles:
        k = len(c)
        # Forward shift: c[i] moves to c[(i + 1) % k]
        fwd = {c[i]: c[(i + 1) % k] for i in range(k)}
        permutations.append(fwd)
        # Backward shift: c[i] moves to c[(i - 1) % k]
        bwd = {c[i]: c[(i - 1) % k] for i in range(k)}
        permutations.append(bwd)

    # BFS to find the minimum number of rotations
    queue = deque([(start_state, 0)])
    visited_states = {start_state}

    while queue:
        curr_edges, steps = queue.popleft()
        
        for perm in permutations:
            # Apply permutation to current edges
            next_edges = []
            for u, v in curr_edges:
                nu = perm.get(u, u)
                nv = perm.get(v, v)
                next_edges.append((min(nu, nv), max(nu, nv)))
            
            next_state = tuple(sorted(next_edges))
            
            if next_state == goal_state:
                print(steps + 1)
                return
                
            if next_state not in visited_states:
                visited_states.add(next_state)
                queue.append((next_state, steps + 1))

    print(-1)

if _name_ == '_main_':
    solve()