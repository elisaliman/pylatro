import pygame
from enums import Suit, Rank
try:
    sprite_sheet = pygame.image.load("assets/balatro_cards.png")
    back = pygame.image.load("assets/balatro_backs-export.png")
except pygame.error:
    print("Error loading sprite sheet!")
FRAME_WIDTH = 142
FRAME_HEIGHT = 190
def get_cardf_sprite(suit: Suit, num: Rank) -> pygame.surface.Surface:
    """
    Gets sprite image based on card value and suit
    """
    sheet = sprite_sheet
    row = suit.value
    col = num.value
    try:
        x = col * FRAME_WIDTH
        y = row * FRAME_HEIGHT
        sprite = sheet.subsurface((x, y), (FRAME_WIDTH, FRAME_HEIGHT))
        sprite = pygame.transform.scale(sprite, (71, 95))
        return sprite
    except pygame.error as perr:
        print(f"Error: Unable to extract sprite at row {row}, column {col}. {perr}")
        bad_surf = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT))
        bad_surf.fill("purple")
        return bad_surf
def get_cardb_sprite() -> pygame.surface.Surface:
    sheet = back
    try:
        sprite = sheet.subsurface((0, 0), (FRAME_WIDTH, FRAME_HEIGHT))
        sprite = pygame.transform.scale(sprite, (71, 95))
        return sprite
    except pygame.error as perr:
        print(f"Error: Unable to extract deck back. {perr}")
        bad_surf = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT))
        bad_surf.fill("purple")
        return bad_surf