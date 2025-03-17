import time
import copy

import pygame

from assets.balatro_cards_data import CARD_HEI, CARD_WID
from state_logic.game_manager import GameManagerLogic
from states.gui_elements.button import Button
from states.gui_elements.side_panel import SidePanel
from states.gui_elements.card_holder import CardHolder, DeckHolder
from states.pause import Pause
from states.blind_gameplay import Gameplay
from states.statebase import StateBase
from enums import HandType

class BlindSelect(StateBase):
    """Game state for selecting blinds"""
    buttons: pygame.sprite.Group
    manager: GameManagerLogic
    side_panel: SidePanel

    def __init__(self, game):
        super().__init__(game)
        self.manager = self.ctx["manager"]
        self.side_panel = SidePanel(self.pause, self.game.screen, self.manager)
        self.blinds = self.manager.blinds[:-4: -1]
        self._create_buttons()

    def pause(self) -> None:
        print("Pausing game")
        Pause(self.game)

    def _create_buttons(self) -> None:
        """Creates buttons for blind selection. To be called once at start-up"""
        self.buttons = pygame.sprite.Group()
        select_rect = pygame.Rect((400, 100), (CARD_WID * 3, CARD_WID))
        select = Button(
            select_rect,
            "Select",
            self.enter_blind,
            self.font15,
            pygame.Color("goldenrod3"),
            pygame.Color("white"),
        )
        self.buttons.add(select)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """
        if event.type == pygame.QUIT:
            self.game.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons.sprites():
                if isinstance(button, Button) and button.hovered:
                    button.callback()
            print("calling side pannel from blind select")
            self.side_panel.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Pause(self.game)

    def enter_blind(self) -> None:
        """Enters next blind"""
        Gameplay(self.game, self.side_panel)

    def update(self, dt: float) -> None:
        for button in self.buttons.sprites():
            if isinstance(button, Button):
                button.update(dt)
        self.side_panel.update(dt)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("darkgreen")
        self.buttons.draw(screen)
        self.side_panel.draw(screen)
        self.draw_text(f"Score at least: {self.blinds[0]}", self.font24, (400,150), pygame.Color("white"))
        pygame.display.flip()
