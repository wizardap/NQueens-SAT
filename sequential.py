
def generate_variables(n):
    return [[n*i+j+1 for j in range(n)] for i in range(n)]

def generate_seq_variables(n):
    return [n*n+x for x in range(n-1)]


def at_most_one(clauses,variables):
    pass

def exactly_one(clauses,variables):
    clauses.append(variables)
    at_most_one(clauses,variables)

def generate_clauses(n):
    clauses = []
    variables = generate_variables(n)
    seq_variables = generate_seq_variables(n)
    
    # Exactly one queen in a row
    for row in variables:
        exactly_one(clauses,row)
    
    # Exactly one queen in a column 
    

def solve_n_queens(n):
    pass


