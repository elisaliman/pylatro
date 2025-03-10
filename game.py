import pygame
import sys
from card import Card, CardGroup
from enums import Suit, Rank
import random

def generate_deck(shuffle: bool=False) -> list[Card]:
    """
    Creates a standard deck of cards

    Args:
        shuffle (bool, optional): True to shuffle deck. Defaults to False
    """

    deck = []
    x = 0
    y = 600
    for suit in Suit:
        x += 200
        for rank in Rank:
            y -= 30
            card = Card(suit, rank, (x, y))
            deck.append(card)
        y = 600
    if shuffle:
        random.shuffle(deck)
    return deck

class Game():

    cards: CardGroup
    held_card: Card | None

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False
        self.cards = CardGroup()
        deck = generate_deck()
        self.cards.add(deck)
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
