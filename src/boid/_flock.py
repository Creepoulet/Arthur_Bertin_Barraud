from ._predator import Predator
from ._bird import Bird
from scipy.spatial import KDTree
import numpy as np
import matplotlib.pyplot as plt
import pygame


class Flock:

    def show_flock(self, step:int=1) -> None:
        '''
        Display the moving flock using pygame based on the move_flock function.
        Manage the predators eating the boids when being close enough along with the cooldown between each "boid eating".
        Allow the user to pause the simulation.
        
        Args:
            step : Number of iterations of mouvements per frame.
        '''
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

        # Setting the different fonts used to display text
        pygame.font.init()
        font = pygame.font.SysFont("calibri", 30)
        font_cd = pygame.font.SysFont("calibri", 20)
        font_welcome = pygame.font.SysFont("calibri", 200, bold=True)
        font_end = pygame.font.SysFont("calibri", 100, bold=True)

        def load_resize_image(path : str) -> pygame.Surface:
            '''
            Load a resize an image using its path and dividing its dimensions by 3.
            
            Args:
                path : The path leading to the image
            '''
            img = pygame.image.load(path)
            w, h = img.get_size()
            img = pygame.transform.scale(img, (w//3, h//3))
            return img

        # Game variables
        game_paused = False
        pause_time = 0
        unpause_time = 0

        # Candy Crush reference when the predators eat a bird.
        Divine_image = load_resize_image("assets/Divine.png")
        Sweet_image = load_resize_image("assets/Sweet.png")
        Tasty_image = load_resize_image("assets/Tasty.png")
        Delicious_image = load_resize_image("assets/Delicious.png")
        Frogtastic_image = load_resize_image("assets/Frogtastic.png")
        eat_image = [Divine_image, Sweet_image, Tasty_image, Delicious_image, Frogtastic_image]

        # Initiation of countdown variables
        countdown = 3 # decreasing countdown from 3
        countdown_duration = 1000  # each number lasts 1 second
        current_count = countdown

        while running:

            screen.fill(black)

            # Handle countdown display
            time_passed = pygame.time.get_ticks() 
            if time_passed < countdown * countdown_duration:
                # Calculate which number to display, and display it with a fade out
                current_count = countdown - (time_passed // countdown_duration)
                count_time_passed = time_passed % countdown_duration
                if current_count > 0:
                    welcome_text = font_welcome.render(str(current_count), True, white)
                    alpha = max(0, 255 - (count_time_passed / countdown_duration) * 255)
                    welcome_text.set_alpha(alpha)
                    screen.blit(welcome_text, (550, 230))

            # Move the flock only if the game is not paused
            # Display the pause/unpause message.
            if not game_paused:
                if pygame.time.get_ticks() >= 3100:
                    self.move_flock(n=step)
                pause_text = font_cd.render("Press SPACE to pause", True, white)
                screen.blit(pause_text, (1000, 670)) 
            else:
                unpause_text = font_cd.render("Press SPACE to resume", True, white)
                screen.blit(unpause_text, (1000, 670))


            # Making sure that we stop the program when the user closes the window or press escape, and pausing when space is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                # Pausing and unpausing the game is only possible when there is still some birds left
                if len(self.boid_list) > 0:
                    if event.type == pygame.KEYDOWN: # check if a key is pressed
                        if event.key == pygame.K_SPACE: # check if the key is space
                            game_paused = not game_paused # game_paused becomes its opposite
                            if game_paused:
                                pause_time = pygame.time.get_ticks() # store the time when the game is paused
                            else:
                                unpause_time = pygame.time.get_ticks() # store the time when the game is unpaused


            for p in self.predator_list:
                current_posp = p.position
                velocityp = p.velocity

                # Make them go from one side of the screen to the other
                if current_posp[0] < 0 or current_posp[0] > width:
                    current_posp[0] = current_posp[0] % width
                if current_posp[1] < 0 or current_posp[1] > height:
                    current_posp[1] = current_posp[1] % height
                directionp = (velocityp) / np.linalg.norm(velocityp)

                # Manage cooldown after eating (predator will be slower for a while, cf one_step_move_predator)
                if not game_paused:
                    if p.eaten:
                        p.cooldown += 1
                        if p.cooldown >= 180: # cooldown of 3 seconds at 60 fps
                            p.eaten = False
                            p.cooldown = 0

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

                # Delete boids that are in the same position as predators
                for p in self.predator_list:
                    if np.linalg.norm(current_pos - p.position) < 10 and not p.eaten:
                        self.boid_list.remove(b)
                        p.eaten = True
                        self.score += 1 # increment score when a boid is eaten
                        eat_text = eat_image[np.random.randint(0, len(eat_image))] # add eat image when a boid is eaten
                        self.eat_image.append((eat_text, current_pos.copy(), pygame.time.get_ticks(), 1500)) # append image with its position, start time and duration
                        # If there is no bird left, game is paused (avoid crash and trigger end of simulation)
                        if len(self.boid_list) == 0:
                            game_paused = True
                            end_time = pygame.time.get_ticks() # store the time when the game has ended
                        break

                # Make them go from one side of the screen to the other
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

            current_time = pygame.time.get_ticks() + pause_time # current time adjusted for pauses
            img_to_remove = []

            # Display eat images with fading effect
            for i, (img, pos, start_time, duration) in enumerate(self.eat_image):
                # Adjust start_time if the game was paused so that the timing remains consistent
                if game_paused:
                    start_time += (current_time - pause_time)
                else:
                    start_time += unpause_time
                elapsed = current_time - start_time
                if elapsed < duration:
                    alpha = max(0, 255 - (elapsed / duration) * 255) # fade out effect over duration
                    img.set_alpha(alpha)
                    screen.blit(img, pos)
                else:
                    img_to_remove.append(i) # mark image for removal

            # Remove images that have finished displaying
            for i in sorted(img_to_remove, reverse=True):
                del self.eat_image[i]
            
            # Display number of boids that have been eaten, the cooldown of each predator, and the escape message.
            score_text = font.render(f"Birds predated: {self.score}", True, white)
            screen.blit(score_text, (10, 10))
            for p_index, p in enumerate(self.predator_list):
                if p.eaten:
                    cooldown_text = font_cd.render(f"Predator {p_index+1} cooldown: {3-(p.cooldown/60):.2f}s", True, white)
                    screen.blit(cooldown_text, (10, 40 + 30 * p_index))
            
            escape_text = font_cd.render("Press ESCAPE to quit", True, white)
            screen.blit(escape_text, (1025, 10)) 

            # Time for the end message to fade in.
            end_duration = 1500  

            # Manage the end of the simulation.
            # Only instance when the simulation is paused and there is no boid left is when it has ended.
            # Display a black screen with a fade in end message.
            if game_paused and len(self.boid_list) == 0:
                time_passed_after_end = pygame.time.get_ticks() 
                count_time_passed_after_end = time_passed_after_end - end_time
                if time_passed_after_end <= end_duration + end_time:
                    alpha = (count_time_passed_after_end / end_duration) * 255
                else:
                    alpha = 255
                screen.fill(black)
                end_text1 = font_end.render("No bird left", True, white)
                end_text2 = font_end.render("Press ESCAPE to quit", True, white)
                end_text1.set_alpha(alpha)
                end_text2.set_alpha(alpha)
                screen.blit(end_text1, (350, 250))
                screen.blit(end_text2, (190, 350))

                # Hidden messages if you wait 5s after the end then every 2s. Far too long I concede, but I was having fun.
                if time_passed_after_end >= end_duration + end_time + 5000:
                    hidden_text1 = font.render("Still here ?", True, white)
                    screen.blit(hidden_text1, (550, 450))
                    if time_passed_after_end >= end_duration + end_time + 7000:
                        hidden_text2 = font.render("Not much to do uh", True, white)
                        screen.blit(hidden_text2, (20, 20))
                        if time_passed_after_end >= end_duration + end_time + 9000:
                            hidden_text3 = font.render("Now you want to see hom many of them there is", True, white)
                            screen.blit(hidden_text3, (500, 50))
                            if time_passed_after_end >= end_duration + end_time + 11000:
                                hidden_text4 = font.render("Well, this one's not the last", True, white)
                                screen.blit(hidden_text4, (100, 650))
                                if time_passed_after_end >= end_duration + end_time + 13000:
                                    hidden_text5 = font.render("This is a subliminal message...", True, white)
                                    screen.blit(hidden_text5, (50, 540))
                                    if time_passed_after_end >= end_duration + end_time + 15000:
                                        hidden_text5 = font.render("...your are now convinced this project deserve a 20/20", True, white)
                                        screen.blit(hidden_text5, (450, 580))
                                        if time_passed_after_end >= end_duration + end_time + 17000:
                                            hidden_text5 = font.render("Ok now you can go", True, white)
                                            screen.blit(hidden_text5, (200, 150))
                                            if time_passed_after_end >= end_duration + end_time + 19000:
                                                hidden_text5 = font.render("Don't want to leave ?", True, white)
                                                screen.blit(hidden_text5, (700, 130))
                                                if time_passed_after_end >= end_duration + end_time + 21000:
                                                    hidden_text5 = font.render("Fine, I'll do it myself", True, white)
                                                    screen.blit(hidden_text5, (800, 200))
                                                    if time_passed_after_end >= end_duration + end_time + 26000:
                                                        running = False

            # Update the display.
            pygame.display.flip()

            # Frame rate.
            pygame.time.Clock().tick(60)
        pygame.quit()

    def move_flock(self, n:int=1): 
        '''
        Move all the boids
        
        Args:
            n : Number of iterations of mouvements
        '''
        for _ in range(n):
            self.one_step_move_boid()
            self.one_step_move_predator()

    def find_neighbourhood(self, positions:np.ndarray, r=None) -> list[list[int]]:
        '''
        Compute the neighbours of a bird or predator based on its position and radius around it.
        
        Args:
            positions: positions of every boids.
            r : radius of neighbourhood.
        '''

        if r is None:
            r = self.r
        kdtree = KDTree(positions)
        neighbs = kdtree.query_ball_point(positions, r=r, return_sorted=True)
        return neighbs

    def get_all_neighbours(self):
        """
        Compute the dictionaries of neighbours for each boid and predator based on self position, velocity and neighbours.

        """

        # Positions and velocity of boids around boids.
        positions_b = np.array([b.position for b in self.boid_list])
        velocities_b = np.array([b.velocity for b in self.boid_list])

        neighbs = self.find_neighbourhood(positions_b, r=self.r)
        self.neighb_positions = {i: positions_b[n] for i, n in enumerate(neighbs)}
        self.neighb_velocities = {i: velocities_b[n] for i, n in enumerate(neighbs)}

        neighbs = self.find_neighbourhood(positions_b, r=self.r_repulsion)
        self.neighb_positions_repulsion = {i: positions_b[n] for i, n in enumerate(neighbs)}

        # Check if there are predators.
        if len(self.predator_list) > 0:

            # Get positions of predators.
            positions_p = np.array([p.position for p in self.predator_list])    
        
            # Positions of boids around predators.
            tree_boids = KDTree(positions_b)
            neighbs_pred = tree_boids.query_ball_point(positions_p, r=self.r_pred)

            self.neighb_positions_pred = {i: positions_b[n] for i, n in enumerate(neighbs_pred)}   

            # Positions of predators around predators for repulsion.
            neighbs_p = self.find_neighbourhood(positions_p, r=self.r_repulsion*3) 
            self.neighb_positions_pred_pred = {i: positions_p[n] for i, n in enumerate(neighbs_p)} 
            
            # Positions of predators around boids for repulsion.
            tree_pred = KDTree(positions_p)
            neighbs_pred_rep = tree_pred.query_ball_point(positions_b, r=self.r_repulsion*1.5)

            self.neighb_positions_repulsion_pred = {i: positions_p[n] for i, n in enumerate(neighbs_pred_rep)}

        

    def one_step_move_boid(self):
        """
        Move the boids based on their velocity using move_flyer.
        Compute the velocity of the boids based on their neighbours and previous velocity by calculating their coherence, separation and alignment between each other and separation from predators .
        Limit the maximum speed of the boids.

        """
        for b in self.boid_list:
            b.move_flyer(dt=self.dt)

        self.get_all_neighbours()
        new_velocity = []
        for b_index, b in enumerate(self.boid_list):
            C = b.coherence(self.neighb_positions[b_index], self.boid_list[b_index].position, self.c_c)
            S = b.separation(self.neighb_positions_repulsion[b_index], self.boid_list[b_index].position, self.c_s)
            # Check if there are predators to avoid, else Sp is zero.
            if len(self.predator_list) > 0:
                Sp = b.separation(self.neighb_positions_repulsion_pred[b_index],self.boid_list[b_index].position,self.c_s_pred)
            else:
                Sp = np.zeros(2)
            A = b.alignment(self.neighb_velocities[b_index], self.boid_list[b_index].velocity, self.c_a)
            new_velocity.append(b.velocity + self.dt * (C + S + A + Sp))
        for b, new_v in zip(self.boid_list, new_velocity):
            if np.linalg.norm(new_v) > 5:
                b.velocity = (new_v / np.linalg.norm(new_v)) * 5
            else:
                b.velocity = new_v

    def one_step_move_predator(self):
        """
        Move the predators based on their velocity using move_flyer.
        Compute the velocity of the predators based on their neighbours and previous velocity by calculating their coherence toward boids and separation between each other.
        If the predators have eaten, their speed is greatly reduced.
        Limit the maximum acceleration and maximum speed of the predators.

        """
        for p in self.predator_list:
            p.move_flyer(dt=self.dt)

        self.get_all_neighbours()
        new_velocity = []
        for b_index, p in enumerate(self.predator_list):
            # Compute coherence only if there are boids in sight. Added to avoid NaN errors and predator staying stuck out of the screen with NaN velocity.
            if len(self.neighb_positions_pred[b_index]) > 0:
                C = p.coherence(self.neighb_positions_pred[b_index], p.position, self.c_c*2)
            else:
                C = np.zeros(2)
            # Compute separation from other predators so that they don't stack and stay less in the same place.
            if len(self.neighb_positions_pred_pred[b_index]) > 0:
                S = p.separation(self.neighb_positions_pred_pred[b_index], p.position, self.c_s)
            else:
                S = np.zeros(2)
            new_velocity.append(p.velocity + self.dt * (C + S))
        
        for p, new_v in zip(self.predator_list, new_velocity):

            # Limit the speed of the predator depending on whether it has eaten or not.
            if p.eaten==True:
                max_speed = 1
            else:
                max_speed = 8

            # Limit the acceleration of the predator, looks more "realistic".
            if np.linalg.norm(new_v - p.velocity) > 1:
                new_v = p.velocity + (new_v - p.velocity) / np.linalg.norm(new_v - p.velocity) * 2

            # Limit the speed of the predator.
            if np.linalg.norm(new_v) > max_speed:
                p.velocity = (new_v / np.linalg.norm(new_v)) * max_speed
            else:
                p.velocity = new_v


    def __init__(self, nb_boids:int=100, nb_predators:int=2, c_c:float=.001, c_s:float=.01, c_s_pred:float=5, c_a:float=.01, r:int=100, r_repulsion:int=20, r_pred:int=200, score:int=0, dt:float=1.5, seed:int=np.random.randint(0, 10000)) -> None:

        # Set the seed used for the simulation.
        np.random.seed(seed)
        
        # Create boid and predator lists.
        self.boid_list = [
            Bird(500 + np.random.rand(2) * 100 - 50, 2*np.random.rand(2)-1)
            for _ in range(nb_boids)
        ]

        self.predator_list = [
            Predator(np.random.rand(2) * np.array([1200, 700]), 2*np.random.rand(2)-1) for _ in range(nb_predators)
        ]

        # Flocking parameters.
        self.c_c = c_c
        self.c_s = c_s
        self.c_s_pred = c_s_pred
        self.c_a = c_a
        self.r = r
        self.r_repulsion = r_repulsion
        self.r_pred = r_pred
        self.score = score
        self.eat_image = []
        self.dt = dt
        print("In Flock")