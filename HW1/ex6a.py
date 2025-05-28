import numpy as np

# Problem setup
c = np.array([2, 1, 6, -4])  # Objective coefficients (maximize)

A = np.array([
   
    [1, 2, 4, -1],   # x1 + 2x2 + 4x3 − x4 ≤ 6   
    [2, 3, -1, 1],    # 2x1 + 3x2 − x3 + x4 ≤ 12
    [1, 0, 1, 1]      # x1 + x3 + x4 ≤ 2   
])
b = np.array([6, 12, 2])

num_constraints, num_vars = A.shape
# tableau structure rows= 3 constraints and the objective,col= 4 decision var + 3 slack vars + b
tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))

# Initialize tableau
tableau[:-1, :num_vars] = A # all rows except from the objective and cols of decision vars
tableau[:-1, num_vars:num_vars+num_constraints] = np.eye(num_constraints)  # identity matrix (cols: slack vars)
tableau[:-1, -1] = b # last column b
tableau[-1, :num_vars] = c  # last row objective funct (c coefficients)

# variable labels [x1, x2, x3, x4, s1, s2, s3 ,b]
var_labels = ['x1', 'x2', 'x3', 'x4', 's1', 's2', 's3',' b']
basic_vars=[4,5,6] # initial basis slack variables 

def print_tableau(tableau, iteration, basic_vars):
    print(f"\nIteration {iteration}:")
    #print header
    print("\t" + "\t".join(var_labels))

    #print z_row
    z_row = tableau[-1, :]  
    print(f"-Z\t" + "\t".join(f"{val:.2f}" for val in z_row))

    #print basis rows 
    for row in range(num_constraints):
        basis_col = basic_vars[row]
        print(f"{var_labels[basis_col]}\t" + "\t".join(f"{val:.2f}" for val in tableau[row]))

def simplex(tableau):
    iteration = 0
    print_tableau(tableau, iteration, basic_vars)
    while True:
        iteration += 1
        # check for optimality if there are not any non positive c coefficients stop
        if np.all(tableau[-1, :-1] <= 0): #last row
            break
            
        # select entering variable most positive in objective row
        entering_col = np.argmax(tableau[-1, :-1])
        
        # check for unbounded problem
        # pivot  column must have at least one value>0 for the minimum ratio test
        if np.all(tableau[:-1, entering_col] <= 0): 
            raise Exception("Problem is unbounded")
    
        # select leaving variable (minimum ratio test)
        ratios = []
        for i in range(num_constraints):
            if tableau[i, entering_col] > 0: #positive coefficients in the entering column
                # b_i / entering column coefficient i
                ratios.append(tableau[i, -1] / tableau[i, entering_col]) 
            else:
                ratios.append(np.inf) #else ignore ratio
        leaving_row = np.argmin(ratios) 
        # pivot element
        pivot = tableau[leaving_row, entering_col]
        basic_vars[leaving_row] = entering_col
        tableau[leaving_row, :] /= pivot # 1 in pivot element
        for i in range(num_constraints + 1):
            if i != leaving_row:
                #zeros in all the rows of entering column except pivot
                tableau[i, :] -= tableau[i, entering_col] * tableau[leaving_row, :]
        # print current tableau
        print_tableau(tableau, iteration, basic_vars)
    return tableau
# run simplex algorithm
simplex(tableau)


