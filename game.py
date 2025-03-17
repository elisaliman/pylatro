import sys
import time
from typing import TYPE_CHECKING

import pygame

from states.gui_elements.card import Card, CardGroup
from states.title import Title

if TYPE_CHECKING:
    from states.statebase import StateBase  # Import only for type checking

MAX_DT: float = 0.15
BUTTON_COOLDOWN: float = 0.5

class Game:
    deck: list["Card"]
    cards: "CardGroup"
    held_card: Card | None
    prev_state: "StateBase"
    state_stack: list["StateBase"]
    state: "StateBase"
    dx: float
    prev_time: float
    fps: int
    last_button_click_time: float

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False
        self.state_stack = []
        self.state = Title(self)
        self.prev_time = 0.0
        self.last_button_click_time = time.time()
        self.fps = 120

    def run(self) -> None:
        """
        Main game loop
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.flip()

    def event_loop(self) -> None:
        """
        Runs current state's event handler
        """
        for event in pygame.event.get():
            self.state.handle_event(event)

    def update(self) -> None:
        """
        Updates game state based on time passed to handle animations, movements,
        etc. in order to be independent from fps
        """
        self.clock.tick(self.fps)
        now = time.time()
        dt = now - self.prev_time
        dt = min(dt, MAX_DT)
        self.prev_time = now
        self.state.update(dt)

    def draw(self):
        """
        Draws the current game state
        """
        self.state.draw(self.screen)

    def quit(self) -> None:
        """
        Quit the application
        """
        pygame.quit()
        sys.exit(0)
