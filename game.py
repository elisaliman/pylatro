import pygame
import sys
import time
from card import Card

class Game():

    cards: pygame.sprite.Group

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False
        self.cards = pygame.sprite.Group()
        card1 = Card("grey80", 50, 50)
        self.cards.add(card1)

    def event_loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            self.draw()

    def draw(self):
        self.screen.fill("darkgreen")
        self.cards.draw(self.screen)
        pygame.display.flip()

    def quit(self) -> None:
        """
        Quit the application
        """
        pygame.quit()
        sys.exit(0)
