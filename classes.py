import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

class Particle:
    def __init__(self, particle_id, x, y, radius):
        self.id = particle_id
        self.x = x
        self.y = y
        self.radius = radius

class NeighborData:
    def __init__(self):
        self.neighbors = {}

    def add_neighbors(self, particle_id, neighbors):
        self.neighbors[particle_id] = neighbors

    def get_neighbors(self, particle_id):
        return self.neighbors.get(particle_id, [])

class ParticleVisualizer:
    def __init__(self, particles, neighbor_data, Rc=0):
        self.particles = particles
        self.neighbor_data = neighbor_data
        self.Rc = Rc  # Rc value to be used for drawing the additional circle
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal', 'box')  # Set the aspect ratio to 1:1
        self.selected_particle = None

    def on_click(self, event):
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            closest_particle = min(self.particles, key=lambda p: (p.x - x) ** 2 + (p.y - y) ** 2)
            self.selected_particle = closest_particle.id
            self.highlight_neighbors()

    def highlight_neighbors(self):
        self.ax.clear()
        neighbors = self.neighbor_data.get_neighbors(self.selected_particle)
        for particle in self.particles:
            if particle.id == self.selected_particle:
                self.ax.plot(particle.x, particle.y, 'go')  # Selected particle in green
                # Draw the circle for the selected particle's radius
                circle = Circle((particle.x, particle.y), particle.radius, color='g', fill=False, linestyle='--', alpha=0.5)
                self.ax.add_patch(circle)
                # Draw the circle representing the area with Rc
                Rc_circle = Circle((particle.x, particle.y), particle.radius + self.Rc, color='r', fill=False, linestyle=':', alpha=0.5)
                self.ax.add_patch(Rc_circle)
            elif particle.id in neighbors:
                self.ax.plot(particle.x, particle.y, 'ro')  # Neighbors in red
            else:
                self.ax.plot(particle.x, particle.y, 'bo')  # Other particles in blue
        self.ax.set_aspect('equal', 'box')  # Keep the aspect ratio after clearing
        plt.draw()

    def visualize(self):
        for particle in self.particles:
            self.ax.plot(particle.x, particle.y, 'bo')  # Plot all particles in blue

        self.ax.set_aspect('equal', 'box')  # Ensure 1:1 aspect ratio on initial plot
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()
