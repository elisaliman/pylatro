
import pygame
from typing import Callable
from assets.balatro_cards_data import CARD_HEI, CARD_WID
from states.gui_elements.button import Button
from state_logic.blind_logic import BlindLogic
from state_logic.game_manager import GameManagerLogic
from enums import HandType

class SidePanel():
    screen: pygame.surface.Surface
    rect: pygame.Rect
    box: pygame.Rect
    chips: pygame.surface.Surface | None
    mult: pygame.surface.Surface | None
    hand_type: HandType
    buttons: pygame.sprite.OrderedUpdates
    _blind_logic: BlindLogic | None
    manager: GameManagerLogic

    def __init__(self, pause_func: Callable, screen: pygame.surface.Surface, manager: GameManagerLogic):
        self.manager = manager
        self.font10 = pygame.font.Font("assets/balatro.ttf", 10)
        self.font15 = pygame.font.Font("assets/balatro.ttf", 15)
        self.font24 = pygame.font.Font("assets/balatro.ttf", 24)
        self.pause_func = pause_func
        screen_w, screen_h = screen.get_size()
        self.rect = pygame.Rect((screen_w // 15, 0), (screen_w // 6, screen_h))
        self.box_temp = pygame.Rect((self.rect.x, self.rect.y), (CARD_WID - 10, CARD_HEI // 2))
        self.hand_type = HandType.EMPTY
        self.chips = None
        self.mult = None
        self.X = self.font24.render("X", True, pygame.Color("crimson"))
        self.O = self.font24.render("0", True, pygame.Color("white"))
        self._blind_logic = None
        self._create_buttons()

    def pause(self) -> None:
        self.pause_func()

    def _create_buttons(self) -> None:
        self.buttons = pygame.sprite.OrderedUpdates()
        pause_rect = pygame.Rect((self.rect.left + 10, 570), (CARD_HEI * 0.7, CARD_WID))
        pause = Button(
            pause_rect,
            "Options",
            self.pause,
            self.font15,
            pygame.Color("goldenrod3"),
            pygame.Color("white"),
        )
        self.buttons.add(pause)

    def draw_box(self, screen: pygame.surface.Surface, pos: tuple[int, int], num: str, color: str, scale: tuple[float, float]=(1,1), text: str | None=None, has_small_box: bool=True) -> None:
        num_image = self.font24.render(num, True, pygame.Color(color))
        box = self.box_temp.copy()
        box.w, box.h = int(box.w * scale[0]), int(box.h * scale[1])
        box.center = pos
        pygame.draw.rect(screen, pygame.Color("grey10"), box, border_radius=5)
        if text:
            text_image = self.font10.render(text, True, pygame.Color("white"))
            text_size_x, text_size_y = text_image.get_size()
            if has_small_box:
                small_box = box.scale_by(0.85, 0.6)
                small_box.center = box.centerx, box.centery + text_size_y - 5
            screen.blit(text_image, (box.centerx - text_size_x // 2, box.y))
        else:
            if has_small_box:
                small_box = box.scale_by(0.9, 0.85)
                small_box.center = box.center
        if has_small_box:
            pygame.draw.rect(screen, pygame.Color("grey20"), small_box, border_radius=5)
            x, y = small_box.centerx, small_box.centery
        else:
            x, y = box.centerx, box.centery
        num_x, num_y = num_image.get_size()
        x -= num_x // 2
        y -= num_y // 2
        screen.blit(num_image, (x, y))


    def draw(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.rect(screen, pygame.Color("grey20"), self.rect)
        self.draw_box(screen, (self.rect.centerx, 430), "", "white", scale=(3.3, 1), has_small_box=False)
        self.draw_box(screen, (self.rect.centerx, 380), f"{self.hand_type.name}", "white", scale=(3.3, 1.5), has_small_box=False)
        pygame.draw.rect(screen, pygame.Color("dodgerblue2"), pygame.Rect((self.rect.left + 10, 405), (self.rect.width // 2.5, 40)), border_radius=5)
        pygame.draw.rect(screen, pygame.Color("crimson"), pygame.Rect((self.rect.right - self.rect.width // 2.5 - 10, 405), (self.rect.width // 2.5, 40)), border_radius=5)
        screen.blit(self.X, (184, 410))
        if self.chips and self.mult:
            screen.blit(self.chips, (150, 410))
            screen.blit(self.mult, (220, 410))
        else:
            screen.blit(self.O, (150, 410))
            screen.blit(self.O, (220, 410))
        self.draw_box(screen, (self.rect.right - 100, 500), str(self.num_hands), "dodgerblue2", text="Hands")
        self.draw_box(screen, (self.rect.right - 35, 500), str(self.num_discards), "crimson", text="Discards")
        self.draw_box(screen, (self.rect.centerx, 300), f"{self.score}", "white", text="Round Score", scale=(3.1, 1))
        self.draw_box(screen, (self.rect.right - 67, 560), f"${self.manager.money}", "goldenrod3", scale=(2.1, 1))
        self.draw_box(screen, (self.rect.right - 100, 620), f"{self.manager.ante}/8", "goldenrod3", text="Ante")
        self.draw_box(screen, (self.rect.right - 35, 620), str(self.manager.round), "goldenrod3", text="Round")
        self.buttons.draw(screen)

    def set_blind_logic(self, blind_logic: BlindLogic) -> None:
        self._blind_logic = blind_logic

    def remove_blind_logic(self) -> None:
        self._blind_logic = None
        self.num_hands = 4
        self.num_discards = 4

    def update(self, dt: float) -> None:
        for button in self.buttons:
            if isinstance(button, Button):
                button.update(dt)
        if self._blind_logic:
            self.num_hands = self._blind_logic.num_hands
            self.num_discards = self._blind_logic.num_discards
        else:
            self.num_hands, self.num_discards, self.score = 4, 4, 0

    def update_score(self, score: int, chips: int, mult: int) -> None:
        self.score = score
        self.chips = self.font24.render(str(chips), True, pygame.Color("white"))
        self.mult = self.font24.render(str(mult), True, pygame.Color("white"))

    def update_hand_type(self, hand_type: HandType) -> None:
        self.hand_type = hand_type
        chips, mult = self.manager.levels[hand_type]["chips"], self.manager.levels[hand_type]["mult"]
        self.chips = self.font24.render(str(chips), True, pygame.Color("white"))
        self.mult = self.font24.render(str(mult), True, pygame.Color("white"))

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons.sprites():
                if isinstance(button, Button) and button.hovered:
                    button.callback()
                    return