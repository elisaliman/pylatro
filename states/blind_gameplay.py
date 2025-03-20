import time
import copy

import pygame

from typing import cast
from assets.balatro_cards_data import CARD_HEI, CARD_WID
from state_logic.carddata import CardData
from state_logic.blind_logic import BlindLogic
from states.gui_elements.button import Button
from states.gui_elements.card import Card, Joker, GUICardBase
from states.gui_elements.card_holder import CardHolder, DeckHolder
from states.pause import Pause
from states.statebase import StateBase
from states.gui_elements.side_panel import SidePanel
from states.gui_elements.score_animation import ScoreAnimation
from enums import HandType
from utils import get_play_anim_start_x

DRAG_THRESHOLD = 0.25
BUTTON_COOLDOWN: float = 0.5


class Gameplay(StateBase):
    game_logic: BlindLogic
    buttons: pygame.sprite.OrderedUpdates
    jokers: CardHolder[Joker]
    hand: CardHolder[Card]
    hand_ordered: list[Card]
    deck: DeckHolder
    sort_by_rank: bool
    held_card: GUICardBase | None
    mouse_down_timer: float | None
    scoring_animation: ScoreAnimation | None
    side_panel: SidePanel
    last_button_click_time: float  # Safety measure to prevent duplicate clicks

    def __init__(self, game, side_panel: SidePanel, jokers: CardHolder):
        super().__init__(game)
        # Initializes game logic and adds current game logic to side panel
        manager = self.ctx["manager"]
        self.game_logic = BlindLogic(manager)
        self.side_panel = side_panel
        self.side_panel.set_blind_logic(self.game_logic)
        screen_w, screen_h = self.game.screen.get_size()
        x = screen_w // 2
        y = screen_h - 2 * CARD_HEI
        self.hand = CardHolder[Card](CARD_WID * 8, (x, y), 8, "center")
        self.hand_ordered = []
        self.jokers = jokers
        x += int(CARD_WID * 4.5) + CARD_WID * 2
        self.deck = DeckHolder(CARD_WID, (x, y + 30), len(self.game_logic.deck), "left")
        temp = copy.deepcopy(self.game_logic.deck[-1])
        fake_card = Card(
            temp.get_suit, temp.get_rank, 0, self.deck.rect.center, shown=False
        )
        self.deck.add_card(fake_card)
        self.held_card = None
        self.sort_by_rank = True
        self.mouse_down_timer = None
        self.scoring_animation = None
        self._create_buttons()
        self.deal_to_hand()

    def _create_buttons(self) -> None:
        self.last_button_click_time = time.time()
        self.buttons = pygame.sprite.OrderedUpdates()
        hand = self.hand.rect
        play_rect = pygame.Rect((hand.x, hand.y + CARD_HEI + 10), (CARD_HEI, CARD_WID))
        play = Button(
            play_rect,
            "Play Hand",
            self.play_hand,
            self.font15,
            pygame.Color("cornflowerblue"),
            pygame.Color("white"),
        )
        discard_rect = pygame.Rect(
            (hand.bottomright[0] - CARD_HEI, hand.y + CARD_HEI + 10),
            (CARD_HEI, CARD_WID),
        )
        discard = Button(
            discard_rect,
            "Discard",
            self.discard,
            self.font15,
            pygame.Color("crimson"),
            pygame.Color("white"),
        )
        rank_rect = play_rect.scale_by(0.5, 0.5)  # I base rank rect off of play rect
        rank_rect.center = (self.hand.rect.centerx - rank_rect.w, rank_rect.centery)
        rank = Button(
            rank_rect,
            "Rank",
            self.sort_rank,
            self.font15,
            pygame.Color("orange"),
            pygame.Color("white"),
        )
        suit_rect = discard_rect.scale_by(
            0.5, 0.5
        )  # I base suit rect off of discard rect
        suit_rect.center = (self.hand.rect.centerx + suit_rect.w, suit_rect.centery)
        suit = Button(
            suit_rect,
            "Suit",
            self.sort_suit,
            self.font15,
            pygame.Color("orange"),
            pygame.Color("white"),
        )
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
        Also stores the ordered cards
        """
        # Ensure game_logic is consistent with the sort mode
        self.game_logic.sort_cards(self.sort_by_rank)
        if self.sort_by_rank:
            cards = sorted(
                self.hand.cards.sprites(),
                key=lambda card: (-card.rank.value, card.suit.value),
            )
        else:
            cards = sorted(
                self.hand.cards.sprites(),
                key=lambda card: (card.suit.value, -card.rank.value),
            )
        self._sort_adjust_pos(cards)
        self.hand_ordered = cards

    def sort_by_custom(self, pos_x: int) -> None:
        """
        Does a custom sorting where a held card is placed wherever it is dropped
        in the hand

        Args:
            pos_x (int): x coord of the mouse when card is dropped
        """
        assert self.held_card
        hand: list[GUICardBase]
        if isinstance(self.held_card, Card):
            hand = cast(list[GUICardBase], self.hand_ordered)
        elif isinstance(self.held_card, Joker):
            hand = cast(list[GUICardBase], self.jokers.cards.sprites())
        else:
            raise ValueError("No Card Holders to sort")
        og_idx = hand.index(self.held_card)
        new_idx: int | None = None
        if pos_x < hand[0].rect.centerx and self.held_card is not hand[0]:
            new_idx = 0
        elif pos_x > hand[-1].rect.centerx and self.held_card is not hand[-1]:
            new_idx = len(hand) - 1
        else:
            for idx, card in enumerate(hand[1:]):
                if (
                    hand[idx] is not self.held_card
                    and card is not self.held_card
                    and hand[idx].rect.centerx < pos_x < card.rect.centerx
                ):
                    new_idx = idx + 1
                    if og_idx < new_idx:
                        new_idx -= 1
                    break
        if new_idx is None:
            return

        hand.insert(new_idx, hand.pop(og_idx))
        if isinstance(self.held_card, Card):
            self.game_logic.sort_cards_custom(og_idx, new_idx)
            self.hand_ordered = cast(list[Card], hand)
            self._sort_adjust_pos(cast(list[Card], hand))

    def _sort_adjust_pos(self, hand: list[Card]) -> None:
        """
        Helper method for sort and custom sort that adjusts the target
        postitions of the cards in hand

        Args:
            hand (list[Card]): list of cards for hand to be ordered in
        """
        self.hand.cards.empty()
        for idx, card in enumerate(hand):
            x = self.hand.rect.x + (idx * CARD_WID) + CARD_WID // 2
            y = self.hand.rect.y + (CARD_HEI // 2)
            if card.selected:
                y -= 35  # Offset in card class is 35. May cause issues if I change value in one place
            card.set_target_pos((x, y))
            self.hand.cards.add(card)

    def deal_to_hand(self) -> None:
        """
        Deals cards from deck into hand
        """
        if not self.game_logic.done:
            hand_num_empty = self.game_logic.hand_size - len(self.game_logic.hand)
            self.game_logic.deal_to_hand()
            if hand_num_empty != 0:
                for card_data in self.game_logic.hand[-hand_num_empty:]:
                    card = Card(
                        card_data.get_suit,
                        card_data.get_rank,
                        card_data.chips,
                        self.deck.rect.center,
                    )  # places center of deck 1.5 card_h above bottom of screen
                    self.hand.add_card(card)
                self.sort_cards()

    def play_hand(self) -> None:
        """
        Plays hand
        """
        current_time = time.time()
        if (
            self.game_logic.num_selected() > 0
            and not self.scoring_animation
            and not self.game_logic.done
            and current_time - self.last_button_click_time > BUTTON_COOLDOWN
        ):
            self.last_button_click_time = current_time
            played_card_datas, hand_type, score = self.game_logic.play_hand()
            self.side_panel.update_hand_type(hand_type)
            _, screen_h = self.game.screen.get_size()
            start_x = get_play_anim_start_x(self.game.screen, len(played_card_datas))
            played: list[Card] = []
            for card in self.hand_ordered:
                card_data = self.convert_to_card_data(card)
                if card_data in played_card_datas and card.selected:
                    card.set_target_pos((start_x, screen_h // 2))
                    start_x += card.rect.w + 30  # SPACING
                    played.append(card)
            self.scoring_animation = ScoreAnimation(
                self.side_panel, self.side_panel.score, score, played, self.jokers.cards.sprites()
            )

    def discard(self, just_played: bool = False) -> None:
        """
        Discards selected cards

        Args:
            just_played (bool, optional): if true, wont deduct a discard as
                it means the fucntion was called to rid the played cards, not
                cards from hand
        """
        if (
            (just_played or self.game_logic.num_discards > 0)
            and self.game_logic.num_selected() > 0
            and not self.scoring_animation
        ):
            self.game_logic.discard(just_played)
            for card in self.hand.cards.sprites():
                if card.selected:
                    card.shown = False
                    x, _ = self.game.screen.get_size()
                    card.set_target_pos((x - 10, card.rect.y + 10))
                    card.kill()
            if self.game_logic.deck:
                self.deal_to_hand()
            self.side_panel.update_hand_type(HandType.EMPTY)

    def select_card(self, card: Card) -> None:
        if card.selected or self.game_logic.num_selected() < 5:
            card_data = self.convert_to_card_data(card)
            card.toggle_select()
            self.game_logic.select_card(card_data)
            self.side_panel.update_hand_type(self.game_logic.get_hand_type())

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """
        if event.type == pygame.QUIT:
            self.game.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            self.side_panel.handle_event(event)
            for button in self.buttons.sprites():
                if isinstance(button, Button) and button.hovered:
                    button.callback()
                    return
            # Reversed to scan cards from top layer to bottom
            for card_holder in [self.hand, self.jokers]:
                assert isinstance(card_holder, CardHolder)
                for card in card_holder.cards.sprites()[::-1]:
                    if not self.scoring_animation and card.rect.collidepoint(event.pos):
                        self.mouse_down_timer = time.time()
                        self.held_card = card
                        return

        if event.type == pygame.MOUSEBUTTONUP:
            if self.mouse_down_timer is not None:
                elapsed_time = time.time() - self.mouse_down_timer
                if elapsed_time < DRAG_THRESHOLD and isinstance(self.held_card, Card):
                    self.select_card(self.held_card)
            if self.held_card and self.held_card.follow_mouse:
                dropped_x = event.pos[0]
                self.sort_by_custom(dropped_x)
                if isinstance(self.held_card, Card):
                    self.hand.cards.move_to_top(self.held_card)
                elif isinstance(self.held_card, Joker):
                    self.jokers.cards.move_to_top(self.held_card)
                self.held_card.toggle_mouse_follow()
            self.held_card = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.held_card:
                    self.held_card.toggle_mouse_follow()
                    self.held_card = None
                Pause(self.game)
            if event.key == pygame.K_UP:
                self.exit_state()

        if self.game_logic.done and not self.scoring_animation:
            self.end_blind()

    def end_blind(self) -> None:
        self.side_panel.remove_blind_logic()
        won = False
        if self.game_logic.score >= self.game_logic.blind:
            won = True
        # TEMPORARY: SENDS BACK TO BLIND SELECT
        if won:
            self.exit_state()
        else:
            self.exit_state()

    def convert_to_card_data(self, card: Card) -> CardData:
        """
        Gets CardData in hand that matches the GUI Card
        """
        ###TODO: Will need to change this bevuase you can have copies of the same card
        ### Will probably need to use indexing and sort the cards in game_logic
        suit, rank = card.suit, card.rank
        for card_data in self.game_logic.hand:
            if card_data.get_suit == suit and card_data.get_rank == rank:
                return card_data
        raise ValueError("Matching card not found in hand")

    def update(self, dt: float) -> None:
        # checks if card is dragged or clicked
        dragged = False
        if self.mouse_down_timer is not None and self.held_card:
            if not self.held_card.rect.collidepoint(pygame.mouse.get_pos()):
                dragged = True  # if user drags the card away even before the threshold
            elapsed = time.time() - self.mouse_down_timer
            if elapsed >= DRAG_THRESHOLD:
                dragged = True
            if dragged:
                self.mouse_down_timer = None  # Reset timer
                self.held_card.toggle_mouse_follow()

        for button in self.buttons.sprites():
            if isinstance(button, Button):
                button.update(dt)
        self.hand.update(dt)
        self.jokers.update(dt)
        self.deck.update(dt, self.game_logic.deck_remaining)
        if self.scoring_animation is not None:
            self.scoring_animation.update(dt)
            if self.scoring_animation.is_done():
                for joker in self.jokers.cards.sprites():
                    joker.jokerdata.scored = False
                self.scoring_animation = None
                self.side_panel.set_played_score()
                self.side_panel.update_hand_type(HandType.EMPTY)
                self.discard(just_played=True)

        self.side_panel.update(dt)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("darkgreen")
        self.hand.draw(screen)
        self.jokers.draw(screen)
        self.deck.draw(screen)
        if self.game_logic.deck:
            self.deck.cards.draw_cards(screen)
        self.buttons.draw(screen)
        if self.scoring_animation is not None:
            self.scoring_animation.draw(screen)
        self.side_panel.draw(screen)
        self.hand.cards.draw_cards(screen)
        self.jokers.cards.draw_cards(screen)
        if self.held_card:
            self.held_card.draw(screen)
