import numpy as np
from itertools import combinations
from scipy.optimize import linprog

#7 constraints in standard form (A x <= b)
A = np.array([
    [-1, -1,  0],  # x1 + x2 >= 10 -> -x1 -x2 <= -10
    [ 0, -1, -1],  # x2 + x3 >= 15 -> -x2 -x3 <= -15
    [-1,  0, -1],  # x1 + x3 >= 12 -> -x1 -x3 <= -12
    [20, 10, 15],  # 20x1 + 10x2 + 15x3 <= 300
    [-1,  0,  0],  # x1 >= 0 -> -x1 <= 0
    [ 0, -1,  0],  # x2 >= 0 -> -x2 <= 0
    [ 0,  0, -1]   # x3 >= 0 -> -x3 <= 0
])
b = np.array([-10, -15, -12, 300, 0, 0, 0])

# a vertex is formed by the intersection of three constraints
vertices = []
hyperplanes=[]
no_intersecting_hyperplanes=[]
feasible_vertices=[]
for indices in combinations(range(len(A)), 3): # all combinations of three constraints
    A_sub = A[list(indices)]
    b_sub = b[list(indices)]
    hyperplanes.append(indices)
    try:
        x = np.linalg.solve(A_sub, b_sub) # solve 3x3, x is the intersection
        vertices.append(x)
    except np.linalg.LinAlgError: 
       no_intersecting_hyperplanes.append(indices)
        
vertices=np.round(vertices,decimals=2) #only 2 decimals in [x1, x2, x3]

#if a vertex is formed twice by different combination of hyperplanes added in degenerate_vertices
unique_vertices, counts = np.unique(vertices, axis=0, return_counts=True) 
degenerate_vertices=unique_vertices[counts>1]
print(degenerate_vertices)

print("Hyperplanes(Constraint Indices) that don't form a vertex")
for i in no_intersecting_hyperplanes: print(i)

print("\nAll Vertices:")
print(f"{'Vertex':<6} {'[x1, x2, x3]':<20} {'Hyperplanes (Constraint Indices)'}")

for i, (v, h) in enumerate(zip(vertices, hyperplanes)):
    print(f"{i:<6} {str(v):<20} {h}")
    if np.all(A @ v <= b ):  # vertex that satisfies all the constraints is feasible
        feasible_vertices.append(v)

print("\nFeasible Vertices:")
print(f"{'Vertex':<6} {'[x1, x2, x3]':<20} {'Hyperplanes (Constraint Indices)'}")
for i, (v, h) in enumerate(zip(feasible_vertices, hyperplanes)):
    print(f"{i:<6} {str(v):<20} {h}")