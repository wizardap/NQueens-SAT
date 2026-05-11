"""
Commander encoding. 
Please read the paper from https://www.cs.cmu.edu/~wklieber/papers/2007_efficient-cnf-encoding-for-selecting-1.pdf
"""

from pysat.solvers import Glucose4
import math
total_variables = 0

def generate_variables(n):
    return [[i*n + j + 1 for j in range(n)] for i in range(n)]

def generate_commander_variables(end, length):
    return [x for x in range(end,end+length)]

def grouping_variables(a):
    """
    Round-robin split
    """
    k = len(a)//group_size
    r = [[] for _ in range(k)]
    for i, x in enumerate(a):
        r[i % k].append(x)
    return r

def naive_AMO(clauses, variables):
    for i in range(len(variables)):
        for j in range(i+1,len(variables)):
            clauses.append([-variables[i],-variables[j]])

def naive_EO(clauses, variables):
    clauses.append(variables)
    naive_AMO(clauses,variables)

def cmdr_AMO(clauses,variables):
    global total_variables
    if (len(variables) <= group_size):
        naive_AMO(clauses,variables)
        return

    groups = grouping_variables(variables)
    commander_variables = generate_commander_variables(total_variables, len(groups))
    total_variables+=len(groups)
    
    
    for idx,group in enumerate(groups):

        # 1. At most one variable in group can be true
        naive_AMO(clauses,group)

        # 2. If the commander variable of a group is true, then at least one of the variables in the group must be true. 
        # clauses.append([-commander_variables[idx]]+group)
        # in AMO, we don't have this constraint

        # 3. If the commander variable of a group is false, then none of the variables in the group can be true
        for x in group:
            clauses.append([commander_variables[idx],-x])
        
    # 4. Exactly one of the commander variables is true
    cmdr_AMO(clauses,commander_variables)


def cmdr_EO(clauses, variables):
    global total_variables

    if (len(variables) <= group_size ):
        naive_EO(clauses,variables)
        return

    groups = grouping_variables(variables)
    commander_variables = generate_commander_variables(total_variables, len(groups))
    total_variables+=len(groups)

    
    
    for idx,group in enumerate(groups):

        # 1. At most one variable in group can be true
        naive_AMO(clauses,group)

        # 2. If the commander variable of a group is true, then at least one of the variables in the group must be true. 
        clauses.append([-commander_variables[idx]]+group)

        # 3. If the commander variable of a group is false, then none of the variables in the group can be true
        for x in group:
            clauses.append([commander_variables[idx],-x])
        
    # 4. Exactly one of the commander variables is true
    cmdr_EO(clauses,commander_variables)

    

def generate_clauses(n):
    global total_variables
    variables = generate_variables(n)
    total_variables+=n*n

    clauses = []
    
    # Exactly one queen in each row
    for row in range(n):
        cmdr_EO(clauses,variables[row])

    # Exactly one queen in each column
    for col in range(n):
        cmdr_EO(clauses,[variables[row][col] for row in range(n)])

    # At most one queen in each diagonal
    # Main diagonals
    for d in range(2*n - 1):
        diag = [variables[i][j] for i in range(n) for j in range(n) if i - j == d - n + 1]
        cmdr_AMO(clauses, diag)
    
    # Anti-diagonals
    for d in range(2*n - 1):
        diag = [variables[i][j] for i in range(n) for j in range(n) if i + j == d]
        cmdr_AMO(clauses, diag)

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
 

def check_valid(solution):
    if (solution is None):
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
                    if i + k < n and j + k < n and solution[i+k][j+k] == 1:
                        print("Main diagonal conflict:", i, j, i+k, j+k)
                        return False
                    if i - k >= 0 and j - k >= 0 and solution[i-k][j-k] == 1:
                        print("Main diagonal conflict:", i, j, i-k, j-k)
                        return False
                # check anti-diagonal
                for k in range(1, n):
                    if i + k < n and j - k >= 0 and solution[i+k][j-k] == 1:
                        print("Anti-diagonal conflict:", i, j, i+k, j-k)
                        return False
                    if i - k >= 0 and j + k < n and solution[i-k][j+k] == 1:
                        print("Anti-diagonal conflict:", i, j, i-k, j+k)
                        return False
    return True

n=1000
group_size=int(math.ceil(math.sqrt(n)))

solution = solve_n_queens(n)
# print_solution(solution)

if check_valid(solution):
    print("Solution is valid.")
else:
    print("Solution is invalid.")
