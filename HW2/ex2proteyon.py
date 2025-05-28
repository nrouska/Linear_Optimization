import pulp

def solver():
    # A LP problem
    prob = pulp.LpProblem("exersice1d", pulp.LpMinimize)

    # Variables
    x1 = pulp.LpVariable("x1", None, 0)
    x2 = pulp.LpVariable("x2", 0, None)
    x3 = pulp.LpVariable("x3", None, None)
    x4 = pulp.LpVariable("x4", 0, None)
   
    # Objective
    prob += x1 + x2 , "obj"

    # Constraints
    prob += 2*x1 + 3*x2 + x3 + x4 <= 0,  "c1"
    prob += -1*x1 + x2 +2*x3 +x4 ==6 , "c2"
    prob += 3*x1 + x2 +4 *x3 + 2*x4>=3, "c3"
   
  
    
    # solve the problem using the default solver
    prob.solve()

    # print the status of the solved LP
    print("Status:", pulp.LpStatus[prob.status])
    # print the value of the objective
    print("objective =", pulp.value(prob.objective))

    # print the value of the variables at the optimum
    for v in prob.variables():
        print(f'{v.name} = {v.varValue:5.2f}')

    print("\nSensitivity Analysis")
    print("{:<30} {:<15} {:<15}".format("Constraint", "Shadow Price", "Slack"))
    for name, c in prob.constraints.items():
        print("{:<30} {:<15} {:<15}".format(
            f"{name} : {c}",
            str(c.pi),
            str(c.slack)
        ))

if __name__ == "__main__":
    solver()

