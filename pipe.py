import pygame
import random
from player import Sprite as player_sprite

stop = False

class Pipe:
    def __init__(self, x, height, pipe_gap, speed, pipe, flip_pipe):
        self.x = x
        self.height = height
        self.pipe = pipe
        self.flip_pipe = flip_pipe
        
        margin = 80
        gap_y = random.randint(
            margin + pipe_gap // 2,
            self.height - margin - pipe_gap // 2
        )
        self.top_y = gap_y - pipe_gap // 2
        self.bottom_y = gap_y + pipe_gap // 2

        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        self.top_rect = self.flip_pipe.get_rect(
            midbottom = (self.x + self.pipe.get_width() // 2,
                         self.top_y))
        screen.blit(self.flip_pipe, self.top_rect)

        self.bottom_rect = self.pipe.get_rect(
            midtop = (self.x  + self.pipe.get_width() // 2,
                      self.bottom_y))
        screen.blit(self.pipe, self.bottom_rect)

    def off_screen(self):
        return self.x + self.pipe.get_width() < 0
        

class PipeSpawner:
    def __init__(self, width, height, speed, pipe, flip_pipe, player, screen):
        self.player = player
        self.width = width
        self.height = height
        self.speed = speed
        self.pipes = []
        self.spawn_distance = 250
        self.pipe = pipe
        self.flip_pipe = flip_pipe
        self.screen = screen

        self.pipes.append(Pipe(self.width+50,self.height, random.randint(80,250), self.speed, self.pipe, self.flip_pipe))

    def update(self, player_rect):
        global stop

        if self.pipes[-1].x <= self.width - self.spawn_distance:
            self.pipes.append(Pipe(self.width+50,self.height, random.randint(80,250), self.speed, self.pipe, self.flip_pipe))

        for pipe in self.pipes:
            sz = pipe.pipe.get_size() # size of pipe

            top_rect = pipe.flip_pipe.get_rect(
                midbottom = (pipe.x + sz[0]//2, pipe.top_y)
            )
            bottom_rect = pipe.pipe.get_rect(
                midtop = (pipe.x + sz[0]//2, pipe.bottom_y)
            )
            
            if player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect):
                stop = True
            else:
                pipe.update()

        self.pipes = [
            pipe for pipe in self.pipes if not pipe.off_screen()
        ]
   
    def draw(self):
        for pipe in self.pipes:
            pipe.draw(self.screen)
