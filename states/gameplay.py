import pygame
from card import Card
from card_holder import CardHolder
import time
from gameplay_logic import CardData, GameplayLogic
from states.statebase import StateBase
from states.pause import Pause
from assets.balatro_cards_data import CARD_HEI, CARD_WID
from button import Button
from operator import attrgetter

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
    buttons: pygame.sprite.Group
    hand: CardHolder
    sort_by_rank: bool
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
        self.sort_by_rank = True
        self.mouse_down_time = None
        self.create_buttons()
        self.deal_to_hand()

    def create_buttons(self) -> None:
        self.buttons = pygame.sprite.Group()
        hand = self.hand.rect
        play_rect = pygame.Rect((hand.x, hand.y + CARD_HEI + 10), (CARD_HEI, CARD_WID))
        play = Button(play_rect, "Play Hand", None, self.font15, pygame.Color("cornflowerblue"), pygame.Color("white"))
        discard_rect = pygame.Rect((hand.bottomright[0] - CARD_HEI, hand.y + CARD_HEI + 10), (CARD_HEI, CARD_WID))
        discard = Button(discard_rect, "Discard", self.discard, self.font15, pygame.Color("crimson"), pygame.Color("white"))
        rank_rect = play_rect.scale_by(0.5) # I base rank rect off of play rect
        rank_rect.center = (self.hand.rect.centerx - rank_rect.w, rank_rect.centery)
        rank = Button(rank_rect, "Rank", self.sort_rank, self.font15, pygame.Color("orange"), pygame.Color("white"))
        suit_rect = discard_rect.scale_by(0.5) # I base suit rect off of discard rect
        suit_rect.center = (self.hand.rect.centerx + suit_rect.w, suit_rect.centery)
        suit = Button(suit_rect, "Suit", self.sort_suit, self.font15, pygame.Color("orange"), pygame.Color("white"))
        self.buttons.add(play, discard, rank, suit)

    def sort_rank(self) -> None:
        """
        Function purely to be passed to sort by rank button
        """
        self.sort_by_rank = True
        self.sort_cards()

    def sort_suit(self) -> None:
        """
        Function purely to be passed to sort by suit button
        """
        self.sort_by_rank = False
        self.sort_cards()

    def sort_cards(self) -> None:
        """
        Sorts the cards in self.hand by rank or suit and updates their target positions.
        """
        # Ensure game_logic is consistent with the sort mode
        self.game_logic.sort_cards(self.sort_by_rank)

        key_attr = attrgetter("rank.value" if self.sort_by_rank else "suit.value")
        cards = self.hand.cards.sprites().copy()
        cards = sorted(cards, key=key_attr, reverse=True)
        self.hand.cards.empty()
        for idx, card in enumerate(cards):
            x = self.hand.rect.x + (idx * CARD_WID) + CARD_WID // 2
            y = self.hand.rect.y + (CARD_HEI // 2)
            if card.selected:
                y -= 35 #Offset in card class is 35. May cause issues if I change value in one place
            card.set_target_pos((x, y))
        self.hand.cards.add(cards)
    def deal_to_hand(self) -> None:
        """
        Deals cards from deck into hand
        """
        hand_num_empty = self.game_logic.hand_size - len(self.game_logic.hand)
        self.game_logic.deal_to_hand()
        if hand_num_empty != 0:
            _, screen_h = self.game.screen.get_size()
            for card_data in self.game_logic.hand[-hand_num_empty:]:
                card = Card(card_data.get_suit, card_data.get_rank, (1000, screen_h - CARD_HEI * 3 // 2)) # places center of deck 1.5 card_h above bottom of screen
                self.hand.add_card(card)
            self.sort_cards()

    def discard(self) -> None:
        if self.num_selected() > 0 and self.game_logic.num_discards > 0:
            self.game_logic.discard()
            for card in self.hand.cards.sprites():
                if card.selected:
                    card.shown = False
                    x, _ = self.game.screen.get_size()
                    card.set_target_pos((x - 10, card.rect.y + 10))
                    card.kill()
                    del card
            if self.game_logic.deck:
                self.deal_to_hand()

    def num_selected(self) -> int:
        """
        Returns number of selected cards
        """
        count = 0
        for cards in self.hand.cards.sprites():
            if cards.selected:
                count += 1
        return count

    def select_card(self, card: Card) -> None:
        if card.selected or self.num_selected() < 5:
            card_data = self.game_logic.convert_to_card_data(card)
            card.toggle_select()
            self.game_logic.select_card(card_data)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """

        if event.type == pygame.QUIT:
            self.game.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            for button in self.buttons.sprites():
                if isinstance(button, Button) and button.hovered:
                    button.callback()
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
                    self.select_card(self.held_card)
                self.mouse_down_time = None
            if self.held_card and self.held_card.follow_mouse:
                self.held_card.toggle_mouse_follow()
            self.held_card = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Pause(self.game).enter_state()
            if event.key == pygame.K_UP:
                self.exit_state()

    def update(self, dt: float) -> None:
        # checks if card is dragged or clicked
        dragged = False
        if self.mouse_down_time is not None and self.held_card:
            if not self.held_card.rect.collidepoint(pygame.mouse.get_pos()):
                dragged = True # if user drags the card away even before the threshold
            elapsed = time.time() - self.mouse_down_time
            if elapsed >= DRAG_THRESHOLD:
                dragged = True
            if dragged:
                self.mouse_down_time = None  # Reset timer
                self.held_card.toggle_mouse_follow()

        for button in self.buttons.sprites():
            if isinstance(button, Button):
                button.update(dt)
        for card in self.hand.cards.sprites():
            card.update(dt) # pos should be propper position in hand table
        self.hand.update(dt)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("darkgreen")
        self.hand.draw(screen)
        self.buttons.draw(screen)
        self.hand.cards.draw_cards(screen)
        self.draw_text(f"Score: {self.game_logic.score}", self.font24, (100, 100), pygame.Color("gold"))
        self.draw_text(f"Discards: {self.game_logic.num_discards}", self.font24, (100, 550), pygame.Color("crimson"))

        if self.held_card:
            self.held_card.draw(screen)
        pygame.display.flip()