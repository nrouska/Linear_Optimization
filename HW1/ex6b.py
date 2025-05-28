import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
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


G = nx.DiGraph() #empty directed graph
visited = set()  #visited basis


#key for each state (basic_vars, b_values, z)
def tableau_key(basis, tableau):
    return tuple(basis), tuple(np.round(tableau[:, -1],4)), round(tableau[-1, -1],4)


def dfs(tableau, basis):
    key = tableau_key(basis, tableau)
    
    if key in visited:
        return
    visited.add(key)

    # info in node (basis,decision_vars,z)
    node = f"B={[var_labels[i] for i in basis]}\n"
    decision_vars=[0.0]*4
    for row, idx in enumerate(basis):
        if idx < 4: 
            decision_vars[idx] = round(tableau[row, -1], 2) #if it is in basis its value is in b column

    node  += f"x={tuple(decision_vars)}\n"  # Shows (x₁, x₂, x₃, x₄)
    node += f"Z={round(-tableau[-1, -1], 2)}" 

    ##add node to graph
    # if c coefficients <=0 stop optimal solution 
    G.add_node(key, label=node, color="#9EC6F3" if np.all(tableau[-1, :-1] <= 0) else "#FFF1D5")
    # c coefficients
    z_row = tableau[-1, :-1]
    entering_vars = [j for j in range(len(z_row)) if z_row[j] > 0] # possible entering vars 
    for entering_col in entering_vars:
        # minimum ratio test
        #compute ratios for each possible entering variable
        ratios = []
        for i in range(num_constraints):
            aij = tableau[i, entering_col] #value in column of the entering var
            if aij > 0:
                ratios.append((tableau[i, -1] / aij, i)) # b_i/ aij
        if not ratios: #ratios for the next entering var
            continue

        min_ratio = min(ratios)[0]

        for ratio, leaving_row in ratios:
            if np.isclose(ratio,min_ratio): #for floating errors
                new_tableau = tableau.copy()
                pivot = new_tableau[leaving_row, entering_col]
                new_tableau[leaving_row] /= pivot #1 in pivot element

                for i in range(num_constraints + 1):
                    if i != leaving_row:
                        #zeros in all the rows of entering column except pivot
                        new_tableau[i, :] -= new_tableau[i, entering_col] * new_tableau[leaving_row, :]

                new_basis = basis.copy()
                
                new_basis[leaving_row] = entering_col #variables interchange in basis
                new_key = tableau_key(new_basis, new_tableau) 
                
                G.add_edge(key, new_key)
                dfs(new_tableau, new_basis)  

#starts dfs algorithm with initial state
dfs(tableau, basic_vars)
# Σχεδίαση γράφου
pos = nx.spring_layout(G)
node_colors = [G.nodes[n]["color"] for n in G.nodes]
labels = nx.get_node_attributes(G, "label")
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_nodes(G, pos, node_color = node_colors, edgecolors = "black", node_size = 11000) 
nx.draw_networkx_edges(G, pos) 
nx.draw_networkx_labels(G, pos, labels=labels, font_size = 12) 
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size = 5) 
plt.title("Simplex Adjacency Graph") 
plt.axis("off") 
plt.tight_layout() 
plt.show()
