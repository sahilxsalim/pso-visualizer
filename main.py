from math import sqrt
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
from matplotlib.backend_bases import MouseButton
import matplotlib
from collections import deque
import tkinter as tk
from tkinter import ttk

# Initialize trail history
trail_history = deque(maxlen=100)

target_x = 0
target_y = 0

num_particles = 50
dimensions = 2
iters = 1000
found_iter = -1
# Initialize a list to store error values for each iteration
error_history = []

# Function to calculate the error between global best and target
def calculate_error(global_best):
    return sqrt((global_best[0] - target_x) ** 2 + (global_best[1] - target_y) ** 2)

# PSO parameters (initial values)
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

# Initialize Tkinter window
root = tk.Tk()
root.title("PSO Parameters")

# Function to update PSO parameters
def update_parameters():
    global w_max, w_min, c1, c2, num_particles
    w_max = float(w_max_entry.get())
    w_min = float(w_min_entry.get())
    c1 = float(c1_entry.get())
    c2 = float(c2_entry.get())
    num_particles = int(num_particles_entry.get())

# Label and entry widgets for PSO parameters
param_frame = ttk.Frame(root)
param_frame.pack()

ttk.Label(param_frame, text="Number of Particles").grid(row=0, column=0)
num_particles_entry = ttk.Entry(param_frame)
num_particles_entry.grid(row=0, column=1)
num_particles_entry.insert(0, str(num_particles))

ttk.Label(param_frame, text="Max Inertia Weight (w_max):").grid(row=1, column=0)
w_max_entry = ttk.Entry(param_frame)
w_max_entry.grid(row=1, column=1)
w_max_entry.insert(0, str(w_max))

ttk.Label(param_frame, text="Min Inertia Weight (w_min):").grid(row=2, column=0)
w_min_entry = ttk.Entry(param_frame)
w_min_entry.grid(row=2, column=1)
w_min_entry.insert(0, str(w_min))

ttk.Label(param_frame, text="Cognitive Coefficient (c1):").grid(row=3, column=0)
c1_entry = ttk.Entry(param_frame)
c1_entry.grid(row=3, column=1)
c1_entry.insert(0, str(c1))

ttk.Label(param_frame, text="Social Coefficient (c2):").grid(row=4, column=0)
c2_entry = ttk.Entry(param_frame)
c2_entry.grid(row=4, column=1)
c2_entry.insert(0, str(c2))

update_button = ttk.Button(param_frame, text="Update Parameters", command=update_parameters)
update_button.grid(row=5, columnspan=2)
 
def animate(i):
    global global_best
    x_lim = ax.get_xlim() 
    y_lim = ax.get_ylim()
    ax.cla()
    ax.set_title('Particle Swarm Optimization Visualization')

    ax.set_xlim(x_lim) 
    ax.set_ylim(y_lim)
    best_fitness = evaluate(global_best) 
    

    # Update inertia weight (linearly decreasing)
    w = w_max - (w_max - w_min) * i / iters
    if best_fitness<0.001:
        global found_iter
        found_iter = i if found_iter==-1 else found_iter
        print("Found at ",found_iter)
        i = found_iter
        ax.text(0.05, 0.70, 'Found at Iteration: %d' % found_iter, transform=ax.transAxes)  
    ax.text(0.05, 0.9, 'Iter: %d' % i, transform=ax.transAxes)  
    ax.text(0.05, 0.85, 'Target: (%.4f, %.4f)' % (target_x, target_y), 
        transform=ax.transAxes)
    ax.text(0.05, 0.8, 'Best Fitness: %.4f' % best_fitness, 
          transform=ax.transAxes)
    ax.text(0.05, 0.75, 'Global Best: (%.4f, %.4f)' % (global_best[0],global_best[1]), 
          transform=ax.transAxes)
    # Update particle velocities and positions
    # Calculate the error and store it in the history
    error = calculate_error(global_best)
    error_history.append(error)
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
    # while len(particle_trails)>max_trail_length:
    #         particle_trails.pop(0)  # Remove the oldest positions
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

# Start the animation
ani = animation.FuncAnimation(fig, animate, frames=iters, interval=40)

# Function to handle button click event
def on_click(event):
    global target_x, target_y, found_iter, particles, velocities, global_best
    if event.button is MouseButton.LEFT:
        print(f"Target is at: x={event.xdata},y={event.ydata}")
        target_x = event.xdata
        target_y = event.ydata
        particle_trails.clear()
        found_iter = -1
        ani.frame_seq = ani.new_frame_seq()
        particles = np.random.uniform(-2, 2, size=(num_particles, dimensions))
        velocities = np.zeros((num_particles, dimensions))
        global_best = particles[0].copy()

plt.connect('button_press_event', on_click)
# Update plot
# 
particle_handles.set_data(particles[:, 0], particles[:, 1]) 

# Plot global best
# ax.plot(global_best[0], global_best[1], 'bo', markersize=10)
# Plot target 
ax.plot(target_x, target_y, 'xk', markersize=10)
# Create a new figure for the error plot
fig_error, ax_error = plt.subplots()
ax_error.set_title('Error between Global Best and Target')
ax_error.set_xlabel('Iteration')
ax_error.set_ylabel('Error')
error_line, = ax_error.plot([], [], 'b-')

def animate_error(i):
    # Update the error plot
    error_line.set_data(range(len(error_history)), error_history)
    ax_error.relim()
    ax_error.autoscale_view()

# Create an animation for the error plot
ani_error = animation.FuncAnimation(fig_error, animate_error, frames=iters, interval=40)

# Rest of your code remains the same

plt.show()
root.mainloop()
