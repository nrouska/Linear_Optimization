import numpy as np
import matplotlib.pyplot as plt

x1=np.linspace(0,10,700) # 700 points between 0 and 10, x1>=0

#constraints
c0=0*x1 # x2>=0
c1=(2.7- 0.3*x1) / 0.1  # Π1: 0.3x1 + 0.1x2 <= 2.7
c2=(6-0.5*x1)/0.5  # Π1: 0.3x1 + 0.1x2 = 6
c3= (6-0.6*x1)/0.4  # Π3: 0.6x1 + 0.4x2 >= 6

# vertices of the feasible area
# Intersection of Π1 and Π2
A = np.linalg.solve([[0.3, 0.1], [0.5, 0.5]], [2.7, 6])


# Intersection of Π2 and Π3
B = np.linalg.solve([[0.5, 0.5], [0.6, 0.4]], [6, 6])

vertices = np.array([A, B])
print(vertices)

z_values = 0.4*vertices[:, 0] + 0.5*vertices[:, 1] 
optimal_index = np.argmin(z_values) #index of the minimum z_value
min_z=np.min(z_values)
## contour lines for z=5.25,5
z0=(min_z -0.4*x1)/0.5
z1=(5-0.4*x1)/0.5
print(min_z)
optimal_vertex = vertices[optimal_index]
print(optimal_vertex)

# Plot the constraints
plt.plot(x1, c1, label='Π1: 0.3x₁ + 0.1x₂ <= 2.7')
plt.plot(x1, c2, label='Π2: 0.5x₁ + 0.5x₂ = 6')
plt.plot(x1, c3, label='Π3: 0.6x₁ + 0.4x₂ >= 6')
plt.plot(x1, c0, label='x₂ >= 0')
plt.axvline(x=0, label='x₁ >= 0')
plt.plot(x1, z0, 'r--', label='0.4x₁ + 0.5x₂ = z')
plt.plot(x1, z1, 'r--')
plt.grid(True)
plt.xlabel('x₁')
plt.ylabel('x₂')
plt.xlim(-1,10)
plt.ylim(-1,10)
plt.title('Feasible Region and optimal solution')
plt.scatter(vertices[:,0],vertices[:,1],color='red',s=50,zorder=5)
#display labels
plt.legend()
# display the plot
plt.show()

