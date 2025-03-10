import pygame
import sys
import time
from card import Card, CardGroup
from states.title import Title
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from states.statebase import StateBase  # Import only for type checking

class Game():
    deck: list['Card']
    cards: 'CardGroup'
    held_card: Card | None
    state_stack: list['StateBase']
    state: 'StateBase'
    dx: float
    prev_time: float
    fps: int

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False
        self.state_stack = [Title(self)]
        self.state = self.state_stack[-1]
        self.prev_time = 0.0
        self.fps = 60

    def run(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.flip()

    def event_loop(self):
        """
        Main event loop. Runs current state's event handler
        """
        for event in pygame.event.get():
            self.state.handle_event(event)

    def update(self) -> None:
        self.clock.tick(self.fps)
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        self.state.update(dt)


    def draw(self):
        self.state.draw(self.screen)

    def quit(self) -> None:
        """
        Quit the application
        """
        pygame.quit()
        sys.exit(0)
