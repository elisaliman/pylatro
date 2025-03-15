import os
import pygame

# Force low-resolution mode (disable HiDPI scaling)
os.environ["SDL_VIDEO_ALLOW_SCREENSAVER"] = "1"  # Optional: Prevent fullscreen issues
os.environ["SDL_VIDEO_MAC_FULLSCREEN_DISABLE_HIDPI"] = "1"
os.environ["SDL_HINT_VIDEO_HIGHDPI_DISABLED"] = "1"
from game import Game

pygame.init()
pygame.font.init()
pygame.display.set_caption("Balatro")
SCREEN_WID, SCREEN_HEI = 1280, 720
screen = pygame.display.set_mode(
    (SCREEN_WID, SCREEN_HEI), pygame.SCALED | pygame.RESIZABLE
)

if __name__ == "__main__":
    game = Game(screen)
    game.run()
