import math

from pysat.solvers import Glucose4


def generate_variables(n):
    return [[n * i + j + 1 for j in range(n)] for i in range(n)]


def at_most_one(clauses, variables):
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])


def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)


def generate_clauses(n):
    clauses = []
    variables = generate_variables(n)

    # print(variables)

    # Exactly one queen in a row
    for row in range(n):
        exactly_one(clauses, variables[row])

    # Exactly one queen in a column
    for col in range(n):
        exactly_one(clauses, [variables[row][col] for row in range(n)])

    # Exactly at most queen in every diagonal
    for i in range(n):
        for j in range(n):
            major_diag = []
            minor_diag = []
            for k in range(n):

                x1_diag = i + k
                y1_diag = j + k
                if (x1_diag < n) and (y1_diag < n):
                    major_diag.append(variables[x1_diag][y1_diag])

                x2_diag = i + k
                y2_diag = j - k
                if (x2_diag < n) and (y2_diag >= 0):
                    minor_diag.append(variables[x2_diag][y2_diag])

            if len(major_diag) > 1:
                at_most_one(clauses, major_diag)
            if len(minor_diag) > 1:
                at_most_one(clauses, minor_diag)

    return clauses


def decode_coordinate(val):
    val = abs(val) - 1
    x = val // n
    y = val % n
    return [x, y]


def debug_clauses(clauses):
    for clause in clauses:
        A_coordinate = decode_coordinate(clause[0])
        B_coordinate = decode_coordinate(clause[1])
        print(
            "-X[{},{}] V -X[{},{}]".format(
                A_coordinate[0], A_coordinate[1], B_coordinate[0], B_coordinate[1]
            )
        )


def solve_n_queens(n):
    solver = Glucose4()

    clauses = generate_clauses(n)
    # debug_clauses(clauses)
    assert len(clauses) > 0
    for clause in clauses:
        solver.add_clause(clause)

    is_sat = solver.solve()

    if is_sat:
        solution = solver.get_model()
        print(solution)
        return [[int(solution[n * x + y] > 0) for y in range(n)] for x in range(n)]
    else:
        return None


def print_result(solution):
    if solution is None:
        print("No solution found")
    else:
        print("Found a solution:")
        mapping = {1: "Q", 0: "."}
        mapped = [[mapping[x] for x in row] for row in solution]
        for row in mapped:
            print(*row)


n = 4
solution = solve_n_queens(n)
print_result(solution)
