import pygame
from abc import ABC, abstractmethod

class StateBase(ABC):
    def __init__(self):
        self.done = False
        self.quit = False
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.ctx = {}
        self.font = pygame.font.Font(None, 24)