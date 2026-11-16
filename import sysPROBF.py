import sys

def solve():
    # Read all non-empty lines while preserving exact leading/trailing spaces
    lines = [line.rstrip('\r\n') for line in sys.stdin.readlines() if line.strip('\r\n') != '']
    if len(lines) < 9:
        return

    def extract_patterns(three_lines):
        # Ensure all 3 lines have the same length, padded with spaces to a multiple of 3
        max_len = max(len(l) for l in three_lines)
        if max_len % 3 != 0:
            max_len += 3 - (max_len % 3)
        padded = [l.ljust(max_len) for l in three_lines]
        
        patterns = []
        for col in range(0, max_len, 3):
            bits = []
            for row in range(3):
                for c in range(col, col + 3):
                    bits.append('0' if padded[row][c] == ' ' else '1')
            patterns.append("".join(bits))
        return patterns

    # 1. Map digits 0-9
    digit_patterns = extract_patterns(lines[0:3])
    bin_to_digit = {}
    digit_to_bin = {}
    for d in range(10):
        pat = digit_patterns[d]
        bin_to_digit[pat] = str(d)
        digit_to_bin[str(d)] = pat

    # 2. Map operators and brackets: OR, AND, NOT, (, )
    op_patterns = extract_patterns(lines[3:6])
    op_names = ['OR', 'AND', 'NOT', '(', ')']
    pat_to_token = {}
    for idx, name in enumerate(op_names):
        pat_to_token[op_patterns[idx]] = name

    # 3. Parse the expression (lines 6-8)
    expr_patterns = extract_patterns(lines[6:9])
    tokens = []
    current_num_bits = []

    for pat in expr_patterns:
        if pat in pat_to_token:
            if current_num_bits:
                tokens.append("".join(current_num_bits))
                current_num_bits = []
            tokens.append(pat_to_token[pat])
        elif pat in bin_to_digit:
            current_num_bits.append(pat)

    if current_num_bits:
        tokens.append("".join(current_num_bits))

    # Bitwise helper functions on binary strings
    def op_not(a):
        return "".join('1' if ch == '0' else '0' for ch in a)

    def op_or(a, b):
        length = max(len(a), len(b))
        a = a.zfill(length)
        b = b.zfill(length)
        return "".join('1' if a[i] == '1' or b[i] == '1' else '0' for i in range(length))

    def op_and(a, b):
        length = max(len(a), len(b))
        a = a.zfill(length)
        b = b.zfill(length)
        return "".join('1' if a[i] == '1' and b[i] == '1' else '0' for i in range(length))

    # 4. Recursive Descent Parser matching custom precedence:
    # Lowest: AND -> OR -> NOT -> Brackets/Operands (Highest)
    pos = 0

    def parse_and():
        nonlocal pos
        left = parse_or()
        while pos < len(tokens) and tokens[pos] == 'AND':
            pos += 1
            right = parse_or()
            left = op_and(left, right)
        return left

    def parse_or():
        nonlocal pos
        left = parse_not()
        while pos < len(tokens) and tokens[pos] == 'OR':
            pos += 1
            right = parse_not()
            left = op_or(left, right)
        return left

    def parse_not():
        nonlocal pos
        if pos < len(tokens) and tokens[pos] == 'NOT':
            pos += 1
            return op_not(parse_not())
        return parse_primary()

    def parse_primary():
        nonlocal pos
        tok = tokens[pos]
        if tok == '(':
            pos += 1
            val = parse_and()
            if pos < len(tokens) and tokens[pos] == ')':
                pos += 1
            return val
        else:
            pos += 1
            return tok

    result_bits = parse_and()

    # 5. Convert resulting binary string back to decimal digits
    # Pad with leading zeros if length isn't a multiple of 9
    if len(result_bits) % 9 != 0:
        result_bits = result_bits.zfill(len(result_bits) + (9 - len(result_bits) % 9))

    ans_digits = []
    for i in range(0, len(result_bits), 9):
        chunk = result_bits[i:i+9]
        ans_digits.append(bin_to_digit.get(chunk, '0'))

    # Print as integer to strip any leading zeros (e.g., "05" -> 5)
    print(int("".join(ans_digits)))

if _name_ == '_main_':
    solve()import sys

def solve():
    # Read all non-empty lines while preserving exact leading/trailing spaces
    lines = [line.rstrip('\r\n') for line in sys.stdin.readlines() if line.strip('\r\n') != '']
    if len(lines) < 9:
        return

    def extract_patterns(three_lines):
        # Ensure all 3 lines have the same length, padded with spaces to a multiple of 3
        max_len = max(len(l) for l in three_lines)
        if max_len % 3 != 0:
            max_len += 3 - (max_len % 3)
        padded = [l.ljust(max_len) for l in three_lines]
        
        patterns = []
        for col in range(0, max_len, 3):
            bits = []
            for row in range(3):
                for c in range(col, col + 3):
                    bits.append('0' if padded[row][c] == ' ' else '1')
            patterns.append("".join(bits))
        return patterns

    # 1. Map digits 0-9
    digit_patterns = extract_patterns(lines[0:3])
    bin_to_digit = {}
    digit_to_bin = {}
    for d in range(10):
        pat = digit_patterns[d]
        bin_to_digit[pat] = str(d)
        digit_to_bin[str(d)] = pat

    # 2. Map operators and brackets: OR, AND, NOT, (, )
    op_patterns = extract_patterns(lines[3:6])
    op_names = ['OR', 'AND', 'NOT', '(', ')']
    pat_to_token = {}
    for idx, name in enumerate(op_names):
        pat_to_token[op_patterns[idx]] = name

    # 3. Parse the expression (lines 6-8)
    expr_patterns = extract_patterns(lines[6:9])
    tokens = []
    current_num_bits = []

    for pat in expr_patterns:
        if pat in pat_to_token:
            if current_num_bits:
                tokens.append("".join(current_num_bits))
                current_num_bits = []
            tokens.append(pat_to_token[pat])
        elif pat in bin_to_digit:
            current_num_bits.append(pat)

    if current_num_bits:
        tokens.append("".join(current_num_bits))

    # Bitwise helper functions on binary strings
    def op_not(a):
        return "".join('1' if ch == '0' else '0' for ch in a)

    def op_or(a, b):
        length = max(len(a), len(b))
        a = a.zfill(length)
        b = b.zfill(length)
        return "".join('1' if a[i] == '1' or b[i] == '1' else '0' for i in range(length))

    def op_and(a, b):
        length = max(len(a), len(b))
        a = a.zfill(length)
        b = b.zfill(length)
        return "".join('1' if a[i] == '1' and b[i] == '1' else '0' for i in range(length))

    # 4. Recursive Descent Parser matching custom precedence:
    # Lowest: AND -> OR -> NOT -> Brackets/Operands (Highest)
    pos = 0

    def parse_and():
        nonlocal pos
        left = parse_or()
        while pos < len(tokens) and tokens[pos] == 'AND':
            pos += 1
            right = parse_or()
            left = op_and(left, right)
        return left

    def parse_or():
        nonlocal pos
        left = parse_not()
        while pos < len(tokens) and tokens[pos] == 'OR':
            pos += 1
            right = parse_not()
            left = op_or(left, right)
        return