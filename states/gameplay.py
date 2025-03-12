import pygame
from card import Card
from card_holder import CardHolder
import time
from gameplay_logic import CardData, GameplayLogic
from states.statebase import StateBase
from states.pause import Pause
from assets.balatro_cards_data import CARD_HEI

DRAG_THRESHOLD = 0.25

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
    hand: CardHolder
    held_card: Card | None
    mouse_down_time: float | None

    def __init__(self, game):
        super().__init__(game)
        self.game_logic = GameplayLogic()
        screen_w, screen_h = self.game.screen.get_size()
        x = (screen_w - 568) // 2 #568 is the size of the hand display
        y = screen_h - 2 * CARD_HEI # places hand two card heights above bottom of screen
        self.hand = CardHolder(568, (x, y), 8, "center")
        self.held_card = None
        self.deal_to_hand()
        self.mouse_down_time = None

    def deal_to_hand(self) -> None:
        """
        Deals cards from deck into hand
        """
        self.game_logic.deal_to_hand()
        _, screen_h = self.game.screen.get_size()
        for card_data in self.game_logic.hand:
            card = Card(card_data.get_suit, card_data.get_rank, (1000, screen_h - CARD_HEI * 3 // 2)) # places center of deck 1.5 card_h above bottom of screen
            self.hand.add_card(card)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """

        if event.type == pygame.QUIT:
            self.game.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # reversed to scan cards from top layer to bottom
            for card in self.hand.cards.sprites()[::-1]:
                if card.rect.collidepoint(event.pos):
                    self.mouse_down_time = time.time()
                    self.held_card = card
                    self.hand.cards.move_to_top(card)
                    break

        if event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_down_time is not None:
                elapsed_time = time.time() - self.mouse_down_time
                if elapsed_time < DRAG_THRESHOLD:
                    print("Mouse Click!")
                self.mouse_down_time = None  # Reset
            if self.held_card and self.held_card.follow_mouse:
                self.held_card.toggle_mouse_follow()
            self.held_card = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Pause(self.game).enter_state()
            if event.key == pygame.K_UP:
                self.exit_state()

    def update(self, dt: float) -> None:
        dragged = False
        if self.mouse_down_time is not None and self.held_card:
            if not self.held_card.rect.collidepoint(pygame.mouse.get_pos()):
                dragged = True
            elapsed = time.time() - self.mouse_down_time
            if elapsed >= DRAG_THRESHOLD:
                dragged = True
            if dragged:
                self.mouse_down_time = None  # Reset
                self.held_card.toggle_mouse_follow()

        for card in self.hand.cards.sprites():
            card.update(dt) # pos should be propper position in hand table


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("darkgreen")
        self.hand.draw(screen)
        self.hand.cards.draw(screen)
        if self.held_card:
            self.held_card.draw(screen, True)
        pygame.display.flip()