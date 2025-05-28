from ex5a import vertices,feasible_vertices
from ex5b import solutions, feasible_solutions
import numpy as np

for i, sol in enumerate(solutions):
    #extract x1, x2, x3 from the solution dictionary
    x1 = sol['x1']
    x2 = sol['x2']
    x3 = sol['x3']
    current_solution = np.array([x1, x2, x3])
    for j, vertex in enumerate(vertices): 
        if (current_solution==vertex).all():
            print(f"Basic solution #{i} matches vertex #{j}: {vertex}")
feasible_vertices=np.array(feasible_vertices)

z_values = 8*feasible_vertices[:, 0] + 5*feasible_vertices[:, 1] + 4*feasible_vertices[:, 2]#objective function in each vertex
optimal_index = np.argmin(z_values) #index of the max z_value
min_z=np.min(z_values)

print(f"Optimal z_value {min_z}")
optimal_vertex = vertices[optimal_index]
print(f"Optimal vertex {optimal_vertex}")