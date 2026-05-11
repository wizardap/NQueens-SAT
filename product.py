from pysat.solvers import Glucose4
import math

total_variables = 0


def get_bit(mask, pos):
    return (mask >> pos) & 1


def generate_variables(n):
    return [[n * i + j + 1 for j in range(n)] for i in range(n)]


def generate_binary_variables(end, length):
    return [x for x in range(end, end + math.ceil(math.log2(length)))]


def split_variables(end, variables_length):
    p = math.ceil(math.sqrt(variables_length))

    # Can't use: (variables_length // p) because we need p * q >= variables_length
    # and  (variables_length // p <= sqrt(variables_length)). I use my own ceil
    # q = (variables_length + p - 1) // p
    q = math.ceil(variables_length / p)
    u = [x for x in range(end, end + p)]
    v = [x for x in range(end + p, end + p + q)]
    return u, v


def binary_encoding(clauses, target, bit_variables):
    for bit_val in bit_variables:
        clauses.append([-target, bit_val])


def naive_AMO(clauses, variables):
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])


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


def at_most_one(clauses, variables):
    global total_variables

    if len(variables) <= 10:
        naive_AMO(clauses, variables)
        return

    u, v = split_variables(total_variables, len(variables))
    total_variables += len(u) + len(v)

    binary_AMO(clauses, u)
    binary_AMO(clauses, v)

    p_len = len(u)
    q_len = len(v)
    n_len = len(variables)

    # product
    n_count = 0
    for j in range(q_len):
        for i in range(p_len):
            clauses.append([-variables[n_count], u[i]])
            clauses.append([-variables[n_count], v[j]])
            n_count += 1
            if n_count == n_len:
                break
        if n_count == n_len:
            break


def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)


def generate_clauses(n):
    global total_variables
    variables = generate_variables(n)
    total_variables += n * n

    clauses = []

    # Exactly one queen in each row
    for row in range(n):
        exactly_one(clauses, variables[row])

    # Exactly one queen in each column
    for col in range(n):
        exactly_one(clauses, [variables[row][col] for row in range(n)])

    # At most one queen in each diagonal
    # Main diagonals
    for d in range(2 * n - 1):
        diag = [
            variables[i][j] for i in range(n) for j in range(n) if (i - j == d - n + 1)
        ]
        at_most_one(clauses, diag)

    # Anti-diagonals
    for d in range(2 * n - 1):
        diag = [variables[i][j] for i in range(n) for j in range(n) if i + j == d]
        at_most_one(clauses, diag)

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


n = 512

solution = solve_n_queens(n)
# print_solution(solution)

if check_valid(solution):
    print("Solution is valid.")
else:
    print("Solution is invalid.")
