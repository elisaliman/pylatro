from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from game import Game  # Import only for type checking


class StateBase(ABC):
    def __init__(self, game: "Game"):
        self.game = game
        self.prev_state = None
        self.font15 = pygame.font.Font("assets/balatro.ttf", 15)
        self.font24 = pygame.font.Font("assets/balatro.ttf", 24)
        self.font200 = pygame.font.Font("assets/balatro.ttf", 200)
        # TODO: figure out if there is a better method of resizing fonts
        # if so, implement that wherever needed like self.draw_text()
        self.ctx = {}

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Gets event from main Game event loop. Functions as gameplay game loop
        """
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen: pygame.surface.Surface):
        """
        Draws screen for current state
        """
        raise NotImplementedError

    def update(self, dt: float) -> None:
        """
        Updates dt in order to run game independent of fps
        """
        pass

    def draw_text(
        self,
        text: str,
        font: pygame.font.Font,
        position: tuple[int, int],
        color: pygame.Color,
    ) -> None:
        """
        Renders text on the screen.

        Args:
            text: The string to render.
            font: font to use
            position: (x, y) tuple for the text position.
            color: RGB tuple for text color (default is white).
        """
        text_surface = font.render(text, True, color)
        self.game.screen.blit(text_surface, position)

    def enter_state(self) -> None:
        ctx = self.ctx
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
        self.game.state = self
        self.game.state.ctx = ctx

    def exit_state(self):
        ctx = self.ctx
        self.game.state_stack.pop()
        self.game.state = self.game.state_stack[-1]
        self.game.state.ctx = ctx
