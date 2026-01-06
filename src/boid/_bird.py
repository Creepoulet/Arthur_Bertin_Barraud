from ._flyer import Flyer
import numpy as np

class Bird(Flyer):
        
    def coherence(self, neighb_positions:np.ndarray, b_position:np.ndarray, c_c:float) -> np.ndarray:
        """
        Compute the coherence of the boid based on the position of its neighbours and its own 

        Args:
            b_index: Index specific to each boid
            neighb_positions: The positions of the neighbours of the boid
            b_position : The position of the boid
            c_c: coefficient of coherence (it's "strenght")
        """
        return (np.mean(neighb_positions, axis=0) - b_position) * c_c

    def separation(self, neighb_positions:np.ndarray, b_position:np.ndarray, c_s:float) -> np.ndarray:
        """
        Compute the separation of the boid based on the position of its neighbours and its own 

        Args:
            b_index: Index specific to each boid
            neighb_positions: The positions of the neighbours of the boid
            b_position : The position of the boid
            c_s: coefficient of separation (it's "strenght")
        """
        return -c_s * np.sum(neighb_positions - b_position, axis=0)
    
    def alignment(self, neighb_velocities:np.ndarray, b_velocity:np.ndarray, c_a:float) -> np.ndarray:
        """
        Compute the alignment of the boid based on the position of its neighbours and its own 

        Args:
            b_index: Index specific to each boid
            neighb_positions: The positions of the neighbours of the boid
            b_position : The position of the boid
            c_a: coefficient of alignment (it's "strenght")
        """
        return c_a * (np.mean(neighb_velocities, axis=0) - b_velocity)

    def __init__(self, p:np.ndarray, v:np.ndarray, dt:float=0.1) -> None:
        super().__init__(p, v, dt=0.1)
        print("In Bird")

# 