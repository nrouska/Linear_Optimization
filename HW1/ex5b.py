import numpy as np
from itertools import combinations

#the constraints with slack variables [Α Ι]
A = np.array([
    [ 1,  1,  0,  -1,  0,  0,  0],  # x1 + x2 - s1 = 10
    [ 0,  1,  1,  0,  -1,  0,  0],  # x2 + x3 - s2 = 15
    [ 1,  0,  1,  0,  0,  -1,  0],  # x1 + x3 - s3 = 12
    [20, 10, 15,  0,  0,  0,  1],  # 20x1 + 10x2 + 15x3 + s4 = 300
   
])

b = np.array([10, 15, 12, 300])
solutions = []
feasible_solutions=[]
num_vars=7
degenerate_solutions=[]
index_sol=[]
for indices in combinations(range(7), 4): #combinations of 4 columns (out of 7 columns) for basic matrix
    
    B = A[:, list(indices)]  # select columns corresponding to the basic variables
    b_sub = b               
    try:
        # Solve the system  B* x_basic = b
        x_basic = np.linalg.solve(B, b_sub)

        x_full = np.zeros(num_vars)
        x_full[list(indices)] = x_basic #[x_basic, x_N]

        var_names = ['x1', 'x2', 'x3', 's1', 's2', 's3', 's4']
        solution = {var_names[i]: round(x_full[i], 2) for i in range(num_vars)} # dictionary {var_name1:value, var_name2:value, var_name3:value..}
        #{var_name1:value, var_name2:value, var_name3:value.., 'basic_vars':[var_name1,var_name2,...]}
        solution['basic_vars'] = [var_names[i] for i in indices] 
        solutions.append(solution)
        
    except np.linalg.LinAlgError: ## linear dependent columns, B not invertible
        continue

print("Solution Basic variables x_basic (x_N = 0)")
for i, sol in enumerate(solutions):
    basic_vars = sol['basic_vars']
    basic_values = [f"{var}={sol[var]:<6}" for var in basic_vars]
    print(f"{i:<8}  {' '.join(basic_values)}")
    if all(val >= 0 for var, val in sol.items() if var != 'basic_vars'): ## feasible solution if x_basic >=0
        feasible_solutions.append(sol)
        index_sol.append(i)

    if any(val == 0 for val in x_basic): ## degenerate solution basic_variable=0
        degenerate_solutions.append(sol)


print("Feasible Solutions")
print("Solution Basic variables x_basic>=0 (x_N = 0)")       
for idx, sol in zip(index_sol,feasible_solutions):
    basic_pairs = [f"{var}={sol[var]:<6}" for var in sol['basic_vars']]
    print(f"{idx:<8}  {' '.join(basic_pairs)}")
       
print(degenerate_solutions)
