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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement (WASD)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Up
        overworld.move_player(0, -1)
    if keys[pygame.K_s]:  # Down
        overworld.move_player(0, 1)
    if keys[pygame.K_a]:  # Left
        overworld.move_player(-1, 0)
    if keys[pygame.K_d]:  # Right
        overworld.move_player(1, 0)

    # Draw everything
    screen.fill((0, 0, 0))
    overworld.draw_map()
    overworld.draw_player()
    pygame.display.flip()

    clock.tick(30)  # Limit to 30 FPS

pygame.quit()
