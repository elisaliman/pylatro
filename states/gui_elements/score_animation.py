import time
import pygame
from states.gui_elements.card import Card, Joker, CARD_WID, CARD_HEI
from states.gui_elements.side_panel import SidePanel
from utils import get_play_anim_start_x
from enums import AbilCategory

ANIMATION_START_DELAY = 0.7


class ScoreAnimation:
    card_points_images: list[pygame.surface.Surface]
    side_panel: SidePanel
    card_points: list[int]
    font: pygame.font.Font
    displayed_score: int
    current_card_index: int
    start_delay_timer: float
    card_display_timer: float
    completion_delay_timer: float | None
    playing: bool
    joker_anim: bool | None

    def __init__(
        self,
        side_panel: SidePanel,
        current: int,
        scores: tuple[int, int, int],
        cards: list[Card],
        jokers: list[Joker]
    ):
        """Initialize animation with target score and card point breakdown."""
        self.jokers = jokers
        self.side_panel = side_panel
        self.final_score, self.chips, self.mult = scores  # Target score to reach
        self.card_points = [
            card.chips for card in cards
        ]  # List of chips each card earned
        self.card_points_images = []
        self.font = pygame.font.Font(
            "assets/balatro.ttf", 20
        )  # Font for rendering text
        for i in range(len(self.card_points)):
            text_surface = self.font.render(
                f"+{self.card_points[i]}", True, pygame.Color("dodgerblue2")
            )
            self.card_points_images.append(text_surface)
        self.initial_score = current  # Score before any calculations
        self.displayed_score = current  # Score shown on screen
        self.current_card_index = 0  # Track which card's points are being revealed
        self.start_delay_timer = time.time()  # Timer for pre animation delay
        self.card_display_timer = time.time()  # Time tracker for card animation
        self.completion_delay_timer = None  # Timer for post animation delay
        self.playing = True  # Is animation running?
        self.joker_anim = None

    def update(self, dt: float):
        """Update the animation frame by frame."""
        if not self.playing:
            return
        if time.time() - self.start_delay_timer >= ANIMATION_START_DELAY:
            self.start_delay_timer = ANIMATION_START_DELAY

            if (
                self.current_card_index == len(self.card_points)
                and self.displayed_score < self.final_score
            ):
                self.side_panel.set_played_score(self.final_score - self.initial_score)
                difference = self.final_score - self.displayed_score
                increment = max(1, difference // 20)
                self.displayed_score = min(
                    self.final_score, self.displayed_score + increment
                )

            # Reveal next card’s score every 0.5s
            if self.current_card_index < len(self.card_points):
                if time.time() - self.card_display_timer > 0.5:
                    self.current_card_index += 1
                    self.chips += self.card_points[self.current_card_index - 1]
                    self.card_display_timer = time.time()

            # Animate Jokers that activate after all cards score
            if self.current_card_index == len(self.card_points):
                indies = [joker for joker in self.jokers if AbilCategory.INDIE in joker.jokerdata.ability_category]
                for joker in indies:
                    if joker.jokerdata.scored:
                        if self.joker_anim is None or self.joker_anim == True:
                            self.joker_anim = joker.score_anim()

            # Stop animation when displayed score reaches final score
            if (self.displayed_score >= self.final_score
                and self.current_card_index == len(self.card_points)
                and not self.completion_delay_timer):
                self.completion_delay_timer = time.time()
            if (self.completion_delay_timer
                and time.time() - self.completion_delay_timer > 1):
                self.playing = False

    def draw(self, screen: pygame.surface.Surface):
        """Draw the animation elements."""
        if not self.playing:
            return

        # Draw each revealed card’s score
        x_offset = get_play_anim_start_x(screen, len(self.card_points))
        for i in range(self.current_card_index):
            text_surface = self.card_points_images[i]
            screen.blit(text_surface, (x_offset, screen.get_size()[1] // 2 - CARD_HEI))
            x_offset += CARD_WID + 30  # Space out the numbers

        # Draw the dynamically updating score
        self.side_panel.update_score(self.displayed_score, self.chips, self.mult)

    def is_done(self):
        """Check if the animation has finished."""
        return not self.playing
