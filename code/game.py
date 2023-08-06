from pygame.sprite import Group
from random import choice
import setting
import pygame

TETROMINOS_LETTER_LIST = list(setting.TETROMINOS.keys())

class Game:

    def __init__(self):
        #Setup
        self.surface = pygame.Surface((setting.GAME_WIDTH, setting.GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (setting.PADDING, setting.PADDING))
        self.sprites = pygame.sprite.Group()

        # Lines surface
        self.line_surface = pygame.Surface((setting.GAME_WIDTH, setting.GAME_HEIGHT))
        self.line_surface.fill((0, 255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # Tetromino
        self.tetromino = Tetromino(choice(TETROMINOS_LETTER_LIST), self.sprites)

    def draw_grid(self):
        for col in range(1, setting.COLUMNS):
            x = col * setting.CELL_SIZE
            pygame.draw.line(self.surface, setting.LINE_COLOR, (x,0), (x,self.surface.get_height()), 1)

        for row in range(1, setting.ROWS):
            y = row * setting.CELL_SIZE
            pygame.draw.line(self.surface, setting.LINE_COLOR, (0,y), (self.surface.get_width(),y), 1)

        self.surface.blit(self.line_surface, (0,0))

    def run(self):

        # Drawing
        self.surface.fill(setting.GRAY)
        self.sprites.draw(self.surface)
        

        self.draw_grid()
        self.display_surface.blit(self.surface, (setting.PADDING, setting.PADDING))
        pygame.draw.rect(self.display_surface, setting.LINE_COLOR, self.rect, 2, 2)

class Tetromino:

    def __init__(self, shape, group):
        
        # Setup
        self.block_positions = setting.TETROMINOS[shape]['shape']
        self.color = setting.TETROMINOS[shape]['color']

        # Block Creation
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]


class Block(pygame.sprite.Sprite):

    def __init__(self, group, pos, color):

        # Setup
        super().__init__(group)
        self.image = pygame.Surface((setting.CELL_SIZE,setting.CELL_SIZE))
        self.image.fill(color)

        # Position
        self.pos = pygame.Vector2(pos) + setting.BLOCK_OFFSET
        x = self.pos.x * setting.CELL_SIZE
        y = self.pos.y * setting.CELL_SIZE
        self.rect = self.image.get_rect(topleft = (x,y))
