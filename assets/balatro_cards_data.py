import pygame

from enums import Rank, Suit

CARD_WID, CARD_HEI = 71, 95
FRAME_WIDTH, FRAME_HEIGHT = 142, 190

try:
    sprite_sheet = pygame.image.load("assets/balatro_cards.png")
    decks = pygame.image.load("assets/balatro_decks.png")
    bad_surf = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT))
    bad_surf.fill("yellow")
except pygame.error:
    print("Error loading sprite sheet!")


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
        sprite = pygame.transform.scale(sprite, (CARD_WID, CARD_HEI))
        return sprite
    except pygame.error as perr:
        print(f"Error: Unable to extract sprite at row {row}, column {col}. {perr}")
        return bad_surf

def get_cardb_sprite() -> pygame.surface.Surface:
    sheet = decks
    try:
        sprite = sheet.subsurface((0, 0), (FRAME_WIDTH, FRAME_HEIGHT))
        return sprite
    except pygame.error as perr:
        print(f"Error: Unable to extract deck back. {perr}")
        return bad_surf

def get_joker_sprites() -> tuple[pygame.Surface, pygame.Surface]:
    """Gets the front and back sprites for a given joker"""
    #TEMP IMAGES
    sheet = decks
    try:
        front = sheet.subsurface((CARD_WID * 5, CARD_HEI * 3), (CARD_WID, CARD_HEI))
        back = sheet.subsurface((CARD_WID * 2, CARD_HEI * 1), (CARD_WID, CARD_HEI))
        return (front, back)
    except pygame.error as perr:
        print(f"Error: Unable to extract deck back. {perr}")
        return (bad_surf, bad_surf)

