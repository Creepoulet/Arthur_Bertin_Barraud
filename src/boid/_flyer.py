import numpy as np
import matplotlib.pyplot as plt

class Flyer:

    # Because the acceleration is a function of the velocity,
    # it is not needed as an argument to the constructor anymore

    # The acceleration is now a property
    @property
    def acceleration(self):
        if not hasattr(self, "_acceleration"):
            self._acceleration = np.zeros_like(self.velocity)
        return self._acceleration

    @acceleration.setter
    def acceleration(self, value):
        self._acceleration = np.array(value, dtype=float)

    def update_velocity(self, *, dt: float) -> None:
        """
        Update the velocity of the boid based on its acceleration

        Args:
            dt: The time step for the simulation
        """
        new_velocity = self.velocity + self.acceleration*dt
        self.velocity = new_velocity
        ...

    def move_flyer(self, *, dt: float) -> None:
        """
        Move the boid based on its velocity

        Args:
            dt: The time step for the simulation
        """
        # new_position = self.position + self.velocity*dt 
        # self.position = new_position
        # self.update_velocity(dt=dt)

        # if not np.all(np.isfinite(self.velocity)):
        # self.velocity = np.zeros_like(self.velocity)

        # update position
        self.position = self.position + self.velocity * dt

        # If the position contains NaN or Inf, reset it to zero
        if not np.all(np.isfinite(self.position)):
            self.position = np.nan_to_num(self.position)

        self.update_velocity(dt=dt)
        ...

    def plot_trajectory(self, *, dt: float, num_steps: int) -> None:
        """
        Plot the trajectory of the boid

        Args:
            dt: The time step for the simulation
            num_steps: The number of steps to simulate
        """
        traj = []
        for _ in range(num_steps):
            self.move_flyer(dt=dt)
            traj.append(self.position)
        traj = np.array(traj)
        fig, ax = plt.subplots()
        ax.plot(*traj.T, "o-")
        ax.set_aspect("equal")
        ...

    #truc pour qu'ils évitent les bords de l'écran 


    def __init__(self, p, v, dt=0.1) -> None:
        self.position = np.array(p, dtype=float)
        self.velocity = np.array(v, dtype=float)
        print("In Flyer")
