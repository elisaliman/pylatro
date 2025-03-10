import pygame
import sys
from card import Card, CardGroup
from enums import Suit, Rank
from states.statebase import StateBase
from states.title import Title

class Game():
    deck: list[Card]
    cards: CardGroup
    held_card: Card | None
    state_stack: list[StateBase]
    state: StateBase

    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.done = False
        self.state_stack = [Title(self)]
        self.state = self.state_stack[-1]

    def run(self):
        while not self.done:
            self.event_loop()
            self.draw()
            pygame.display.flip()

    def event_loop(self):
        """
        Main event loop. Runs current state's event handler
        """
        for event in pygame.event.get():
            self.state.handle_event(event)

    def draw(self):
        self.state.draw(self.screen)

    # def back_state(self):
    #     """
    #     Flips game to next state in the state stack
    #     """
    #     self.state.done = False
    #     self.state_name = self.state_stack.pop()
    #     ctx = self.state.ctx
    #     self.state = self.state_map[self.state_name]
    #     self.state.startup(ctx)

    def quit(self) -> None:
        """
        Quit the application
        """
        pygame.quit()
        sys.exit(0)
