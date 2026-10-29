import pygame
import random

stop = False


class Pipe:
    def __init__(self, x, height, pipe_gap, speed, pipe, flip_pipe,
                 scale_x=1.0, scale_y=1.0):

        self.x = x
        self.height = height
        self.speed = speed
        self.player_passed = 0
        self.scale_x = scale_x
        self.scale_y = scale_y

        # Scale pipe images to match the screen resolution
        original_width, original_height = pipe.get_size()

        new_size = (
            max(1, int(original_width * scale_x)),
            max(1, int(original_height * scale_y))
        )

        self.pipe = pygame.transform.smoothscale(pipe, new_size)
        self.flip_pipe = pygame.transform.flip(self.pipe, False, True)

        # Scale the gap with the screen height
        pipe_gap = int(pipe_gap * scale_y)

        margin = int(80 * scale_y)
        margin = min(margin, height // 4)

        min_gap_y = margin + pipe_gap // 2
        max_gap_y = height - margin - pipe_gap // 2

        # Make sure the gap fits on screen
        if min_gap_y > max_gap_y:
            gap_y = height // 2
            pipe_gap = max(1, height - 2 * margin)
        else:
            gap_y = random.randint(min_gap_y, max_gap_y)

        self.top_y = gap_y - pipe_gap // 2
        self.bottom_y = gap_y + pipe_gap // 2

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        self.top_rect = self.flip_pipe.get_rect(
            midbottom=(
                int(self.x + self.pipe.get_width() // 2),
                self.top_y
            )
        )
        screen.blit(self.flip_pipe, self.top_rect)

        self.bottom_rect = self.pipe.get_rect(
            midtop=(
                int(self.x + self.pipe.get_width() // 2),
                self.bottom_y
            )
        )
        screen.blit(self.pipe, self.bottom_rect)

    def off_screen(self):
        return self.x + self.pipe.get_width() < 0


class PipeSpawner:
    def __init__(self, width, height, speed, pipe, flip_pipe,
                 player, screen):

        global stop
        stop = False

        self.player = player
        self.width = width
        self.height = height
        self.screen = screen
        self.points = 0

        # Reference resolution
        self.scale_x = width / 640
        self.scale_y = height / 480

        # Scale movement and spacing with resolution
        self.speed = max(1, int(speed * self.scale_x))
        self.spawn_distance = int(250 * self.scale_x)

        self.pipe = pipe
        self.flip_pipe = flip_pipe
        self.pipes = []

        self.pipes.append(self.create_pipe())

    def create_pipe(self):
        gap = random.randint(80, 250)

        return Pipe(
            self.width + int(50 * self.scale_x),
            self.height,
            gap,
            self.speed,
            self.pipe,
            self.flip_pipe,
            self.scale_x,
            self.scale_y
        )

    def update(self, player_rect):
        global stop

        if stop:
            return

        if self.pipes and self.pipes[-1].x <= (
            self.width - self.spawn_distance
        ):
            self.pipes.append(self.create_pipe())

        for pipe in self.pipes:
            top_rect = pipe.flip_pipe.get_rect(
                midbottom=(
                    int(pipe.x + pipe.pipe.get_width() // 2),
                    pipe.top_y
                )
            )

            bottom_rect = pipe.pipe.get_rect(
                midtop=(
                    int(pipe.x + pipe.pipe.get_width() // 2),
                    pipe.bottom_y
                )
            )

            if (player_rect.colliderect(top_rect)
                    or player_rect.colliderect(bottom_rect)):
                stop = True
                break

            if (player_rect.x >= bottom_rect.x + bottom_rect.width) and (pipe.player_passed == 0):
                pipe.player_passed = 1
                self.points += 1
                

            pipe.update()

        self.pipes = [
            pipe for pipe in self.pipes
            if not pipe.off_screen()
        ]

    def draw(self):
        for pipe in self.pipes:
            pipe.draw(self.screen)

