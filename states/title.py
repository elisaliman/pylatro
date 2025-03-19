import pygame

from states.blind_gameplay import Gameplay
from states.blind_select import BlindSelect
from states.statebase import StateBase
from state_logic.game_manager import GameManagerLogic
from enums import HandType


class Title(StateBase):
    title: pygame.surface.Surface
    title_rect: pygame.surface.Surface

    def __init__(self, game):
        super().__init__(game)
        self.screen_center = game.screen.get_rect().center
        self.title = self.font200.render("Balatro", True, "blue")
        self.rect = pygame.Rect(0, 0, 800, 400)
        self.rect.center = self.screen_center
        self.ctx = {
            "manager": GameManagerLogic()
        }  ###TODO: this means everytime the title screen is created, a new "Profile" is made

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """
        if event.type == pygame.QUIT:
            self.game.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                BlindSelect(self.game)

    def update(self, dt) -> None:
        pass

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("darkgreen")
        pygame.draw.rect(screen, "red", self.rect)
        screen.blit(self.title, self.title.get_rect(center=self.screen_center))
        pygame.display.flip()
