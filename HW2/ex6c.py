import pulp
def solver():
    # A LP problem
    prob = pulp.LpProblem("ex6c", pulp.LpMinimize)

    #Variables
    y =  pulp.LpVariable.dicts('y', range(1,7),lowBound=0, upBound = None, cat=pulp.LpInteger)

    # Objective
    prob += 11*y[1]+y[2]+y[3]+y[4]+y[5]+y[6], 'obj'

    prob += 6*y[1] + y[2] >=48
    prob += 4*y[1] + y[3] >=31
    prob += 8*y[1] + y[4] >=60
    prob += 2*y[1] + y[5] >=10
    prob += 3*y[1] + y[6] >=14


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
