import setting
import pygame
from sys import exit

# Import Components
from game import Game
from score import Score
from preview import Preview

class Main:
    def __init__(self):

        # General Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((setting.WINDOW_WIDTH, setting.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris")

        # Components
        self.game = Game()
        self.score = Score()
        self.preview = Preview()
        

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
            self.preview.run()

            # Updating The Game => Tick
            pygame.display.update()
            self.clock.tick()


if __name__ == "__main__":
    main = Main()
    main.run()
