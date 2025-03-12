import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game  # Import only for type checking


class StateBase(ABC):
    def __init__(self, game: 'Game'):
        self.game = game
        self.prev_state = None
        self.font24 = pygame.font.Font("assets/balatro.ttf", 24)
        self.font200 = pygame.font.Font("assets/balatro.ttf", 200)

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

    def enter_state(self) -> None:
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
        self.game.state = self

    def exit_state(self):
        self.game.state_stack.pop()
        self.game.state = self.game.state_stack[-1]

