from classes import Particle, NeighborData, ParticleVisualizer


def load_particles(file_path):
    particles = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        N = int(lines[0].strip())  # Number of particles
        L = float(lines[1].strip())  # Length of the area

        for line in lines[2:]:
            parts = line.strip().split()
            particle_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            particles.append(Particle(particle_id, x, y))
    return particles

def load_neighbors(file_path):
    neighbor_data = NeighborData()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            particle_id = int(parts[0])
            neighbors = list(map(int, parts[1:]))
            neighbor_data.add_neighbors(particle_id, neighbors)
    return neighbor_data


def main():
    particles = load_particles(r'C:\Users\juana\Documents\ITBA\current\sim\tp1_SIM\static_particles.txt')
    neighbor_data = load_neighbors(r'C:\Users\juana\Documents\ITBA\current\sim\tp1_SIM\neighbors.txt')

    visualizer = ParticleVisualizer(particles, neighbor_data)
    visualizer.visualize()

if __name__ == "__main__":
    main()
