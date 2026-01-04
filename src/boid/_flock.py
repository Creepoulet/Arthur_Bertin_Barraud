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

        # Triangle properties
        scale = 10

        running = True

        pygame.font.init()
        font = pygame.font.SysFont("calibri", 30)
        font_cd = pygame.font.SysFont("calibri", 20)
        font_eaten = pygame.font.SysFont("calibri", 10, bold=True)

        # Candy Crush reference
        eat_message = ["Divine !", "Sweet !", "Tasty !", "Delicious !", "Yummy !", "Scrumptious !", "Superb !"]

        while running:
            self.move_flock(n=step)

            # Making sure that we stop the program when the user closes the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(black)

            for p in self.predator_list:
                current_posp = p.position
                velocityp = p.velocity

                # make them go from one side of the screen to the other
                if current_posp[0] < 0 or current_posp[0] > width:
                    current_posp[0] = current_posp[0] % width
                if current_posp[1] < 0 or current_posp[1] > height:
                    current_posp[1] = current_posp[1] % height
                directionp = (velocityp) / np.linalg.norm(velocityp)

                # manage cooldown after eating (predator will be slower for a while, cf one_step_move_predator)
                if p.eaten:
                    p.cooldown += 1
                    if p.cooldown >= 180: # cooldown of 3 seconds at 60 fps
                        p.eaten = False
                        p.cooldown = 0

                # If they are on the same position as a boid, decrease their speed
                if any(np.linalg.norm(current_posp - b.position) < 10 for b in self.boid_list):
                    p.velocity *= 0.2

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

                # Color the predator differently if it has eaten recently
                if p.eaten:
                    color_pred = (0, 255, 0)
                else:
                    color_pred = (255, 0, 0)
                pygame.draw.polygon(screen, color_pred, [Ap, Bp, Cp])

            for b in self.boid_list:
                current_pos = b.position
                velocity = b.velocity

                # delete boids that are in the same position as predators
                for p in self.predator_list:
                    if np.linalg.norm(current_pos - p.position) < 10 and not p.eaten:
                        self.boid_list.remove(b)
                        p.eaten = True
                        self.score += 1
                        eat_text = font.render(eat_message[np.random.randint(0, 7)], True, "yellow")
                        self.eat_texts.append((eat_text, current_pos.copy(), pygame.time.get_ticks(), 1500))
                        break

                # make them go from one side of the screen to the other
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

            current_time = pygame.time.get_ticks()
            texts_to_remove = []

            for text_displayed, pos, start_time, duration in self.eat_texts:
                # Compute opacity based on elapsed time
                elapsed = current_time - start_time
                if elapsed < duration:
                    # Decrease alpha over time
                    alpha = max(0, 255 - (elapsed / duration) * 255)
                    text_displayed.set_alpha(alpha)  # Set the alpha value
                    screen.blit(text_displayed, pos)
                else:
                    texts_to_remove.append((text_displayed, pos, start_time, duration)) # Append to removal list

            # Delete texts that have finished their duration (that have been appended to the removal list)
            for text in texts_to_remove:
                self.eat_texts.remove(text)
            
            # Display number of boids that have been eaten
            score_text = font.render(f"Birds predated: {self.score}", True, white)
            screen.blit(score_text, (10, 10))
            for p_index, p in enumerate(self.predator_list):
                if p.eaten:
                    cooldown_text = font_cd.render(f"Predator {p_index+1} cooldown: {3-(p.cooldown/60):.2f}s", True, white)
                    screen.blit(cooldown_text, (10, 40 + 30 * p_index))

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

        # positions and velocity of boids around boids
        positions_b = np.array([b.position for b in self.boid_list])
        velocities_b = np.array([b.velocity for b in self.boid_list])

        neighbs = self.find_neighbourhood(positions_b, r=self.r)
        self.neighb_positions = {i: positions_b[n] for i, n in enumerate(neighbs)}
        self.neighb_velocities = {i: velocities_b[n] for i, n in enumerate(neighbs)}

        neighbs = self.find_neighbourhood(positions_b, r=self.r_repulsion)
        self.neighb_positions_repulsion = {i: positions_b[n] for i, n in enumerate(neighbs)}

        # positions of boids around predators
        positions_p = np.array([p.position for p in self.predator_list]) # get positions of predators   
     
        tree_boids = KDTree(positions_b)
        neighbs_pred = tree_boids.query_ball_point(positions_p, r=self.r_pred)

        self.neighb_positions_pred = {i: positions_b[n] for i, n in enumerate(neighbs_pred)}   

        # positions of predators around predators for repulsion
        neighbs_p = self.find_neighbourhood(positions_p, r=self.r_repulsion*4) # find neighbours for predators at range of repulsion
        self.neighb_positions_pred_pred = {i: positions_p[n] for i, n in enumerate(neighbs_p)} 
        
        # positions of predators around boids for repulsion
        tree_pred = KDTree(positions_p)
        neighbs_pred_rep = tree_pred.query_ball_point(positions_b, r=self.r_repulsion*1.5)

        self.neighb_positions_repulsion_pred = {i: positions_p[n] for i, n in enumerate(neighbs_pred_rep)}

        

    def one_step_move_boid(self):
        for b in self.boid_list:
            b.move_flyer(dt=self.dt)

        self.get_all_neighbours()
        new_velocity = []
        for b_index, b in enumerate(self.boid_list):
            C = b.coherence(b_index, self.neighb_positions[b_index], self.boid_list[b_index].position, self.c_c)
            S = b.separation(b_index, self.neighb_positions_repulsion[b_index], self.boid_list[b_index].position, self.c_s)
            Sp = b.separation(b_index, self.neighb_positions_repulsion_pred[b_index],self.boid_list[b_index].position,self.c_s_pred)
            A = b.alignment(b_index, self.neighb_velocities[b_index], self.boid_list[b_index].velocity, self.c_a)
            new_velocity.append(b.velocity + self.dt * (C + S + A + Sp))
        for b, new_v in zip(self.boid_list, new_velocity):
            if np.linalg.norm(new_v) > 5:
                b.velocity = (new_v / np.linalg.norm(new_v)) * 5
            else:
                b.velocity = new_v


    # Corriger les prédateurs en l'état ça va pas du tout ils vont super vite pour rien
    def one_step_move_predator(self):
        for p in self.predator_list:
            p.move_flyer(dt=self.dt)

        self.get_all_neighbours()
        new_velocity = []
        for b_index, p in enumerate(self.predator_list):
            # compute coherence only if there are boids in sight. Added to avoir NaN errors and predator staying stuck out of the screen with NaN velocity.
            if b_index in self.neighb_positions_pred and len(self.neighb_positions_pred[b_index]) > 0:
                C = p.coherence(b_index, self.neighb_positions_pred[b_index], p.position, self.c_c*2)
            else:
                C = np.zeros(2)
            # compute separation from other predators so that they don't stack and stay less in the same place
            # S = p.separation(b_index, self.neighb_positions_pred_pred[b_index], p.position, self.c_s)
            if b_index in self.neighb_positions_pred_pred and len(self.neighb_positions_pred_pred[b_index]) > 0:
                S = p.separation(b_index, self.neighb_positions_pred_pred[b_index], p.position, self.c_c*2)
            else:
                S = np.zeros(2)
            new_velocity.append(p.velocity + self.dt * (C + S))
        
        for p, new_v in zip(self.predator_list, new_velocity):

            # limit the speed of the predator depending on whether it has eaten or not
            if p.eaten==True:
                max_speed = 1
            else:
                max_speed = 8

            #limit the acceleration of the predator
            if np.linalg.norm(new_v - p.velocity) > 1:
                new_v = p.velocity + (new_v - p.velocity) / np.linalg.norm(new_v - p.velocity) * 2

            # limit the speed of the predator
            if np.linalg.norm(new_v) > max_speed:
                p.velocity = (new_v / np.linalg.norm(new_v)) * max_speed
            else:
                p.velocity = new_v

    def __init__(self, nb_boids=100, nb_predators=2, c_c=.001, c_s=.01, c_s_pred=5, c_a=.01, r=100, r_repulsion=20, r_pred = 200, score=0, dt = 1.5, seed=0):
        
        np.random.seed(seed)
        
        # Create boid and predator lists
        self.boid_list = [
            Bird(500 + np.random.rand(2) * 100 - 50, 2*np.random.rand(2)-1)
            for _ in range(nb_boids)
        ]

        self.predator_list = [
            # predators start at the edges
            Predator(np.random.rand(2) * np.array([1200, 700]), 2*np.random.rand(2)-1) for _ in range(nb_predators)
        ]

        # Flocking parameters
        self.c_c = c_c
        self.c_s = c_s
        self.c_s_pred = c_s_pred
        self.c_a = c_a
        self.r = r
        self.r_repulsion = r_repulsion
        self.r_pred = r_pred
        self.score = score
        self.eat_texts = []
        self.dt = dt
        print("In Flock")