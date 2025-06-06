import pulp
def solver():
    # A LP problem
    prob = pulp.LpProblem("ex5", pulp.LpMaximize)

    #Variables
    x =  pulp.LpVariable.dicts('x', range(1,4),lowBound=0, upBound = None, cat=pulp.LpContinuous)

    # Objective
    prob += 34*x[1]+29*x[2]+2*x[3], 'obj'

    prob += 7*x[1] + 5*x[2] - x[3] <= 16 
    prob += -x[1] + 3*x[2] + x[3] <= 10
    prob += -x[2] + 2*x[3] <= 3

    ##1o branching
    #prob += x[1]<=0
    prob += x[1]>=1

    ##2o branching
    #prob += x[2]<=2
    prob += x[2]>=3

    ##3o branching
    #prob += x[3]<=2
    # prob += x[3]>=3

    ##4o branching
    #prob += x[1]<=1
    # prob += x[1]>=2

    ##5o branching
    #prob += x[3]<=1
    #prob += x[3]>=2

    ##6o branching
    #prob += x[1]<=1
    #prob += x[1]>=2

    ##7ο branching
    #prob += x[2]<=3
    #prob += x[2]>=4

    ##8ο branching
    #prob += x[2]<=0
    #prob += x[2]>=1

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

