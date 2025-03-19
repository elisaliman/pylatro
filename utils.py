import inspect
import pygame
from states.gui_elements.card import CARD_WID


def caller_info():
    stack = inspect.stack()
    caller_function = stack[1].function  # Get the function name of the caller
    print(f"Called from: {caller_function}")


def get_play_anim_start_x(screen: pygame.surface.Surface, card_num: int) -> int:
    spacing = 30
    screen_w, screen_h = screen.get_size()
    tot_span = (card_num * CARD_WID) + (spacing * (card_num - 1))
    start_x = (screen_w // 2) - (tot_span // 2) + (CARD_WID // 2)
    return start_x
