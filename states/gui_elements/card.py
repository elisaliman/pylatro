import pygame
from enums import Suit, Rank
import assets.balatro_cards_data as assets
from assets.balatro_cards_data import CARD_WID, CARD_HEI

CARD_WID = 71
CARD_HEI = 95


class Card(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect
    suit: Suit
    rank: Rank
    front: pygame.surface.Surface
    back: pygame.surface.Surface
    shown: bool
    target_pos: tuple[int, int]
    follow_mouse: bool
    selected: bool

    def __init__(
        self, suit: Suit, rank: Rank, pos: tuple[int, int], shown: bool=True, *groups: pygame.sprite.Group
    ):
        super().__init__(*groups)
        self.suit = suit
        self.rank = rank
        self.image = pygame.Surface((CARD_WID, CARD_HEI), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        wid, hei = self.image.get_size()[0], self.image.get_size()[1]
        card_image = pygame.Rect(0, 0, wid, hei)
        pygame.draw.rect(
            self.image, pygame.Color("grey90"), card_image, border_radius=7
        )
        pygame.draw.rect(
            self.image, pygame.Color("grey70"), card_image, width=1, border_radius=7
        )
        self.front = assets.get_cardf_sprite(self.suit, self.rank)
        self.back = assets.get_cardb_sprite()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.target_pos = pos
        self.follow_mouse = False
        self.selected = False
        self.shown = not shown
        self.toggle_show()

    def toggle_show(self) -> None:
        """
        Toggles if card is shown (as in whether front vs back of card is displayed)
        """
        self.shown = not self.shown
        self.image.fill((0, 0, 0, 0))
        wid, hei = self.image.get_size()[0], self.image.get_size()[1]
        card_image = pygame.Rect(0, 0, wid, hei)
        pygame.draw.rect(
            self.image, pygame.Color("grey90"), card_image, border_radius=7
        )
        pygame.draw.rect(
            self.image, pygame.Color("grey70"), card_image, width=1, border_radius=7
        )
        if self.shown:
            self.image.blit(self.front, (0, 0))
        else:
            self.image.blit(self.back, (0, 0))

    def toggle_mouse_follow(self) -> None:
        self.follow_mouse = not self.follow_mouse

    def toggle_select(self) -> None:
        self.selected = not self.selected
        offset: int = 35
        if self.selected:
            self.set_target_pos((self.rect.centerx, self.rect.centery - offset))
        else:
            self.set_target_pos((self.rect.centerx, self.rect.centery + offset))

    def draw(self, screen: pygame.surface.Surface) -> None:
        """
        Draws the card, also draws its shadow if its held. (really intended to
        only ever be used when card is held)

        Args:
            screen (pygame.surface.Surface): screen to draw on
            is_held (bool, optional): True if card is currently held. Defaults
                to True
        """
        if self.follow_mouse:
            shadow = self.rect.copy()
            shadow.y += 10
            shadow.x += 10
            trans_surf = pygame.Surface((shadow.width, shadow.height), pygame.SRCALPHA)
            pygame.draw.rect(
                trans_surf,
                (0, 0, 0, 150),
                (0, 0, shadow.width, shadow.height),
                border_radius=10,
            )
            screen.blit(trans_surf, (shadow.x, shadow.y))
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt: float) -> None:
        if self.rect.center != self.target_pos or self.follow_mouse:
            self.rect.center = self.smooth_animation(dt)

    def smooth_animation(self, dt: float) -> tuple[int, int]:
        """
        Smooths movement of card from its location to target location

        Args:
            dt (float): delta time
        """
        # https://stackoverflow.com/questions/64087982/how-to-make-smooth-movement-in-pygame
        # used above thread to create the smooth animation
        Vector2 = pygame.math.Vector2
        target_x, target_y = self.target_pos
        if self.follow_mouse:
            target_x, target_y = pygame.mouse.get_pos()
        target_vector = Vector2(target_x, target_y)
        follower_vector = Vector2(self.rect.centerx, self.rect.centery)
        distance = follower_vector.distance_to(target_vector)
        if distance < 5:
            return (target_x, target_y)
        # Calculate the normalized direction vector from the current position to the target
        direction_vector = (target_vector - follower_vector).normalize()
        # Compute the step distance (using 10 as a speed multiplier; adjust as needed)
        step_distance = 10 * distance * dt
        # Ensure we don't move farther than the remaining distance
        step_distance = max(min(step_distance, distance), 5)
        new_follower_vector = follower_vector + direction_vector * step_distance
        return (int(new_follower_vector.x), int(new_follower_vector.y))

    def set_target_pos(self, pos: tuple[int, int]) -> None:
        """
        Sets a new rest position for the card

        Args:
            pos (tuple[int, int]): x, y position for card
        """
        self.target_pos = pos

    def __repr__(self):
        return f"Card: {self.rank.name.capitalize()} of {self.suit.name.capitalize()}s"

    def __eq__(self, value):
        if isinstance(value, Card):
            return self.rank == value.rank and self.suit == value.suit
        else:
            return False

    def __hash__(self):
        """
        Needed to add if i added an __eq__ method
        """
        return hash((self.suit, self.rank))


class CardGroup(pygame.sprite.Group):
    """
    pygame Group class that allows extra functionality
    """

    # Only reason for this overwrite is to enforce return type of Card for mypy
    def sprites(self) -> list[Card]:
        return super().sprites()

    def draw_cards(self, screen: pygame.surface.Surface) -> None:
        """draws cards onto screen"""
        for card in self.sprites():
            card.draw(screen)

    def move_to_top(self, card: Card) -> None:
        """Moves card to top (Drawn last)"""
        if card in self.sprites():
            self.remove(card)
            self.add(card)

    def move_to_bottom(self, card: Card) -> None:
        """Moves card to bottom (Drawn first)"""
        if card in self.sprites():
            self.remove(card)
            cards = self.sprites()
            cards = [card] + cards
            self.empty()
            self.add(cards)
