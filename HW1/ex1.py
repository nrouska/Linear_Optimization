import numpy as np
import matplotlib.pyplot as plt

x1=np.linspace(0,6,700) # 700 points between 0 and 6, x1>=0
#constraints
c0=0*x1 # x2>=0
c1=(12- 6*x1) / 3  # Π1: 6x1 + 3x2 >= 12
c2=(16-4*x1)/8  # Π2: 4x1 + 8x2 >= 16
c3= (30-6*x1)/5  # Π3: 6x1 + 5x2 >= 30
c4= (36-6*x1)/7  # Π4: 6x1 + 7x2 >= 36


# vertices of the feasible area
# Intersection of Π3 and Π4
A = np.linalg.solve([[6, 5], [6, 7]], [30, 36])

# Intersection of Π3 and x2=0
B = np.linalg.solve([[6, 5], [0, 1]], [30, 0])

# Intersection of Π2 and x2=0
C = np.linalg.solve([[4, 8], [0, 1]], [16, 0])

# Intersection of Π1 and Π2
D = np.linalg.solve([[6, 3], [4, 8]], [12, 16])

# Intersection of Π1 and x1=0
E = np.linalg.solve([[6, 3], [1, 0]], [12, 0])

# Intersection of Π4 and x1=0
F = np.linalg.solve([[6, 7], [1, 0]], [36, 0])

vertices = np.array([A, B, C, D, E, F])
vertices=np.round(vertices,3) #3 decimals
print(vertices)

z_values = 3*vertices[:, 0] + vertices[:, 1] #objective function in each vertex

optimal_index = np.argmax(z_values) #index of the max z_value
max_z=np.max(z_values)

##contour lines of the objective function for z=15,12,13.5
z0 = max_z - 3*x1
z1 = 12- 3*x1
z2 = 13.5-3*x1
print(max_z)

optimal_vertex = vertices[optimal_index]
print(optimal_vertex)

# Plot the constraints
plt.plot(x1, c1, label='Π1: 6x₁ + 3x₂ >= 12')
plt.plot(x1, c2, label='Π2: 4x₁ + 8x₂ >= 16')
plt.plot(x1, c3, label='Π3: 6x₁ + 5x₂ <= 30')
plt.plot(x1, c4, label='Π4: 6x₁ + 7x₂ <= 36')
plt.plot(x1, c0, label='x₂ >= 0')
plt.axvline(x=0, label='x₁ >= 0')

plt.plot(x1, z0, 'r--', label='3x₁ + x₂ = z')
plt.plot(x1, z1, 'r--')
plt.plot(x1, z2, 'r--')

plt.grid(True)
plt.xlabel('x₁')
plt.ylabel('x₂')
plt.ylim(-2,7)
plt.xlim(-1,6)
plt.title('Feasible Region and optimal solution')

upper_bound= np.minimum(c3,c4) # in each x2 take the minimum of <= constraints
lower_bound= np.maximum(np.maximum(c1,c2),c0) # in each x2 take the maximum of >= constraints
# plot area between constraints
plt.fill_between(x1,lower_bound,upper_bound,where=(upper_bound>lower_bound) & (x1>0),alpha=0.5)
#plot vertices
plt.scatter(vertices[:,0],vertices[:,1],color='red',s=50,zorder=5)

#display labels
plt.legend()
# display the plot
plt.show()