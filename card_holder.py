import pygame
from card import Card, CardGroup, CARD_WID, CARD_HEI
from gameplay_logic import GameplayLogic


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


    def __init__(self, w: int, pos: tuple[int, int], num_slots: int, text_side: str):
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
        self.rect.topleft = pos
        self.cards = CardGroup()
        self.num_slots = num_slots
        self.pos = pos
        self.set_text(text_side)

    def set_text(self, text_side: str) -> None:
        """
        Sets text placement for text
        """
        positions = ["left", "center", "right"]
        if text_side.lower() not in positions:
            text_side = "left"
        x, y = self.pos
        text_y = y + CARD_HEI + 10
        idx = positions.index(text_side)
        text_x = x + (idx * self.image.get_size()[0] // 2)
        self.text_pos = (text_x, text_y)
        self.font = pygame.font.Font("assets/balatro.ttf", 15)
        text = f"{len(self.cards.sprites())}/{self.num_slots}"
        self.text_image = self.font.render(text, True, "white")
        if text_side == "center":
            offset_x = self.text_image.get_size()[0] // 2
            self.text_pos = self.text_pos[0] - offset_x, self.text_pos[1]


    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.image, self.pos)
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

    def update(self, dt: float) -> None:
        """
        Updates card count text
        """
        count = 0
        for card in self.cards.sprites():
            if self.rect.collidepoint(card.target_pos):
                count += 1
        text = f"{count}/{self.num_slots}"
        self.text_image = self.font.render(text, True, "white")