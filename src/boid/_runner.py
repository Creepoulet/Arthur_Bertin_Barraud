from boid import Flock, Bird, Predator
import pygame
import numpy as np
import customtkinter

def setup_pygame(
    width: int = 600, height: int = 600, title: str = "Moving Triangles"
) -> pygame.Surface:
    # Initialising pygame
    pygame.init()

    # Set up display
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Moving Triangles")

    return screen


def display_triangles(
    screen: pygame.Surface,
    triangles: list[list[int, int, int]],
    color: list[int, int, int],
) -> None:
    for t in triangles:
        pygame.draw.polygon(screen, color, t)


def run_test():
    # bird = Bird()
    # predator = Predator()
    # flock = Flock()
    print("Hello World!")

    # Define colors
    black = (0, 0, 0)
    white = (255, 255, 255)

    width, height = 600, 600

    # Triangle properties
    scale = 10

    running = True
    current_pos = (width // 2, height // 2)
    speed = np.random.random(2) * 4 - 2

    screen = setup_pygame(width, height)
    while running:
        screen.fill(black)

        # Making sure that we stop the program when the user closes the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        new_pos = current_pos + speed
        direction = (speed) / np.linalg.norm(speed)

        ## A, B and C will be the points of the triangle
        C = new_pos + scale * direction
        A = (new_pos[0] + 3 * direction[1], new_pos[1] - 3 * direction[0])
        B = (new_pos[0] - 3 * direction[1], new_pos[1] + 3 * direction[0])
        display_triangles(screen, [[A, B, C]], white)

        # Updating the position
        current_pos = new_pos
        if new_pos[0] < 0 or new_pos[0] > width:
            speed[0] = -speed[0]
        if new_pos[1] < 0 or new_pos[1] > height:
            speed[1] = -speed[1]

        # Shuffling the speed
        angle = np.random.random() * np.pi / 6 - np.pi / 12
        speed = [
            np.cos(angle) * speed[0] - np.sin(angle) * speed[1],
            np.sin(angle) * speed[0] + np.cos(angle) * speed[1],
        ]
        # Update the display
        pygame.display.flip()

        # Frame rate
        pygame.time.Clock().tick(60)
    pygame.quit()


def run():
    '''
    Docstring for run
    '''

    # Custom Tkinter appearance
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    # Input dialogs for number of birds and predators
    dialog = customtkinter.CTkInputDialog(text="Enter number of birds :", title="Input")
    num_birds = int(dialog.get_input())
    if not isinstance(num_birds, int) or num_birds <= 0:
        raise ValueError("Number of birds must be a positive integer.")
    
    dialog2 = customtkinter.CTkInputDialog(text=f"Number of birds : {num_birds}\n Enter number of predators :", title="Input")
    num_predators = int(dialog2.get_input())
    if not isinstance(num_predators, int) or num_birds < 0:
        raise ValueError("Number of birds must be a positive integer or 0.")
    
    dialog3 = customtkinter.CTkInputDialog(text=f"Number of birds : {num_birds}\n Number of predators : {num_predators} \n Set a seed (Int/0/'Random')", title="Input")
    set_seed = dialog3.get_input()
    # check if set seed is an int or random
    if set_seed.lower() == "random":
        set_seed = np.random.randint(0, 10000)
    elif set_seed == "0":
        set_seed = 0
    else:
        try:
            set_seed = int(set_seed)
        except ValueError:
            raise ValueError("Seed must be a positive integer, 0 or 'Random'.")

    flock = Flock(num_birds, num_predators, seed = set_seed)
    flock.show_flock()
