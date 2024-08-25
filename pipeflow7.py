import numpy as np
import matplotlib.pyplot as plt
import os

# Define simulation parameters
nx, ny = 800, 50  # Grid size
nt = 50000  # Number of time steps
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

# Initialize velocity and pressure fields
u = np.zeros((ny, nx))  # x-direction velocity
v = np.zeros((ny, nx))  # y-direction velocity
p = np.zeros((ny, nx))  # Pressure

# Function to update the velocity field
def update_velocity(u, v, p, rho, nu, dt, dx, dy):
    un = u.copy()
    vn = v.copy()

    # Add small artificial diffusion to help stabilize
    diffusion = 0.01 * nu

    # Update u component of velocity
    u[1:-1, 1:-1] = (un[1:-1, 1:-1] -
                     un[1:-1, 1:-1] * dt / dx * (un[1:-1, 1:-1] - un[1:-1, :-2]) -
                     vn[1:-1, 1:-1] * dt / dy * (un[1:-1, 1:-1] - un[:-2, 1:-1]) -
                     dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, :-2]) +
                     diffusion * (dt / dx**2 * (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, :-2]) +
                                  dt / dy**2 * (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[:-2, 1:-1])))

    # Update v component of velocity
    v[1:-1, 1:-1] = (vn[1:-1, 1:-1] -
                     un[1:-1, 1:-1] * dt / dx * (vn[1:-1, 1:-1] - vn[1:-1, :-2]) -
                     vn[1:-1, 1:-1] * dt / dy * (vn[1:-1, 1:-1] - vn[:-2, 1:-1]) -
                     dt / (2 * rho * dy) * (p[2:, 1:-1] - p[:-2, 1:-1]) +
                     diffusion * (dt / dx**2 * (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, :-2]) +
                                  dt / dy**2 * (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[:-2, 1:-1])))

    # Boundary conditions
    u[0, :] = 0
    u[-1, :] = 0
    v[0, :] = 0
    v[-1, :] = 0
    u[:, 0] = 0.5  # Inlet velocity
    u[:, -1] = u[:, -2]  # Outlet boundary condition (zero gradient)
    v[:, 0] = 0
    v[:, -1] = 0

    return u, v

# Create directories to save data
if not os.path.exists('frames'):
    os.makedirs('frames')
if not os.path.exists('data'):
    os.makedirs('data')

# Main simulation loop
for n in range(1,nt+1):
    u, v = update_velocity(u, v, p, rho, nu, dt, dx, dy)

    # Save velocity data every 50 iterations
    if n % 50 == 0: # or n == nt - 1:
        np.savetxt(f'data/u_{n:05d}.txt', u, fmt='%.6f')
        np.savetxt(f'data/v_{n:05d}.txt', v, fmt='%.6f')

        # Save images
        plt.clf()
        plt.contourf(X, Y, np.sqrt(u**2 + v**2), cmap='jet', levels=50)
        plt.colorbar()
        plt.title(f"Velocity field at time step {n}")
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.gca().set_aspect('equal', adjustable='box')  # Set aspect ratio
        plt.savefig(f'frames/frame_{n:05d}.png')  # Save frame as PNG

plt.show()
