import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
import random

# Function to generate Perlin noise
def perlin_noise(x, y, seed=0):
    random.seed(seed)
    
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(t, a, b):
        return a + t * (b - a)

    def grad(hash, x, y):
        h = hash & 15
        u = x if h < 8 else y
        v = y if h < 8 else x
        return ((h & 1) * u + (h & 2) * -u + (h & 4) * v + (h & 8) * -v)

    p = list(range(512))
    random.shuffle(p)
    p += p

    X = int(x) & 255
    Y = int(y) & 255

    x -= int(x)
    y -= int(y)

    u = fade(x)
    v = fade(y)

    A = p[X] + Y
    B = p[X + 1] + Y

    return lerp(v, lerp(u, grad(p[A], x, y),
                     grad(p[B], x - 1, y)),
                lerp(u, grad(p[A + 1], x, y - 1),
                     grad(p[B + 1], x - 1, y - 1)))

# Generate 10,000 random points within a rectangle
np.random.seed(0)
num_points = 10000
x_min, x_max = 0, 200
y_min, y_max = 0, 100
points = np.random.uniform(x_min, x_max, (num_points, 2))

# Compute the Voronoi diagram
vor = Voronoi(points)

# Create a gray background
fig, ax = plt.subplots()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_facecolor('gray')

# Perlin Noise Parameters
scale = 50  # Adjust the scale to control the noise granularity
water_percentage = 0.5  # Percentage of water cells

# Initialize the land/water data
land_water_data = np.zeros(len(vor.regions) - 1)  # Adjust size

# Generate Perlin noise values for each Voronoi cell
for i, region in enumerate(vor.regions[:-1]):  # Iterate up to len(regions) - 1
    if not -1 in region and len(region) > 0:
        polygon = [vor.vertices[i] for i in region]
        centroid = np.mean(polygon, axis=0)
        # Use the homemade Perlin noise to determine land/water
        noise_value = perlin_noise(centroid[0] / scale, centroid[1] / scale)
        if noise_value > (1 - water_percentage):  # Adjust threshold based on water percentage
            land_water_data[i] = 1  # Land
        else:
            land_water_data[i] = 0  # Water

# Plot Voronoi regions with land and water colors
for i, region in enumerate(vor.regions[:-1]):  # Iterate up to len(regions) - 1
    if not -1 in region and len(region) > 0:
        polygon = [vor.vertices[i] for i in region]
        if land_water_data[i] == 1:
            ax.fill(*zip(*polygon), edgecolor='none', lw=1, facecolor='burlywood')  # Land
        else:
            ax.fill(*zip(*polygon), edgecolor='none', lw=1, facecolor='navy')  # Darker blue for Water

# Remove blue dots at Voronoi vertices
ax.plot(vor.vertices[:, 0], vor.vertices[:, 1], 'bo', markersize=0)

plt.gca().set_aspect('equal', adjustable='box')
plt.title('Voronoi Diagram with Homemade Perlin Noise Land/Water')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
