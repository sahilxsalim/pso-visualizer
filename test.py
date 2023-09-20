import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
from matplotlib.backend_bases import MouseButton

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

# Evaluate fitness
def evaluate(particle):
    x, y = particle
    return (x-2)**2 + (y - 3)**2

# Initialize plot
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
particle_handles, = ax.plot(particles[:, 0], particles[:, 1], 'ro')

def animate(i):
    global global_best

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
        particles[j] = np.clip(particles[j], -10, 10)

    # Update plot
    particle_handles.set_data(particles[:, 0], particles[:, 1])

    return particle_handles,

ani = animation.FuncAnimation(fig, animate, frames=iters, interval=100)

# def on_click(event):
#     if event.button is MouseButton.LEFT:
#         print(event.xdata,event.ydata)


# plt.connect('button_press_event', on_click)
plt.show()
