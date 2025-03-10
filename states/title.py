import pygame
from states.statebase import StateBase
from states.gameplay import Gameplay

class Title(StateBase):
    def __init__(self, game):
        super().__init__(game)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """
        if event.type == pygame.QUIT:
            self.game.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                Gameplay(self.game).enter_state()
    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("darkgreen")
        self.rect = pygame.Rect((screen.get_rect().center), (50, 50))
        pygame.draw.rect(screen, "red", self.rect)