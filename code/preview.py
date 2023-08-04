import setting
import pygame

class Preview():
    def __init__(self):
        self.surface = pygame.Surface((
            setting.SIDEBAR_WIDTH, 
            setting.GAME_HEIGHT * setting.PREVIEW_HEIGHT_FRACTION
            ))
        self.rect = self.surface.get_rect(topright = 
                                          (setting.WINDOW_WIDTH - setting.PADDING, setting.PADDING))
        self.display_surface = pygame.display.get_surface()

    def run(self):
        self.display_surface.blit(self.surface, self.rect)