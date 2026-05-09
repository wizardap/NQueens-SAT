

total_variables = 0
def generate_variables(n):
    return [[i*n + j + 1 for j in range(n)] for i in range(n)]

def generate_commander_variables(end, length):
    return [x for x in range(end,end+length-1)]

def split(a, k):
    """
    Round-robin split
    """
    r = [[] for _ in range(k)]
    for i, x in enumerate(a):
        r[i % k].append(x)
    return r


def at_most_one(clauses,variables,groups_size=3,level=1):
    """
    Commander encoding

    Link original variable to commander variables: (x \in group Ai)
    """
    if (level == 0):
        return
    command_arr = split(variables,groups_size)
    temp_variables = generate_commander_variables(total_variables,len(command_arr))
    



    

def exactly_one(clauses,variables,groups_size = 3, level=1):
    clauses.append(variables)
    at_most_one(clauses,variables,groups_size,level)

def generate_clauses(n):
    global total_variables
    variables = generate_variables(n)
    total_variables+=n*n

    

    pass

def solve_n_queens(n):
    pass

def print_solution(solution):
    for row in solution:
        print(" ".join("Q" if cell == 1 else "." for cell in row))

