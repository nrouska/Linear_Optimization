import pulp

def solver():
    # A LP problem
    prob = pulp.LpProblem("dovetail", pulp.LpMinimize)

    #Variables
    x =  pulp.LpVariable.dicts('x', range(1,8),lowBound=0, upBound = None, cat=pulp.LpContinuous)

    # Objective
    prob += x[1]+x[2]+x[3]+x[4]+x[5]+x[6]+x[7], 'obj'

    prob += x[1] + x[4] + x[5] + x[6] + x[7] >= 10 #sunday
    prob += x[1] + x[2] + x[5] + x[6] + x[7] >= 8 #monday
    prob += x[1] + x[2] + x[3] + x[6] + x[7] >= 8 #tuesday
    prob += x[1] + x[2] + x[3] + x[4] + x[7] >= 8 #wednesday
    prob += x[1] + x[2] + x[3] + x[4] + x[5] >= 8 #thursday
    prob += x[2] + x[3] + x[4] + x[5] + x[6] >= 15 #friday
    prob += x[3] + x[4] + x[5] + x[6] + x[7] >= 15 #saturday
    
    # solve the problem using the default solver
    prob.solve()

    # print the status of the solved LP
    print("Status:", pulp.LpStatus[prob.status])

    # print the value of the objective
    print("objective =", pulp.value(prob.objective))

    # print the value of the variables at the optimum
    for v in prob.variables():
        print(f'{v.name} = {v.varValue:5.2f}')


if __name__=='__main__':
    solver()
