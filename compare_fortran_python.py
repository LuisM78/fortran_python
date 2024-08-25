import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import time

# Physical domain
Lx, Ly = 10.0, 0.5  # Domain size
nx, ny = 800, 50  # Grid size
dx = Lx / (nx - 1)  # Grid spacing in x
dy = Ly / (ny - 1)  # Grid spacing in y

# Create mesh grid
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Directory containing the saved data
data_dir = 'data'

# Get all data files
u_files = sorted([f for f in os.listdir(data_dir) if f.startswith('u_') and f.endswith('.txt')])
v_files = sorted([f for f in os.listdir(data_dir) if f.startswith('v_') and f.endswith('.txt')])


if not os.path.exists('compareprofiles'):
    os.makedirs('compareprofiles')


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


data_dir = 'data'
# Get all data files
u_files = sorted([f for f in os.listdir(data_dir) if f.startswith('u_') and f.endswith('.txt')])
v_files = sorted([f for f in os.listdir(data_dir) if f.startswith('v_') and f.endswith('.txt')])
#print('uv_files',u_files)

nt = 50

for u_file, v_file in zip(u_files[1:], v_files[1:]):
    upython = np.loadtxt(os.path.join(data_dir, u_file))
    vpython = np.loadtxt(os.path.join(data_dir, v_file))
    timestep = int(u_file.split('_')[1].split('.')[0])  # Extract timestep from filename
    nt = timestep
    
    filename = f"results//{nt:05d}.txt"

    u, v, p = read_fortran_data(filename,nx,ny)
    #print('im here')

    x_positions = [0.01 * Lx, 0.05 * Lx, 0.1 * Lx, 0.2 * Lx, 0.3 * Lx, 0.4 * Lx, 0.5 * Lx, 0.6 * Lx, 0.7 * Lx, 0.9 * Lx]  # Selected x positions

    plt.figure(figsize=(12, 6))
    for x_pos in x_positions:
        idx = int(x_pos / dx)
        plt.plot(u[:, idx], y, marker='o', linestyle='-', label=f'Fortran iter {nt} x = {x_pos:.1f} m')
        plt.plot(upython[:, idx], y, marker='x', linestyle='--', label=f'Python x = {x_pos:.1f} m')
    plt.xlabel('Horizontal Velocity (u)')
    plt.ylabel('Height (y)')
    plt.title(f'Velocity Profiles at Different Distances from Inlet {timestep}')
    #plt.title(f"Velocity field at time step {timestep}")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')  # Set aspect ratio to match the physical domain
    plt.savefig(f'compareprofiles/frame_{timestep:05d}.png')  # Save frame as PNG
    #plt.show()
    plt.close()  # Close the current figure to free up memory
    
