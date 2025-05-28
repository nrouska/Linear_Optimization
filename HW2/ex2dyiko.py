import pulp

def solver():
    # A LP problem
    prob = pulp.LpProblem("exersice1d", pulp.LpMaximize)

    # Variables
    y1 = pulp.LpVariable("y1", None, 0)
    y2 = pulp.LpVariable("y2", None, None)
    y3 = pulp.LpVariable("y3", 0, None)
   
    # Objective
    prob += 6*y2 + 3*y3 , "obj"

    # Constraints
    prob += 2*y1 - y2 +3*y3 >= 1,  "c1"
    prob += 3*y1 + y2 + y3 <= 1, "c2"
    prob += y1 + 2*y2 + 4*y3 == 0, "c3"
    prob += y1 + y2 + 2*y3 <= 0, "c4"
  
    # solve the problem using the default solver
    prob.solve()

    # print the status of the solved LP
    print("Status:", pulp.LpStatus[prob.status])
    # print the value of the objective
    print(f"objective = {pulp.value(prob.objective):5.2f}")

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

