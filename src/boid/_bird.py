from ._flyer import Flyer
import numpy as np

class Bird(Flyer):
        
    def coherence(self, b_index, neighb_positions, b_position, c_c):
        return (np.mean(neighb_positions, axis=0) - b_position) * c_c

    def separation(self, b_index, neighb_positions, b_position, c_s):
        return -c_s * np.sum(neighb_positions - b_position, axis=0)
    
    # def separation_from_predator(self, b_index, predator_positions, b_position, c_s):
    #     # Return zero if no predators are nearby
    #     if len(predator_positions) == 0:
    #         return np.zeros(2)

    #     # Compute repulsion from predators
    #     diff = b_position - predator_positions # vector from predators to boid
    #     dist = np.linalg.norm(diff, axis=1) # distances to predators
    #     dist[dist == 0] = 1e-6 # avoid division by zero

    #     return c_s * np.sum(diff / dist[:, None]**2, axis=0) # inverse square law repulsion

    def alignment(self, b_index, neighb_velocities, b_velocity, c_a):
        return c_a * (np.mean(neighb_velocities, axis=0) - b_velocity)

    def __init__(self, p, v, dt=0.1) -> None:
        super().__init__(p, v, dt=0.1)
        print("In Bird")

# 