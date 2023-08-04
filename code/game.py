import setting
import pygame

class Game:

    def __init__(self):
        #Setup
        self.surface = pygame.Surface((setting.GAME_WIDTH, setting.GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()

    def run(self):
        self.display_surface.blit(self.surface, (setting.PADDING, setting.PADDING))