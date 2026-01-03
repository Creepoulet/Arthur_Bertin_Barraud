from ._predator import Predator
from ._bird import Bird
from scipy.spatial import KDTree
import numpy as np
import matplotlib.pyplot as plt
import pygame


class Flock:

    def show_flock(self, step=1):
        print("In show_flock")
        pygame.init()

        # Set up display
        width, height = 1200, 700
        pygame.display.set_caption("Boids")
        screen = pygame.display.set_mode((width, height))
        # Define colors
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)

        # Triangle properties
        scale = 10

        running = True

        while running:
            self.move_flock(n=step)
            # Making sure that we stop the program when the user closes the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(black)

            for b in self.boid_list:
                current_pos = b.position
                velocity = b.velocity
                if current_pos[0] < 0 or current_pos[0] > width:
                    current_pos[0] = current_pos[0] % width
                if current_pos[1] < 0 or current_pos[1] > height:
                    current_pos[1] = current_pos[1] % height
                direction = (velocity) / np.linalg.norm(velocity)

                ## A, B and C will be the points of the triangle
                C = current_pos + scale * direction
                A = (
                    current_pos[0] + 3 * direction[1],
                    current_pos[1] - 3 * direction[0],
                )
                B = (
                    current_pos[0] - 3 * direction[1],
                    current_pos[1] + 3 * direction[0],
                )
                pygame.draw.polygon(screen, white, [A, B, C])

            for p in self.predator_list:
                current_posp = p.position
                velocityp = p.velocity
                # if current_posp[0] < 0 or current_posp[0] > width:
                #     current_posp[0] = current_posp[0] % width
                # if current_posp[1] < 0 or current_posp[1] > height:
                #     current_posp[1] = current_posp[1] % height
                # directionp = (velocityp) / np.linalg.norm(velocityp)

                # make them bounce on the walls
                if current_posp[0] < 0 or current_posp[0] > width:
                    velocityp[0] = -velocityp[0]
                if current_posp[1] < 0 or current_posp[1] > height:
                    velocityp[1] = -velocityp[1]
                if (current_posp[0] < 0 or current_posp[0] > width) and (current_posp[1] < 0 or current_posp[1] > height):
                    velocityp = -velocityp
                directionp = (velocityp) / np.linalg.norm(velocityp)

                ## A, B and C will be the points of the triangle
                Cp = current_posp + scale * directionp
                Ap = (
                    current_posp[0] + 3 * directionp[1],
                    current_posp[1] - 3 * directionp[0],
                )
                Bp = (
                    current_posp[0] - 3 * directionp[1],
                    current_posp[1] + 3 * directionp[0],
                )
                pygame.draw.polygon(screen, red, [Ap, Bp, Cp])

            # Shuffling the speed
            # Update the display
            pygame.display.flip()

            # Frame rate
            pygame.time.Clock().tick(60)
        pygame.quit()

    def move_flock(self, n=1): 
        for _ in range(n):
            self.one_step_move_boid()
            self.one_step_move_predator()

    
    def find_neighbourhood(self, positions, r=None):
        if r is None:
            r = self.r
        kdtree = KDTree(positions)
        neighbs = kdtree.query_ball_point(positions, r=r, return_sorted=True)
        return neighbs

    def get_all_neighbours(self):

        # boids
        positions_b = np.array([b.position for b in self.boid_list])
        velocities_b = np.array([b.velocity for b in self.boid_list])

        neighbs = self.find_neighbourhood(positions_b, r=self.r)
        self.neighb_positions = {i: positions_b[n] for i, n in enumerate(neighbs)}
        self.neighb_velocities = {i: velocities_b[n] for i, n in enumerate(neighbs)}

        neighbs = self.find_neighbourhood(positions_b, r=self.r_repulsion)
        self.neighb_positions_repulsion = {i: positions_b[n] for i, n in enumerate(neighbs)}

        # predators
        positions_p = np.array([p.position for p in self.predator_list]) # get positions of predators
        velocities_p = np.array([p.velocity for p in self.predator_list]) # get velocities of predators

        neighbs_p = self.find_neighbourhood(positions_p, r=self.r_pred) # find neighbours for predators
        self.neighb_positions_pred = {i: positions_b[n] for i, n in enumerate(neighbs_p)} # positions of boids around each predator
        self.neighb_velocities_pred = {i: velocities_b[n] for i, n in enumerate(neighbs_p)} # velocities of boids around each predator

        tree_pred = KDTree(positions_p)
        neighbs_pred = tree_pred.query_ball_point(positions_b, r=self.r_pred)

        self.neighb_positions_repulsion_pred = {i: positions_p[n] for i, n in enumerate(neighbs_pred)}

        

    def one_step_move_boid(self):
        for b in self.boid_list:
            b.move_flyer(dt=self.dt)

        self.get_all_neighbours()
        new_velocity = []
        for b_index, b in enumerate(self.boid_list):
            C = b.coherence(b_index, self.neighb_positions[b_index], self.boid_list[b_index].position, self.c_c)
            S = b.separation(b_index, self.neighb_positions_repulsion[b_index], self.boid_list[b_index].position, self.c_s)
            Sp = b.separation_from_predator(b_index, self.neighb_positions_repulsion_pred[b_index],self.boid_list[b_index].position,self.c_s_pred)
            A = b.alignment(b_index, self.neighb_velocities[b_index], self.boid_list[b_index].velocity, self.c_a)
            new_velocity.append(b.velocity + self.dt * (C + S + A + Sp))
        for b, new_v in zip(self.boid_list, new_velocity):
            b.velocity = new_v


    # Corriger les prédateurs en l'état ça va pas du tout ils vont super vite pour rien
    def one_step_move_predator(self):
        for p in self.predator_list:
            p.move_flyer(dt=self.dt)

        self.get_all_neighbours()
        new_velocity = []
        for b_index, p in enumerate(self.predator_list):
            C = p.coherence(b_index, self.neighb_positions_pred[b_index], p.position, self.c_c)
            # S = p.separation(b_index, self.neighb_positions_repulsion[b_index], p.position, self.c_s)
            # A = (p.alignment(b_index, self.neighb_velocities[b_index], p.velocity, self.c_a)) *1.5
            new_velocity.append(p.velocity + self.dt * (C))
        for p, new_v in zip(self.predator_list, new_velocity):
            p.velocity = new_v

    def __init__(self, nb_boids=50, nb_predators=1, c_c=.001, c_s=.01, c_s_pred=5, c_a=.01, r=100, r_repulsion=20, r_pred = 200, dt = 1.5, seed=0):
        
        np.random.seed(seed)
        
        # Create boid and predator lists
        self.boid_list = [
            Bird(500 + np.random.rand(2) * 100 - 50, 2*np.random.rand(2)-1)
            for _ in range(nb_boids)
        ]

        self.predator_list = [
            Predator(500 + np.random.rand(2) * 100 - 50, 2*np.random.rand(2)-1) for _ in range(nb_predators)
        ]

        # Flocking parameters
        self.c_c = c_c
        self.c_s = c_s
        self.c_s_pred = c_s_pred
        self.c_a = c_a
        self.r = r
        self.r_repulsion = r_repulsion
        self.r_pred = r_pred
        self.dt = dt
        print("In Flock")