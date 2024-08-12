import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import simpledialog

class Particle:
    def __init__(self, particle_id, x, y):
        self.id = particle_id
        self.x = x
        self.y = y

class NeighborData:
    def __init__(self):
        self.neighbors = {}

    def add_neighbors(self, particle_id, neighbors):
        self.neighbors[particle_id] = neighbors

    def get_neighbors(self, particle_id):
        return self.neighbors.get(particle_id, [])
    

class ParticleVisualizer:
    def __init__(self, particles, neighbor_data):
        self.particles = particles
        self.neighbor_data = neighbor_data
        self.fig, self.ax = plt.subplots()
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
            elif particle.id in neighbors:
                self.ax.plot(particle.x, particle.y, 'ro')  # Neighbors in red
            else:
                self.ax.plot(particle.x, particle.y, 'bo')  # Other particles in blue
        plt.draw()

    def visualize(self):
        for particle in self.particles:
            self.ax.plot(particle.x, particle.y, 'bo')  # Plot all particles in blue

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()

