
def at_most_one(clauses, variables):
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])

def exactly_one(clauses, variables):
    clauses.append(variables)
    at_most_one(clauses, variables)


