from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
from matplotlib.backend_bases import MouseButton
import matplotlib
target_x = 0
target_y = 0

num_particles = 50
dimensions = 2
iters = 100

# PSO parameters
w_max = 0.9  # Maximum inertia weight
w_min = 0.4  # Minimum inertia weight
c1 = 2      # Cognitive (particle)
c2 = 2      # Social (swarm)

# Initialize particles and velocities
particles = np.random.uniform(-2, 2, size=(num_particles, dimensions))
velocities = np.zeros((num_particles, dimensions))

# Initialize local best as the current particle positions
local_best = particles.copy()

# Initialize global best as a point far from the search space
global_best = np.array([0, -10])

# Store previous particle positions for plotting trails
particle_trails = []

# Maximum trail length (adjust as needed)
max_trail_length = 500

# Evaluate fitness
def evaluate(particle):
    x, y = particle
    return sqrt((x - target_x)**2 + (y - target_y)**2)

# Initialize plot
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
particle_handles, = ax.plot(particles[:, 0], particles[:, 1], 'r_')

def animate(i):
    x_lim = ax.get_xlim() 
    y_lim = ax.get_ylim()
    global global_best
    ax.cla()
    ax.set_xlim(x_lim) 
    ax.set_ylim(y_lim)
    # Update inertia weight (linearly decreasing)
    w = w_max - (w_max - w_min) * i / iters

    # Update particle velocities and positions
    for j in range(num_particles):
        # Update local best
        if evaluate(particles[j]) < evaluate(local_best[j]):
            local_best[j] = particles[j].copy()

        # Update global best
        if evaluate(particles[j]) < evaluate(global_best):
            global_best = particles[j].copy()

        # Update velocity
        r1, r2 = random.random(), random.random()
        velocities[j] = w * velocities[j] + c1 * r1 * (local_best[j] - particles[j]) + c2 * r2 * (global_best - particles[j])

        # Limit velocity magnitude
        velocities[j] = np.clip(velocities[j], -0.1, 0.1)

        # Update position
        particles[j] += velocities[j]

        # Check bounds
        particles[j] = np.clip(particles[j], -100, 100)

    # Store current particle positions for plotting trails
    particle_trails.append(particles.copy())

    # Limit the length of the trails
    while len(particle_trails) > max_trail_length:
        del particle_trails[0]  # Remove the oldest positions

    # Update plot
    particle_handles.set_data(particles[:, 0], particles[:, 1])

    # Plot particle trails as lines
    if len(particle_trails) > 1:
        cmap = plt.get_cmap('Reds')
        for j in range(num_particles):
            # Only plot the last 5 trail positions
            trail = np.array(particle_trails)[-50:, j, :]
            
            # Fade color
            cmap = plt.get_cmap('Reds') 
            norm = matplotlib.colors.Normalize(vmin=0, vmax=max_trail_length)
            color = cmap(norm(len(particle_trails)))
            
            ax.plot(trail[:, 0], trail[:, 1], color=color)
        # for j in range(num_particles):
        #     trail = np.array(particle_trails)[:, j, :]  # Get the trail for particle j
        #     ax.plot(trail[:, 0], trail[:, 1], 'r-', alpha=0.2)  # Plot the trail

    return particle_handles,

ani = animation.FuncAnimation(fig, animate, frames=iters, interval=40)

def on_click(event):
    global target_x, target_y
    if event.button is MouseButton.LEFT:
        print(f"Target is at: x={event.xdata},y={event.ydata}")
        target_x = event.xdata
        target_y = event.ydata

plt.connect('button_press_event', on_click)

plt.show()
