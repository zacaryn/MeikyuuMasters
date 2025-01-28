import pygame
from pytmx.util_pygame import load_pygame

class Overworld:
    def __init__(self, screen, map_file):
        self.screen = screen
        self.tmx_data = load_pygame(map_file)  # Load the Tiled map
        self.tile_size = self.tmx_data.tilewidth
        self.player_x, self.player_y = 2, 2  # Starting position in grid

        self.map_width = self.tmx_data.width
        self.map_height = self.tmx_data.height

        self.camera = Camera(screen.get_width(), screen.get_height(),
                             self.map_width, self.map_height, self.tile_size)

    def draw_map(self):
        """Draw all tile layers, including the collision layer."""
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):  # Ensure it's a tile layer
                for x, y, image in layer.tiles():  # Directly get image from tiles()
                    if image:  # Only draw if the tile has an image
                        screen_x, screen_y = self.camera.apply(x * self.tile_size, y * self.tile_size)
                        if 0 <= screen_x < self.camera.width and 0 <= screen_y < self.camera.height:
                            self.screen.blit(image, (screen_x, screen_y))


    def draw_player(self):
        """Draw the player centered in the viewport."""
        player_screen_x, player_screen_y = self.camera.apply(
            self.player_x * self.tile_size + self.tile_size // 2,
            self.player_y * self.tile_size + self.tile_size // 2
        )
        pygame.draw.circle(self.screen, (255, 0, 0), (player_screen_x, player_screen_y), self.tile_size // 3)

    def move_player(self, dx, dy):
        """Move the player, checking collisions."""
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if self.is_walkable(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y
            self.camera.update(self.player_x, self.player_y, self.tile_size)

    def is_walkable(self, tile_x, tile_y):
        """Check if the tile at (tile_x, tile_y) is walkable."""
        for layer in self.tmx_data.visible_layers:
            if layer.name == "collision" and hasattr(layer, "tiles"):  # Only check the collision layer
                for x, y, image in layer.tiles():
                    if x == tile_x and y == tile_y and image:  # Non-None image means collision
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

    def update(self, player_x, player_y, tile_size):
        """Center the camera on the player while staying within map bounds."""
        self.x = max(0, min(player_x * tile_size - self.width // 2, self.map_width - self.width))
        self.y = max(0, min(player_y * tile_size - self.height // 2, self.map_height - self.height))

    def apply(self, x, y):
        """Convert world coordinates to screen coordinates."""
        return x - self.x, y - self.y




