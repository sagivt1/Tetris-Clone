from pygame.sprite import Group
from random import choice
from timer import Timer
import setting
import pygame

TETROMINOS_LETTER_LIST = list(setting.TETROMINOS.keys())


class Game:
    def __init__(self, get_next_shape):
        # Setup
        self.surface = pygame.Surface((setting.GAME_WIDTH, setting.GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(setting.PADDING, setting.PADDING))
        self.sprites = pygame.sprite.Group()

        # Game connection
        self.get_next_shape = get_next_shape

        # Lines surface
        self.line_surface = pygame.Surface((setting.GAME_WIDTH, setting.GAME_HEIGHT))
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        # Tetromino
        self.field_data = [
            [0 for x in range(setting.COLUMNS)] for y in range(setting.ROWS)
        ]
        self.tetromino = Tetromino(
            choice(TETROMINOS_LETTER_LIST),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
        )

        # Timer
        self.down_speed = setting.UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_preesed = False
        self.timers = {
            "vertical move": Timer(self.down_speed, True, self.move_down),
            "horizontal move": Timer(setting.MOVE_WAIT_TIME),
            "rotate": Timer(setting.ROTATE_WAIT_TIME),
        }

        self.timers["vertical move"].activate()

    def create_new_tetromino(self):

        self.check_finished_row()
        self.tetromino = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data,
        )

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(1, setting.COLUMNS):
            x = col * setting.CELL_SIZE
            pygame.draw.line(
                self.surface,
                setting.LINE_COLOR,
                (x, 0),
                (x, self.surface.get_height()),
                1,
            )

        for row in range(1, setting.ROWS):
            y = row * setting.CELL_SIZE
            pygame.draw.line(
                self.surface,
                setting.LINE_COLOR,
                (0, y),
                (self.surface.get_width(), y),
                1,
            )

        self.surface.blit(self.line_surface, (0, 0))

    def check_finished_row(self):

        # Get full row index
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                # Delete full row
                for block in self.field_data[delete_row]:
                    block.kill()
                # Move down block
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1
            # Rebuild field data
            self.field_data = [
                [0 for x in range(setting.COLUMNS)] for y in range(setting.ROWS)
            ]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

    def input(self):
        keys = pygame.key.get_pressed()

        # Checking horizontal movement
        if not self.timers["horizontal move"].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers["horizontal move"].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers["horizontal move"].activate()

        # Checking rotation
        if not self.timers["rotate"].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers["rotate"].activate()

        # Down speedup
        if not self.down_preesed and keys[pygame.K_DOWN]:
            self.down_preesed = True
            self.timers["vertical move"].duration = self.down_speed_faster

        if self.down_preesed and not keys[pygame.K_DOWN]:
            self.down_preesed = False
            self.timers["vertical move"].duration = self.down_speed

    def run(self):

        # update
        self.input()
        self.timer_update()
        self.sprites.update()

        # Drawing
        self.surface.fill(setting.GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (setting.PADDING, setting.PADDING))
        pygame.draw.rect(self.display_surface, setting.LINE_COLOR, self.rect, 2, 2)


class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):

        # Setup
        self.shape = shape
        self.block_positions = setting.TETROMINOS[shape]["shape"]
        self.color = setting.TETROMINOS[shape]["color"]
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        # Block Creation
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # Collisions
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [
            block.horizontal_collide(int(block.pos.x + amount), self.field_data)
            for block in self.blocks
        ]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [
            block.vertical_collide(int(block.pos.y + amount), self.field_data)
            for block in self.blocks
        ]
        return True if any(collision_list) else False

    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount):
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):

        if not self.next_move_vertical_collide(self.blocks, 1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    # Rotate
    def rotate(self):
        if self.shape != "O":
            # Pivot
            pivot_pos = self.blocks[0].pos

            # New block pos
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            # Collision check
            for pos in new_block_positions:

                # Horizontal
                if pos.x < 0 or pos.x >= setting.COLUMNS:
                    return

                # Field
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return

                # Vertical / Floor
                if pos.y > setting.ROWS:
                    return

            # Implement new positions
            for block, new_block in zip(self.blocks, new_block_positions):
                block.pos = new_block


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):

        # Setup
        super().__init__(group)
        self.image = pygame.Surface((setting.CELL_SIZE, setting.CELL_SIZE))
        self.image.fill(color)

        # Position
        self.pos = pygame.Vector2(pos) + setting.BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=self.pos * setting.CELL_SIZE)

    def rotate(self, pivot_pos):
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < setting.COLUMNS:
            return True

        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= setting.ROWS:
            return True

        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * setting.CELL_SIZE
