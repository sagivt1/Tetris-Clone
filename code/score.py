import setting
import pygame
from os.path import join


class Score:
    def __init__(self):
        self.surface = pygame.Surface(
            (
                setting.SIDEBAR_WIDTH,
                setting.GAME_HEIGHT * setting.SCORE_HEIGHT_FRACTION - setting.PADDING,
            )
        )
        self.rect = self.surface.get_rect(
            bottomright=(
                setting.WINDOW_WIDTH - setting.PADDING,
                setting.WINDOW_HEIGHT - setting.PADDING,
            )
        )
        self.display_surface = pygame.display.get_surface()

        # font
        self.font = pygame.font.Font(join("graphics", "Russo_One.ttf"), 30)

        # Increment
        self.increment_height = self.surface.get_height() / 3

        # Score data
        self.level = 1
        self.score = 0
        self.lines = 0

    def display_text(self, pos, text):
        text_surface = self.font.render(f"{text[0]}: {text[1]}", True, "white")
        text_rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):

        self.surface.fill(setting.GRAY)
        x = self.surface.get_width() / 2
        for i, text in enumerate(
            [("Score", self.score), ("Level", self.level), ("Lines", self.lines)]
        ):
            y = self.increment_height / 2 + i * self.increment_height
            self.display_text((x, y), text)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, setting.LINE_COLOR, self.rect, 2, 2)
