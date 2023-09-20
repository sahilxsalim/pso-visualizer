from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
from matplotlib.backend_bases import MouseButton
import matplotlib
from collections import deque

# Initialize trail history 
trail_history = deque(maxlen=100) 

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
max_trail_length = 50

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
    ax.set_title('Particle Swarm Optimization Visualization')

    ax.set_xlim(x_lim) 
    ax.set_ylim(y_lim)
    best_fitness = evaluate(global_best) 
  
    # ax.text(0.05, 0.9, 'Iter: %d' % i, transform=ax.transAxes)  
    ax.text(0.05, 0.85, 'Target: (%.4f, %.4f)' % (target_x, target_y), 
        transform=ax.transAxes)
    ax.text(0.05, 0.8, 'Best Fitness: %.4f' % best_fitness, 
          transform=ax.transAxes)
    ax.text(0.05, 0.75, 'Global Best: (%.4f, %.4f)' % (global_best[0],global_best[1]), 
          transform=ax.transAxes)
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
    # if len(particle_trails) > max_trail_length:
    #     print('d')
        # while len(particle_trails):
        #     particle_trails.pop()  # Remove the oldest positions
    while len(particle_trails)>max_trail_length:
            particle_trails.pop(0)  # Remove the oldest positions
    # Update plot
    particle_handles.set_data(particles[:, 0], particles[:, 1])
    ax.plot(target_x, target_y, 'xk') # Add target marker
    
    ax.plot(global_best[0], global_best[1], 'bo')
    # Plot particle trails as lines
    if len(particle_trails) > 1:
        # print(len(particle_trails))
        cmap = plt.get_cmap('RdYlGn')
        # Append current trails
        trail_history.append(particles.copy())  
        for j in range(num_particles):
            # Only plot the last 50 trail positions
            trail = np.array(particle_trails)[10:, j, :]
            # Fade color
            cmap = plt.get_cmap('RdYlGn') 
            norm = matplotlib.colors.Normalize(vmin=0, vmax=max_trail_length)
            color = cmap(norm(len(particle_trails)))
            
            ax.plot(trail[:, 0], trail[:, 1], color=color)


    return particle_handles,

ani = animation.FuncAnimation(fig, animate, frames=iters, interval=40)

def on_click(event):
    global target_x, target_y
    if event.button is MouseButton.LEFT:
        print(f"Target is at: x={event.xdata},y={event.ydata}")
        target_x = event.xdata
        target_y = event.ydata
        particle_trails.clear()

plt.connect('button_press_event', on_click)
# Update plot
# 
particle_handles.set_data(particles[:, 0], particles[:, 1]) 

# Plot global best
ax.plot(global_best[0], global_best[1], 'bo', markersize=10)
# Plot target 
ax.plot(target_x, target_y, 'xk', markersize=10)
plt.show()