from ._flyer import Flyer
import numpy as np

class Predator(Flyer):
        
    def coherence(self, neighb_positions, b_position, c_c):
        """
        Compute the coherence of the predator based on the position of its neighbours and its own

        Args:
            b_index: Index specific to each boid
            neighb_positions: The positions of the neighbours of the boid
            b_position : The position of the boid
            c_c: coefficient of coherence (it's "strenght")
        """
        return (np.mean(neighb_positions, axis=0) - b_position) * c_c
    
    def separation(self, neighb_positions, b_position, c_s, ):
        """
        Compute the separation of the predator based on the position of its neighbours and its own 

        Args:
            b_index: Index specific to each boid
            neighb_positions: The positions of the neighbours of the boid
            b_position : The position of the boid
            c_s: coefficient of separation (it's "strenght")
        """
        return -c_s * np.sum(neighb_positions - b_position, axis=0)

    def __init__(self, p, v, dt=0.1, eaten=False, cooldown=0) -> None:
        super().__init__(p, v, dt=0.1)
        self.eaten = eaten
        self.cooldown = cooldown
        print("In Predator")
