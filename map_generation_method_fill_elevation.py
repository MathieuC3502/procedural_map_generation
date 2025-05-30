import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
import matplotlib as mpl
import random as rd
import math
import time

start = time.time()

def find_adjacent_cells(vor, cell_index):
    adjacent_cells = []
    target_cell = vor.regions[cell_index]

    # Iterate through all the cells
    for i, cell in enumerate(vor.regions):
        if i == cell_index:
            continue  # Skip the target cell itself

        # Check if the target cell and the current cell share any edges
        shared_edges = set(target_cell) & set(cell)

        if shared_edges:
            adjacent_cells.append(i)

    return adjacent_cells

def grow_elevation(seed_cells,elevation):
    processed_cells=seed_cells
    while len(processed_cells)<len(elevation)-1:
        end1=time.time()
        print(len(processed_cells))
        adjacent_cells=[]
        
        for i in seed_cells:
            adj_cells = find_adjacent_cells(vor, i)
            for j in adj_cells:
                if j not in processed_cells:
                    adjacent_cells.append(j)
                    processed_cells.append(j)
                    if elevation[i]>=0:
                        elevation[j]=np.random.normal(0.25, 0.05)*elevation[i]+np.random.normal(0, 0.25)
                    else:
                        elevation[j]=np.random.normal(1.25, 0.05)*elevation[i]+np.random.normal(0, 0.25)
        seed_cells=adjacent_cells
        
    return elevation
        

# Generate 1000 random points within a rectangle
np.random.seed(0)
num_points = 10000
x_min, x_max = -100, 100
y_min, y_max = -50, 50
points = np.random.uniform(x_min, x_max, (num_points, 2))

# Compute the Voronoi diagram
vor = Voronoi(points)

# Select elevation seeds
seed_number = 2 #int(0.02*num_points)
seeds_index = []
for i in range(seed_number):
    seed = rd.randint(0, len(vor.regions))
    seeds_index.append(seed)

# Assign Elevation Value to the Seeds
elevation = [0] * len(vor.regions)
for i in range(len(seeds_index)):
    if i==0:
        elevation[seeds_index[i]] = 2000#abs(np.random.normal(0.5, 5))
    elif i==1:
        elevation[seeds_index[i]] = -500
    
elevation=grow_elevation(seeds_index,elevation)
print("Elevation Generated \n")


# Create a gray background
fig, ax = plt.subplots()
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_facecolor('white')

seashore=0
T1=666 #max(elevation)/2
T2=-166 #min(elevation)/2

print("Starting Display \n")
for i in range(len(vor.regions)):
    if not vor.regions[i]:
        continue

    polygon = [vor.vertices[j] for j in vor.regions[i]]

    # Clip the polygon to the display boundaries
    clipped_polygon = []
    for p in polygon:
        if x_min <= p[0] <= x_max and y_min <= p[1] <= y_max:
            clipped_polygon.append(p)

    if clipped_polygon:
        if elevation[i]>seashore and elevation[i]<=T1:
            ax.fill(*zip(*clipped_polygon), edgecolor='lightgreen', lw=1, facecolor='lightgreen')
        elif elevation[i]>T1 and elevation[i]<=2*T1:
            ax.fill(*zip(*clipped_polygon), edgecolor='green', lw=1, facecolor='green')
        elif elevation[i]>2*T1 :
            ax.fill(*zip(*clipped_polygon), edgecolor='sienna', lw=1, facecolor='sienna')
        elif elevation[i]<=2*T2:
            ax.fill(*zip(*clipped_polygon), edgecolor='navy', lw=1, facecolor='navy')
        elif elevation[i]>2*T2 and elevation[i]<=T2:
            ax.fill(*zip(*clipped_polygon), edgecolor='lightblue', lw=1, facecolor='lightblue')
        else:
            ax.fill(*zip(*clipped_polygon), edgecolor='royalblue', lw=1, facecolor='royalblue')

# Remove blue dots at Voronoi vertices
ax.plot(vor.vertices[:, 0], vor.vertices[:, 1], 'bo', markersize=0)

plt.gca().set_aspect('equal', adjustable='box')
plt.title('Map generation based on a Voronoi diagram with elevation growth from random seeds',wrap=True)
plt.grid(False)
plt.axis('off')
#plt.show()
plt.savefig('C:/Users/mathi/Documents/__DOCUMENTS__/04_PERSONNEL/01_PROJETS/[PYTHON]_PROCEDURAL_MAP_GENERATION/RESULTS/test.png')

end=time.time()
print("Execution time : ",end-start)