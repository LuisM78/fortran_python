import numpy as np
import matplotlib.pyplot as plt
import os

import pandas as pd

# Define simulation parameters
nx, ny = 800, 50  # Grid size
nt = 500  # Number of time steps
dt = 0.008  # Smaller time step size to improve stability
rho = 1.0  # Density of the fluid
nu = 0.1  # Kinematic viscosity

# Physical domain
Lx, Ly = 10.0, 0.5  # Domain size
dx = Lx / (nx - 1)  # Grid spacing in x
dy = Ly / (ny - 1)  # Grid spacing in y

# Create mesh grid
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Function to read data from Fortran output files
def read_fortran_data(filename, nx, ny):
    # Try reading the entire file into a single DataFrame with space as delimiter
    try:
        df = pd.read_csv(filename, sep='\s+', header=None, dtype=np.float64)
    except Exception as e:
        raise RuntimeError(f"Failed to read the file: {e}")

    # Debugging output: Check the shape and first few rows
    # print(f"DataFrame shape: {df.shape}")
    # print("First few rows of the DataFrame:")
    # print(df.head())

    # Check if the file contains enough rows
    expected_rows = 3 * ny
    if df.shape[0] < expected_rows:
        raise ValueError(f"File format is incorrect: expected at least {expected_rows} rows but found {df.shape[0]} rows")

    # Initialize arrays
    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))
    
    # Extract data for u, v, and p
    for j in range(ny):
        u[j, :] = df.iloc[j, :].values
        v[j, :] = df.iloc[ny + j, :].values
        p[j, :] = df.iloc[2 * ny + j, :].values

    return u, v, p

# Create a directory to save images
if not os.path.exists('frames2'):
    os.makedirs('frames2')

# Main plotting loop
nt = 50000
for n in range(0, nt + 1, 50):
    filename = f"results//{n:05d}.txt"
    if os.path.exists(filename):
        u, v, p = read_fortran_data(filename,nx,ny)
        #print('u nax', np.max(u))
        plt.clf()
        plt.contourf(X, Y, np.sqrt(u**2 + v**2), cmap='jet', levels=50)
        plt.colorbar()
        plt.title(f"Velocity field at time step {n}")
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.gca().set_aspect('equal', adjustable='box')  # Set aspect ratio
        plt.savefig(f'frames2/frame_{n:05d}.png')  # Save frame as PNG
        plt.close()

plt.show()

# # Plot velocity profiles at different distances from the inlet
# x_positions = [0.01 * Lx, 0.05 * Lx, 0.1 * Lx, 0.2 * Lx, 0.3 * Lx, 0.4 * Lx, 0.5 * Lx, 0.6 * Lx, 0.7 * Lx, 0.9 * Lx]  # Selected x positions

# plt.figure(figsize=(12, 6))
# for x_pos in x_positions:
#     idx = int(x_pos / dx)
#     plt.plot(u[:, idx], y, label=f'x = {x_pos:.1f} m')

# plt.xlabel('Horizontal Velocity (u)')
# plt.ylabel('Height (y)')
# plt.title('Velocity Profiles at Different Distances from Inlet')
# plt.legend()
# plt.grid(True)
# plt.gca().set_aspect('equal', adjustable='box')  # Set aspect ratio to match the physical domain
# plt.show()
