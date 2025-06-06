import pulp
def solver():
    # A LP problem
    prob = pulp.LpProblem("ex6", pulp.LpMaximize)

    #Variables
    x =  pulp.LpVariable.dicts('x', range(1,6),lowBound=0, upBound = 1, cat=pulp.LpContinuous)

    # Objective
    prob += 10*x[4]+14*x[5]+31*x[2]+48*x[1]+60*x[3], 'obj'

    prob += 2*x[4] + 3*x[5] + 4*x[2] + 6*x[1] + 8*x[3] <= 11
    
    #1o branching
    prob += x[3]==0

    #2o branching
    prob += x[4]==1

    #3o branching
    prob += x[1]==1

    #4o branching
    #prob += x[5]==1

    #5o branching
    #prob += x[2]==1

    #6o branching
    prob += x[2] ==1

    # solve the problem using the default solver
    prob.solve()

    # print the status of the solved LP
    print("Status:", pulp.LpStatus[prob.status])

    # print the value of the objective
    print(f"objective = {pulp.value(prob.objective):5.2f}")

    # print the value of the variables at the optimum
    for v in prob.variables():
        print(f'{v.name} = {v.varValue:5.2f}')

if __name__=='__main__':
    solver()

