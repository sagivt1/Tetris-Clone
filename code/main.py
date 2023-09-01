import setting
import pygame
from sys import exit

# Import Components
from game import Game
from score import Score
from preview import Preview

from random import choice

TETROMINOS_LETTER_LIST = list(setting.TETROMINOS.keys())


class Main:
    def __init__(self):

        # General Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (setting.WINDOW_WIDTH, setting.WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris")

        # Shapes
        self.next_shapes = [choice(TETROMINOS_LETTER_LIST) for shape in range(3)]
        print(self.next_shapes)

        # Components
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(TETROMINOS_LETTER_LIST))
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Display
            self.display_surface.fill(setting.GRAY)

            # Components Run
            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            # Updating The Game => Tick
            pygame.display.update()
            self.clock.tick()


if __name__ == "__main__":
    main = Main()
    main.run()
