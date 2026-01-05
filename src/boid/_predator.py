from ._flyer import Flyer
import numpy as np

class Predator(Flyer):
        
    def coherence(self, b_index, neighb_positions, b_position, c_c):
        '''
        Docstring for coherence
        
        :param self: Description
        :param b_index: Description
        :param neighb_positions: Description
        :param b_position: Description
        :param c_c: Description
        '''
        return (np.mean(neighb_positions, axis=0) - b_position) * c_c
    
    def separation(self, b_index, neighb_positions, b_position, c_s, ):
        '''
        Docstring for separation
        
        :param self: Description
        :param b_index: Description
        :param neighb_positions: Description
        :param b_position: Description
        :param c_s: Description
        '''
        return -c_s * np.sum(neighb_positions - b_position, axis=0)

    def __init__(self, p, v, dt=0.1, eaten=False, cooldown=0) -> None:
        '''
        Docstring for __init__
        
        :param self: Description
        :param p: Description
        :param v: Description
        :param dt: Description
        :param eaten: Description
        :param cooldown: Description
        '''
        super().__init__(p, v, dt=0.1)
        self.eaten = eaten
        self.cooldown = cooldown
        print("In Predator")
