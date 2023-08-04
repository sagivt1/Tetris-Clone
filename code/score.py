import setting
import pygame


class Score:

    def __init__(self):
        self.surface = pygame.Surface((
            setting.SIDEBAR_WIDTH, 
            setting.GAME_HEIGHT * setting.SCORE_HEIGHT_FRACTION - setting.PADDING
            ))
        self.rect = self.surface.get_rect(bottomright = 
                                          (setting.WINDOW_WIDTH - setting.PADDING, setting.WINDOW_HEIGHT - setting.PADDING))
        self.display_surface = pygame.display.get_surface()

    def run(self):
        self.display_surface.blit(self.surface, self.rect)
