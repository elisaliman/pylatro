import pygame
from enums import Suit, Rank
from assets.balatro_cards_data import get_sprite


class Card(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect
    suit: Suit
    rank: Rank

    def __init__(self, suit: Suit, rank: Rank, pos: tuple[int, int]):
        super().__init__()
        self.suit = suit
        self.rank = rank
        self.image = pygame.Surface((71, 95), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        wid, hei = self.image.get_size()[0], self.image.get_size()[1]
        card_image = pygame.Rect(0, 0, wid, hei)
        pygame.draw.rect(self.image, pygame.Color("grey90"), card_image, border_radius=7)
        pygame.draw.rect(self.image, pygame.Color("grey70"), card_image, width=1, border_radius=7)
        self.image.blit(get_sprite(self.suit, self.rank), (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, screen: pygame.surface.Surface, is_held: bool=True) -> None:
        """
        Draws the card, also draws its shadow if its held. (really intended to
        only ever be used when card is held)

        Args:
            screen (pygame.surface.Surface): screen to draw on
            is_held (bool, optional): True if card is currently held. Defaults
                to True
        """
        # if is_held:
        #     shadow = self.rect.copy()
        #     shadow.y += 10
        #     shadow.x += 10
        #     trans_surf = pygame.Surface((shadow.width, shadow.height), pygame.SRCALPHA)
        #     pygame.draw.rect(
        #         trans_surf,
        #         (0, 0, 0, 150),
        #         (0, 0, shadow.width, shadow.height),
        #         border_radius=10,
        #     )
        #     screen.blit(trans_surf, (shadow.x, shadow.y))
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        """
        Checks if card is clicked

        Args:
            pos(tuple[int, int]): x, y pixel location on screen
        """
        return self.rect.collidepoint(pos)

    def update(self, dt: float) -> None:
        self.rect.center = self.smooth_animation(dt)


    def smooth_animation(self, dt: float) -> tuple[int, int]:
        Vector2 = pygame.math.Vector2
        mousex, mousey = pygame.mouse.get_pos()
        minimum_distance = 5
        maximum_distance = 10000
        target_vector = Vector2(mousex, mousey)
        follower_vector = Vector2(self.rect.centerx, self.rect.centery)
        new_follower_vector = Vector2(self.rect.centerx, self.rect.centery)

        distance = follower_vector.distance_to(target_vector)
        if distance > minimum_distance:
            direction_vector = (target_vector - follower_vector) / distance
            min_step = max(0, distance - maximum_distance)
            max_step = distance - minimum_distance
            step_distance = (min_step + (max_step - min_step) * 10) * dt
            new_follower_vector = follower_vector + direction_vector * step_distance
        return (int(new_follower_vector.x), int(new_follower_vector.y))

class CardGroup(pygame.sprite.Group):
    """
    pygame Group class that allows extra functionality
    """
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
