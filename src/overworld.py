import pygame
from pytmx.util_pygame import load_pygame

class Overworld:
    def __init__(self, screen, map_file):
        self.screen = screen
        self.tmx_data = load_pygame(map_file)  # Load the Tiled map
        self.tile_size = self.tmx_data.tilewidth
        self.player_x = 2 * self.tile_size  # Starting at tile (2, 2) in pixels
        self.player_y = 2 * self.tile_size
        self.speed = 300 # Player speed in pixels per second

        self.map_width = self.tmx_data.width
        self.map_height = self.tmx_data.height

        self.camera = Camera(screen.get_width(), screen.get_height(),
                             self.map_width, self.map_height, self.tile_size)
        
        # Player sprite setup
        self.walk_spritesheet = pygame.image.load("assets/sprites/player.png").convert_alpha()
        self.idle_spritesheet = pygame.image.load("assets/sprites/idle.png").convert_alpha()
        self.frame_width, self.frame_height = 32, 32  # Frame size
        self.sprite_row = {
            "down": 0,     # Row 0: Facing down
            "up": 1,       # Row 1: Facing up
            "left": 3,     # Row 3: Facing left
            "right": 2     # Row 2: Facing right
        }
        self.current_frame = 0  # Frame index for animation
        self.animation_speed = 0.1  # Speed of animation (lower is faster)
        self.time_since_last_frame = 0  # Time tracker for animation
        self.player_direction = "down"  # Initial facing direction
        self.is_moving = False  # Tracks if the player is moving

    def draw_map(self):
        """Draw all tile layers, including the collision layer."""
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):  # Ensure it's a tile layer
                for x, y, image in layer.tiles():  # Directly get image from tiles()
                    if image:  # Only draw if the tile has an image
                        screen_x, screen_y = self.camera.apply(x * self.tile_size, y * self.tile_size)
                        if 0 <= screen_x < self.camera.width and 0 <= screen_y < self.camera.height:
                            self.screen.blit(image, (screen_x, screen_y))


    def draw_player(self, dt):
        """Draw the player with the correct sprite frame, centered in the viewport."""
        # Update animation frame
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.animation_speed:
            self.time_since_last_frame = 0
            self.current_frame = (self.current_frame + 1) % 2  # Cycle through frames

        # Determine the correct spritesheet (walking or idle)
        spritesheet = self.walk_spritesheet if self.is_moving else self.idle_spritesheet

        # Get the correct sprite frame
        row = self.sprite_row[self.player_direction]
        frame_x = self.current_frame * self.frame_width
        frame_y = row * self.frame_height
        frame = spritesheet.subsurface(
            pygame.Rect(frame_x, frame_y, self.frame_width, self.frame_height)
        )

        # Calculate screen position using the camera
        player_screen_x, player_screen_y = self.camera.apply(self.player_x, self.player_y)

        # Draw the player sprite on the screen
        self.screen.blit(frame, (player_screen_x - self.frame_width // 2, player_screen_y - self.frame_height // 2))



    def move_player(self, dx, dy, dt):
        """Move the player smoothly using pixel-based movement, update the camera, and handle sprite direction."""
        # Calculate potential new position in pixels
        new_x = self.player_x + dx * self.speed * dt
        new_y = self.player_y + dy * self.speed * dt

        # Check if the new position is walkable
        if self.is_walkable(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y
            self.is_moving = True

            # Update player direction based on movement
            if dx > 0:
                self.player_direction = "right"
            elif dx < 0:
                self.player_direction = "left"
            elif dy > 0:
                self.player_direction = "down"
            elif dy < 0:
                self.player_direction = "up"

            # Update the camera to follow the player
            self.camera.update(self.player_x, self.player_y)
        else:
            print("Position is not walkable.")
            self.is_moving = False  # Player is idle



    def is_walkable(self, pixel_x, pixel_y):
        """Check if the tile at the given pixel position is walkable."""
        # Convert pixel position to tile position
        tile_x = int(pixel_x // self.tile_size)
        tile_y = int(pixel_y // self.tile_size)

        # Ensure tile coordinates are within the map bounds
        if tile_x < 0 or tile_x >= self.map_width or tile_y < 0 or tile_y >= self.map_height:
            print(f"Out of bounds: tile ({tile_x}, {tile_y})")
            return False

        # Check the collision layer for blocking tiles
        for layer in self.tmx_data.visible_layers:
            if layer.name == "collision" and hasattr(layer, "tiles"):  # Only check tile layers with "tiles"
                for x, y, image in layer.tiles():
                    if x == tile_x and y == tile_y and image:  # Non-None image means collision
                        print(f"Collision detected at tile ({tile_x}, {tile_y})")
                        return False

        return True



class Camera:
    def __init__(self, width, height, map_width, map_height, tile_size):
        self.width = width  # Viewport width (window size)
        self.height = height  # Viewport height (window size)
        self.map_width = map_width * tile_size  # Full map width in pixels
        self.map_height = map_height * tile_size  # Full map height in pixels
        self.x = 0  # Top-left corner of the viewport
        self.y = 0  # Top-left corner of the viewport

    def update(self, player_x, player_y):
        """Center the camera on the player while staying within map bounds."""
        self.x = max(0, min(player_x - self.width // 2, self.map_width - self.width))
        self.y = max(0, min(player_y - self.height // 2, self.map_height - self.height))

    def apply(self, x, y):
        """Convert world coordinates (in pixels) to screen coordinates."""
        return x - self.x, y - self.y





