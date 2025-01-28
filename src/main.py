import pygame
from overworld import Overworld

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((720, 480))
pygame.display.set_caption("Meikyuu Masters")

# Create the Overworld
overworld = Overworld(screen, "assets/maps/overworld.tmx")

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement (WASD)
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_w]:  # Up
        dy = -1
    elif keys[pygame.K_s]:  # Down
        dy = 1
    elif keys[pygame.K_a]:  # Left
        dx = -1
    elif keys[pygame.K_d]:  # Right
        dx = 1    
    # Move the player
    overworld.move_player(dx, dy, dt)

    # If no keys are pressed, set is_moving to False
    if dx == 0 and dy == 0:
        overworld.is_moving = False

    # Draw everything
    screen.fill((0, 0, 0))
    overworld.draw_map()
    overworld.draw_player(dt)
    pygame.display.flip()

    clock.tick(30)  # Limit to 30 FPS

pygame.quit()
