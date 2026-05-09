from pysat.solvers import Glucose4

total_variables = 0

def generate_variables(n):
    return [[n*i+j+1 for j in range(n)] for i in range(n)]

def generate_seq_variables(end,size):
    return [x for x in range(end,end+size-1)]



def at_most_one(clauses,variables):
    global total_variables
    seq_variables = generate_seq_variables(total_variables,len(variables))
    total_variables += len(seq_variables)

    assert len(variables) <= n, "The number of variables should not exceed n for sequential encoding."
    
    """
    Activate: 1 <= i <= n-1, not x[i] or s[i] 
    Propagate: 2 <= i <= n-1, not s[i-1] or s[i]
    Forbid second TRUE: 2 <= i <= n, not s[i-1] or not x[i]

    Notes: All indexs in this comment are 1-based index
    """
    
    # Activate
    for i in range(len(variables)-1):
        clauses.append([-variables[i],seq_variables[i]])

    
    # Propagate
    for i in range(1,len(variables)-1):
        clauses.append([-seq_variables[i-1],seq_variables[i]])

    # Forbid second TRUE
    for i in range(1,len(variables)):
        clauses.append([-seq_variables[i-1], -variables[i]])



def exactly_one(clauses,variables):
    clauses.append(variables)
    at_most_one(clauses,variables)

def generate_clauses(n):
    global total_variables
    clauses = []
    variables = generate_variables(n)
    total_variables += len(variables)*len(variables[0])
    
    # Exactly one queen in a row
    for row in range(n):
        exactly_one(clauses, variables[row])
    
    # Exactly one queen in a column 
    for col in range(n):
        exactly_one(clauses,[variables[row][col] for row in range(n)])
    
    # At most one queen in each diagonal
    # Main diagonals
    for d in range(2*n - 1):
        diag = [variables[i][j] for i in range(n) for j in range(n) if i - j == d - n + 1]
        at_most_one(clauses, diag)
    
    # Anti-diagonals
    for d in range(2*n - 1):
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
        solution = [[0]*n for _ in range(n)]
        for var in model:
            if var > 0 and var <= n*n:
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

n = 8
solution = solve_n_queens(n)
print_solution(solution)

