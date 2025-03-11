import pygame
from card import Card, CardGroup
from enums import Suit, Rank
from gameplay_logic import CardData, GameplayLogic
from states.statebase import StateBase
from states.pause import Pause

# use for testing cards
# def generate_deck(deck_data: list[CardData]) -> list[Card]:
#     deck = []
#     x = 100
#     y = 100
#     for card_data in deck_data:
#         suit = card_data.get_suit
#         rank = card_data.get_rank
#         card = Card(suit, rank, (x, y))
#         deck.append(card)
#         y += 30
#         if y % 490 == 0:
#             x += 200
#             y = 100
#     return deck

def generate_deck(deck_data: list[CardData]) -> list[Card]:
    deck = []
    for card_data in deck_data:
        suit = card_data.get_suit
        rank = card_data.get_rank
        card = Card(suit, rank, (400, 400))
        deck.append(card)
    return deck


class Gameplay(StateBase):
    game_logic: GameplayLogic
    deck: list[Card]
    hand: CardGroup
    held_card: Card | None

    def __init__(self, game):
        super().__init__(game)
        self.game_logic = GameplayLogic()
        self.hand = CardGroup()
        self.held_card = None
        self.startup()

    def startup(self) -> None:
        """Intended to be run once at state start"""
        self.game_logic.deal_to_hand()
        self.deal_to_hand()

    def deal_to_hand(self) -> None:
        """
        Deals cards from deck into hand
        """
        for card_data in self.game_logic.hand:
            card = Card(card_data.get_suit, card_data.get_rank, (400, 400)) # pos should be where deck is in game
            card.toggle_show()
            self.hand.add(card)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """
        if event.type == pygame.QUIT:
            self.game.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # reversed to scan cards from top layer to bottom
            for card in self.hand.sprites()[::-1]:
                if card.is_clicked(event.pos):
                    self.held_card = card
                    self.hand.move_to_top(card)
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            self.held_card = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Pause(self.game).enter_state()
            if event.key == pygame.K_UP:
                self.exit_state()

    def update(self, dt: float) -> None:
        if self.held_card:
            self.held_card.update(dt, pygame.mouse.get_pos())
        for card in self.hand.sprites():
            if card is not self.held_card:
                card.update(dt, (100, 100)) # pos should be propper position in hand table


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("darkgreen")
        self.hand.draw(screen)
        if self.held_card:
            self.held_card.draw(screen, True)
        pygame.display.flip()