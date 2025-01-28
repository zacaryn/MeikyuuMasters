import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 700
TILE_SIZE = 80

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Overworld Mockup")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Define the maze grid (1 = wall, 0 = open space)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Player properties
player_x, player_y = 1, 1  # Start position in grid
player_radius = TILE_SIZE // 3

# Movement speed
speed = 1

def draw_maze():
    """Draw the maze grid."""
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            color = GRAY if maze[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_player():
    """Draw the player."""
    pygame.draw.circle(
        screen, RED, 
        (player_x * TILE_SIZE + TILE_SIZE // 2, player_y * TILE_SIZE + TILE_SIZE // 2), 
        player_radius
    )

def handle_collision(new_x, new_y):
    """Check for wall collisions."""
    if maze[new_y][new_x] == 1:
        return False
    return True

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement keys
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y
    if keys[pygame.K_w]:  # Move up
        new_y -= speed
    if keys[pygame.K_s]:  # Move down
        new_y += speed
    if keys[pygame.K_a]:  # Move left
        new_x -= speed
    if keys[pygame.K_d]:  # Move right
        new_x += speed

    # Check collisions
    if handle_collision(new_x, new_y):
        player_x, player_y = new_x, new_y

    # Draw maze and player
    draw_maze()
    draw_player()

    # Update the display
    pygame.display.flip()
    clock.tick(30)  # Cap frame rate to 30 FPS

# Quit Pygame
pygame.quit()
sys.exit()
