import pulp

def solver():
    # A LP problem
    prob = pulp.LpProblem("exersice1", pulp.LpMaximize)
   
    # Variables
    x1 = pulp.LpVariable("x1", None, None)
    x2 = pulp.LpVariable("x2", 0, None)
    x3 = pulp.LpVariable("x3", 0, None)
    x4 = pulp.LpVariable("x4", 0, None)
    x5 = pulp.LpVariable("x5", 0, None)

    # Objective
    prob += 3*x1 + 11*x2 + 9*x3 - x4 - 29*x5, "obj"

    # Constraints
    prob += x2 + x3 + x4 - 2*x5 <= 4,  "c1"
    prob += x1 - x2 + x3 + 2*x4 + x5 >= 0, "c2"
    prob += x1 + x2 + x3 - 3*x5 <= 1, "c3"
    
    # solve the problem using the default solver
    prob.solve()

    # print the status of the solved LP
    print("Status:", pulp.LpStatus[prob.status])

    # print the value of the objective
    print("objective =", pulp.value(prob.objective))

    # print the value of the variables at the optimum
    for v in prob.variables():
        print(f'{v.name} = {v.varValue:5.2f}')

    print()
    print("Sensitivity Analysis\nConstraint\t\t\t  Shadow Price\t\tSlack")
    for name, c in prob.constraints.items():
        print(f'{name} : {c}     \t{c.pi} \t\t{c.slack}')

if __name__ == "__main__":
    solver()

