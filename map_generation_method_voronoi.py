import numpy as np
from scipy.spatial import Voronoi, Delaunay
import matplotlib.pyplot as plt

# Generate 10,000 random points within a rectangle
np.random.seed(0)  # Set a random seed for reproducibility
num_points = 1000
x_min, x_max = 0, 200  # Rectangle's x-coordinate range
y_min, y_max = 0, 100  # Rectangle's y-coordinate range
points = np.random.uniform(x_min, x_max, (num_points, 2))

# Compute the Voronoi diagram
vor = Voronoi(points)

# Compute the Delaunay triangulation
tri = Delaunay(points)

# Create a gray background
fig, ax = plt.subplots()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_facecolor('gray')

# Plot Voronoi regions with white edges
for region in vor.regions:
    if not -1 in region and len(region) > 0:
        polygon = [vor.vertices[i] for i in region]
        ax.fill(*zip(*polygon), edgecolor='white', lw=1, facecolor='none')

# Plot the centers of Voronoi regions (Delaunay vertices) with red dots
ax.plot(vor.vertices[:, 0], vor.vertices[:, 1], 'bo', markersize=5)

# Plot the Delaunay triangulation edges in black
ax.triplot(points[:, 0], points[:, 1], tri.simplices, color='black', lw=1)

# Plot the points in red
ax.plot(points[:, 0], points[:, 1], 'ro', markersize=3)

plt.gca().set_aspect('equal', adjustable='box')
plt.title('Voronoi Diagram with Delaunay Triangulation')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()