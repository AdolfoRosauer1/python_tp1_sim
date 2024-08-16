import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from matplotlib.backend_bases import MouseEvent
from typing import List, Dict, Optional

class Particle:
    """
    Represents a particle with an ID, position (x, y), and a radius.

    Attributes:
        id (int): Unique identifier for the particle.
        x (float): X-coordinate of the particle.
        y (float): Y-coordinate of the particle.
        radius (float): Radius of the particle.
    """

    def __init__(self, particle_id: int, x: float, y: float, radius: float) -> None:
        """
        Initializes a Particle instance.

        Args:
            particle_id (int): The unique ID for the particle.
            x (float): The X-coordinate of the particle.
            y (float): The Y-coordinate of the particle.
            radius (float): The radius of the particle.
        """
        self.id = particle_id
        self.x = x
        self.y = y
        self.radius = radius

class NeighborData:
    """
    Manages the neighbor relationships between particles.

    Attributes:
        neighbors (Dict[int, List[int]]): A dictionary where the key is a particle's ID
                                          and the value is a list of IDs of neighboring particles.
    """

    def __init__(self) -> None:
        """Initializes the NeighborData instance with an empty neighbor dictionary."""
        self.neighbors: Dict[int, List[int]] = {}

    def add_neighbors(self, particle_id: int, neighbors: List[int]) -> None:
        """
        Adds a list of neighboring particle IDs for a specific particle.

        Args:
            particle_id (int): The ID of the particle.
            neighbors (List[int]): A list of IDs representing neighboring particles.
        """
        self.neighbors[particle_id] = neighbors

    def get_neighbors(self, particle_id: int) -> List[int]:
        """
        Retrieves the list of neighbors for a given particle.

        Args:
            particle_id (int): The ID of the particle.

        Returns:
            List[int]: A list of IDs of neighboring particles. Returns an empty list if no neighbors are found.
        """
        return self.neighbors.get(particle_id, [])

class ParticleVisualizer:
    """
    Visualizes a collection of particles and their neighbor relationships.

    Attributes:
        particles (List[Particle]): The list of particles to visualize.
        neighbor_data (NeighborData): The neighbor data managing particle relationships.
        Rc (float): An optional value to represent an additional radius circle around the selected particle.
        fig (plt.Figure): The matplotlib figure used for plotting.
        ax (plt.Axes): The matplotlib axes used for plotting.
        selected_particle (Optional[int]): The ID of the currently selected particle.
    """

    def __init__(self, particles: List[Particle], neighbor_data: NeighborData, Rc: float = 0) -> None:
        """
        Initializes the ParticleVisualizer instance.

        Args:
            particles (List[Particle]): A list of Particle instances to visualize.
            neighbor_data (NeighborData): An instance of NeighborData for managing particle relationships.
            Rc (float, optional): An additional radius value to draw around the selected particle. Defaults to 0.
        """
        self.particles = particles
        self.neighbor_data = neighbor_data
        self.Rc = Rc  # Rc value to be used for drawing the additional circle
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal', 'box')  # Set the aspect ratio to 1:1
        self.selected_particle: Optional[int] = None

    def on_click(self, event: MouseEvent) -> None:
        """
        Event handler for mouse click events on the plot.

        Args:
            event (plt.MouseEvent): The mouse event triggered by clicking on the plot.
        """
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            closest_particle = min(self.particles, key=lambda p: (p.x - x) ** 2 + (p.y - y) ** 2)
            self.selected_particle = closest_particle.id
            self.highlight_neighbors()

    def highlight_neighbors(self) -> None:
        """
        Highlights the selected particle and its neighbors on the plot.
        Draws a circle around the selected particle's radius and optionally around its radius plus Rc.
        """
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

    def visualize(self) -> None:
        """
        Initiates the visualization of particles and their interactions.
        Plots all particles, connects the plot to mouse click events, and displays the plot.
        """
        for particle in self.particles:
            self.ax.plot(particle.x, particle.y, 'bo')  # Plot all particles in blue

        self.ax.set_aspect('equal', 'box')  # Ensure 1:1 aspect ratio on initial plot
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()
