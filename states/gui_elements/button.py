import pygame


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        rect,
        text,
        callback,
        font=None,
        bg_color=(70, 70, 70),
        text_color=(255, 255, 255),
    ):
        """
        Initializes a new Button.

        Args:
            rect (tuple): (x, y, width, height) for the button.
            text (str): The text to display on the button.
            callback (callable): Function to call when the button is clicked.
            font (pygame.font.Font, optional): Font for the button text.
            bg_color (tuple, optional): Background color when not hovered.
            text_color (tuple, optional): Color of the button text.
        """
        super().__init__()
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.color = bg_color
        self.text_color = text_color
        self.font = font or pygame.font.SysFont("Arial", 20)
        self.hovered = False

        # Create an image surface for the button
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.render()

    def render(self):
        """
        Renders the button's appearance on its image surface.
        """
        # Choose color based on whether the button is hovered
        pygame.draw.rect(
            self.image, self.color, self.image.get_rect(), border_radius=10
        )
        # Render the text and center it on the button
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(
            center=(self.rect.width // 2, self.rect.height // 2)
        )
        self.image.blit(text_surf, text_rect)

    def update(self, dt: float):
        """
        Update the button state (e.g., hover state) every frame.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)