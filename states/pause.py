import pygame
from states.statebase import StateBase


class Pause(StateBase):

    shadow: pygame.surface.Surface

    def __init__(self, game):
        super().__init__(game)
        wid, hei = game.screen.get_size()
        shadow = pygame.Surface((wid, hei), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow,
            (0, 0, 0, 150),
            (0, 0, wid, hei),
        )
        self.shadow = shadow

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """
        if event.type == pygame.QUIT:
            self.game.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_state()

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill("darkgreen")
        self.prev_state.draw(screen)
        screen.blit(self.shadow, (0, 0))
        pygame.display.flip()
