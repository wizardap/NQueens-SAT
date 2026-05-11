"""
Commander encoding.
Please read the paper from https://www.cs.cmu.edu/~wklieber/papers/2007_efficient-cnf-encoding-for-selecting-1.pdf
"""

from pysat.solvers import Glucose4
import math

total_variables = 0


def get_bit(mask, pos):
    return (mask >> pos) & 1


def generate_variables(n):
    return [[n * i + j + 1 for j in range(n)] for i in range(n)]


def generate_binary_variables(end, length):
    return [x for x in range(end, end + math.ceil(math.log2(length)))]


def binary_encoding(clauses, target, bit_variables):
    for bit_val in bit_variables:
        clauses.append([-target, bit_val])
        # print(f"-x[{target}] v {(bit_val//abs(bit_val))*(abs(bit_val)-63)}")


def binary_AMO(clauses, variables):
    global total_variables
    binary_variables = generate_binary_variables(total_variables, len(variables))
    total_variables += len(binary_variables)

    for i, val in enumerate(variables):
        bit_variables = []
        for j, binary_val in enumerate(binary_variables):
            bit = get_bit(i, j)
            if bit == 1:
                bit_variables.append(binary_val)
            else:
                bit_variables.append(-binary_val)
        binary_encoding(clauses, val, bit_variables)


def generate_commander_variables(end, length):
    return [x for x in range(end, end + length)]


def grouping_variables(variables, group_num):
    k = math.ceil(len(variables) / group_num)
    r = [[] for _ in range(k)]

    for idx, val in enumerate(variables):
        r[idx // group_num].append(val)

    return r


def naive_AMO(clauses, variables):
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])


def bcmdr_AMO(clauses, variables):
    global total_variables
    group_num = math.ceil(math.sqrt(len(variables)))

    groups = grouping_variables(variables, group_num)
    binary_variables = generate_binary_variables(total_variables, len(groups))
    total_variables += len(binary_variables)
    for group in groups:
        naive_AMO(clauses, group)

    for i in range(len(groups)):
        for h in range(len(groups[i])):
            val = groups[i][h]
            bit_variables = []
            for j, binary_val in enumerate(binary_variables):
                bit = get_bit(i, j)
                if bit == 1:
                    bit_variables.append(binary_val)
                else:
                    bit_variables.append(-binary_val)
            binary_encoding(clauses, val, bit_variables)


def bcmdr_EO(clauses, variables):
    clauses.append(variables)
    bcmdr_AMO(clauses, variables)


def generate_clauses(n):
    global total_variables
    variables = generate_variables(n)
    total_variables += n * n

    clauses = []

    # Exactly one queen in each row
    for row in range(n):
        bcmdr_EO(clauses, variables[row])
        # exit(0)

    # Exactly one queen in each column
    for col in range(n):
        bcmdr_EO(clauses, [variables[row][col] for row in range(n)])

    # At most one queen in each diagonal
    # Main diagonals
    for d in range(2 * n - 1):
        diag = [
            variables[i][j] for i in range(n) for j in range(n) if i - j == d - n + 1
        ]
        bcmdr_AMO(clauses, diag)

    # Anti-diagonals
    for d in range(2 * n - 1):
        diag = [variables[i][j] for i in range(n) for j in range(n) if i + j == d]
        bcmdr_AMO(clauses, diag)

    return clauses


def solve_n_queens(n):
    global total_variables
    clauses = generate_clauses(n)
    solver = Glucose4()
    solver.append_formula(clauses)

    if solver.solve():
        model = solver.get_model()
        solution = [[0] * n for _ in range(n)]
        for var in model:
            if var > 0 and var <= n * n:
                row = (var - 1) // n
                col = (var - 1) % n
                solution[row][col] = 1
        return solution
    else:
        return None


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell == 1 else "." for cell in row))


def check_valid(solution):
    if solution is None:
        print("No solution found.")
        return False

    n = len(solution)
    # check row
    for i in range(n):
        if solution[i].count(1) != 1:
            print("Row conflict:", i)
            return False
    # check column
    for j in range(n):
        if [solution[i][j] for i in range(n)].count(1) != 1:
            print("Column conflict:", j)
            return False
    # check diagonal
    for i in range(n):
        for j in range(n):
            if solution[i][j] == 1:
                # check main diagonal
                for k in range(1, n):
                    if i + k < n and j + k < n and solution[i + k][j + k] == 1:
                        print("Main diagonal conflict:", i, j, i + k, j + k)
                        return False
                    if i - k >= 0 and j - k >= 0 and solution[i - k][j - k] == 1:
                        print("Main diagonal conflict:", i, j, i - k, j - k)
                        return False
                # check anti-diagonal
                for k in range(1, n):
                    if i + k < n and j - k >= 0 and solution[i + k][j - k] == 1:
                        print("Anti-diagonal conflict:", i, j, i + k, j - k)
                        return False
                    if i - k >= 0 and j + k < n and solution[i - k][j + k] == 1:
                        print("Anti-diagonal conflict:", i, j, i - k, j + k)
                        return False
    return True


n = 91

solution = solve_n_queens(n)
# print_solution(solution)

if check_valid(solution):
    print("Solution is valid.")
else:
    print("Solution is invalid.")
