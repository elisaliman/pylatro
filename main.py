import pygame
import sys
from game import Game

pygame.init()
pygame.font.init()
pygame.display.set_caption("Balatro")
screen = pygame.display.set_mode((1280, 720))

if __name__ == "__main__":
    game = Game(screen)
    game.event_loop()