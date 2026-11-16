import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    n = int(input_data[idx])
    idx += 1
    
    names = input_data[idx : idx + n]
    idx += n
    
    name_to_id = {name: i for i, name in enumerate(names)}
    
    skills = [int(x) for x in input_data[idx : idx + n]]
    idx += n
    
    n1 = int(input_data[idx])
    idx += 1
    
    friend_pair_of = [-1] * n
    units = [] # Each unit: (total_skill, player_count, member_ids_tuple)
    
    for _ in range(n1):
        u = name_to_id[input_data[idx]]
        v = name_to_id[input_data[idx + 1]]
        idx += 2
        friend_pair_of[u] = len(units)
        friend_pair_of[v] = len(units)
        units.append((skills[u] + skills[v], 2, (u, v)))
        
    for i in range(n):
        if friend_pair_of[i] == -1:
            friend_pair_of[i] = len(units)
            units.append((skills[i], 1, (i,)))
            
    n2 = int(input_data[idx])
    idx += 1
    
    num_units = len(units)
    rival_mask = [0] * num_units
    invalid_unit = [False] * num_units
    
    for _ in range(n2):
        u = name_to_id[input_data[idx]]
        v = name_to_id[input_data[idx + 1]]
        idx += 2
        unit_u = friend_pair_of[u]
        unit_v = friend_pair_of[v]
        if unit_u == unit_v:
            # Both members of a friend pair are rivals; unit can never be picked
            invalid_unit[unit_u] = True
        else:
            rival_mask[unit_u] |= (1 << unit_v)
            rival_mask[unit_v] |= (1 << unit_u)
            
    limit = int(input_data[idx])
    
    # Filter out invalid units and remap indices
    valid_indices = [i for i in range(num_units) if not invalid_unit[i]]
    # Sort units by skill ascending (and count descending) for better pruning
    valid_indices.sort(key=lambda i: (units[i][0] / units[i][1], -units[i][1]))
    
    old_to_new = {old: new for new, old in enumerate(valid_indices)}
    m = len(valid_indices)
    
    u_skill = [units[i][0] for i in valid_indices]
    u_count = [units[i][1] for i in valid_indices]
    u_rivals = [0] * m
    
    for new_i, old_i in enumerate(valid_indices):
        mask = 0
        for old_j in range(num_units):
            if (rival_mask[old_i] & (1 << old_j)) and old_j in old_to_new:
                mask |= (1 << old_to_new[old_j])
        u_rivals[new_i] = mask

    # Suffix sum of player counts for upper-bound pruning
    suffix_players = [0] * (m + 1)
    for i in range(m - 1, -1, -1):
        suffix_players[i] = suffix_players[i + 1] + u_count[i]

    best_players = 0

    def backtrack(pos, chosen_mask, cur_skill, cur_players):
        nonlocal best_players
        if cur_players > best_players:
            best_players = cur_players
        
        if pos == m:
            return
        
        # Pruning: even taking all remaining units won't beat best_players
        if cur_players + suffix_players[pos] <= best_players:
            return
        
        # Option 1: Include unit at `pos` if within skill limit and no rival conflict
        if cur_skill + u_skill[pos] <= limit and not (chosen_mask & u_rivals[pos]):
            backtrack(
                pos + 1,
                chosen_mask | (1 << pos),
                cur_skill + u_skill[pos],
                cur_players + u_count[pos]
            )
            
        # Option 2: Skip unit at `pos`
        backtrack(pos + 1, chosen_mask, cur_skill, cur_players)

    backtrack(0, 0, 0, 0)
    print(best_players)

if __name__ == '__main__':
    solve()