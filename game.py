import pygame
import sys
from card import Card, CardGroup
from enums import Suit, Rank

class Game():

    cards: CardGroup
    held_card: Card | None

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False
        self.cards = CardGroup()
        card1 = Card(Suit.SPADE, Rank.TWO, 50, 50)
        card2 = Card(Suit.DIAMOND, Rank.KING, 10, 50)
        self.cards.add(card1, card2)
        self.held_card = None

    def event_loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for card in self.cards:
                        if card.is_clicked(event.pos):
                            self.held_card = card
                            self.cards.move_to_top(card)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.held_card = None
            if self.held_card:
                self.held_card.update()
            self.draw()

    def draw(self):
        self.screen.fill("darkgreen")
        self.cards.draw(self.screen)
        if self.held_card:
            self.held_card.draw(self.screen, True)
        pygame.display.flip()

    def quit(self) -> None:
        """
        Quit the application
        """
        pygame.quit()
        sys.exit(0)
