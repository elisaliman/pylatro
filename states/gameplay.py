import pygame
import sys
from card import Card, CardGroup
from enums import Suit, Rank
import random
from states.statebase import StateBase
from states.pause import Pause

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

class Gameplay(StateBase):
    deck: list[Card]
    cards: CardGroup
    held_card: Card | None

    def __init__(self, game):
        super().__init__(game)
        self.cards = CardGroup()
        self.deck = generate_deck()
        self.cards.add(self.deck)
        self.held_card = None

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """
        if event.type == pygame.QUIT:
            self.game.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # reversed to scan cards from top layer to bottom
            for card in self.cards.sprites()[::-1]:
                if card.is_clicked(event.pos):
                    self.held_card = card
                    self.cards.move_to_top(card)
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            self.held_card = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Pause(self.game).enter_state()
            if event.key == pygame.K_UP:
                self.exit_state()
        if self.held_card:
            self.held_card.update()

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("darkgreen")
        self.cards.draw(screen)
        if self.held_card:
            self.held_card.draw(screen, True)