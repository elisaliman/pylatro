from typing import override

import pygame

from states.gui_elements.card import CARD_HEI, CARD_WID, Card, CardGroup


class CardHolder(pygame.sprite.Sprite):
    w: int
    h: int
    image: pygame.surface.Surface
    rect: pygame.Rect
    cards: CardGroup
    num_slots: int
    pos: tuple[int, int]
    text_pos: tuple[int, int]
    font: pygame.font.Font

    def __init__(
        self, w: int, center_pos: tuple[int, int], num_slots: int, text_side: str
    ):
        self.w = w
        self.h = CARD_HEI + 10
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(
            self.image,
            (0, 0, 0, 50),
            (0, 0, self.w, self.h),
            border_radius=10,
        )
        self.rect = self.image.get_rect()
        self.rect.center = center_pos
        self.cards = CardGroup()
        self.num_slots = num_slots
        self.set_text(text_side)

    def set_text(self, text_side: str) -> None:
        """
        Sets text placement for text
        """
        positions = ["left", "center", "right"]
        if text_side.lower() not in positions:
            text_side = "left"
        text_x, y = self.rect.center
        text_y = y + CARD_HEI // 2 + 10
        if text_side == "left":
            text_x = self.rect.left
        elif text_side == "right":
            text_x = self.rect.right
        self.text_pos = (text_x, text_y)
        self.font = pygame.font.Font("assets/balatro.ttf", 15)
        text = f"{len(self.cards.sprites())}/{self.num_slots}"
        self.text_image = self.font.render(text, True, "white")
        if text_side == "center":  # middles text if text is in center
            offset_x = self.text_image.get_size()[0] // 2
            self.text_pos = self.text_pos[0] - offset_x, self.text_pos[1]
        if text_side == "right":
            offset_x = self.text_image.get_size()[0]
            self.text_pos = self.text_pos[0] - offset_x, self.text_pos[1]

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.rect.topleft)
        screen.blit(self.text_image, self.text_pos)

    def add_card(self, card: Card) -> None:
        """
        Adds card to card holder
        """
        assert isinstance(card, Card)
        if card not in self.cards.sprites():
            card_idx = len(self.cards.sprites())
            x = self.rect.x + (card_idx * CARD_WID) + CARD_WID // 2
            y = self.rect.y + (CARD_HEI // 2)
            card.set_target_pos((x, y))
            self.cards.add(card)

    def add_slot(self) -> None:
        """
        Adds one more card slot to card holder
        """
        self.num_slots += 1

    def update(self, dt: float, ctx: int | None = None) -> None:
        """
        Updates card count text
        """
        count = 0
        for card in self.cards.sprites():
            if self.rect.collidepoint(card.target_pos):
                count += 1
        text = f"{count}/{self.num_slots}"
        self.text_image = self.font.render(text, True, "white")


class DeckHolder(CardHolder):
    """
    Special subclass to override how the text is displayed for the deck
    """

    def __init__(
        self, w: int, center_pos: tuple[int, int], num_slots: int, text_side: str
    ):
        super().__init__(w, center_pos, num_slots, text_side)

    def update(self, dt: float, deck_remaining: int | None = None):
        text = f"{deck_remaining}/{self.num_slots}"
        self.text_image = self.font.render(text, True, "white")
