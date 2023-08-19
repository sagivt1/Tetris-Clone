import setting
import pygame
from pygame.image import load 
from os import path

class Preview():
    def __init__(self):

        # genral 
        self.surface = pygame.Surface((
            setting.SIDEBAR_WIDTH, 
            setting.GAME_HEIGHT * setting.PREVIEW_HEIGHT_FRACTION
            ))
        self.rect = self.surface.get_rect(topright = 
                                          (setting.WINDOW_WIDTH - setting.PADDING, setting.PADDING))
        self.display_surface = pygame.display.get_surface()

        # Shapes
        self.shape_surfaces = {shape : load(path.join('graphics',f'{shape}.png')).convert_alpha() for shape in setting.TETROMINOS.keys()}

        # Image position data
        self.increment_height = self.surface.get_height() / 3

    def display_pieces(self, shapes):
        
        x = self.surface.get_width() / 2
        
        for i, shape in enumerate(shapes):
            shape_surface = self.shape_surfaces[shape]
            y = (self.increment_height / 2) + self.increment_height * i
            rect = shape_surface.get_rect(center = (x,y))
            self.surface.blit(shape_surface, rect)
            


    def run(self, next_shapes):
        self.surface.fill(setting.GRAY)
        self.display_pieces(next_shapes)
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, setting.LINE_COLOR, self.rect, 2, 2)