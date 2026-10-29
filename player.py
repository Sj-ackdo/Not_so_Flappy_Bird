import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, screen):
        super().__init__()
        self.image = image
        self.screen = screen
        self.image = pygame.transform.scale(self.image, (80, 70))
        self.player_rect = self.image.get_rect(
            center=self.screen.get_rect().center
        )

    def reset_position(self):
        self.player_rect = self.image.get_rect(
            center=self.screen.get_rect().center
        )

    def draw_player(self, pos):
        self.player_rect = self.image.get_rect(
            center = pos
        )
        self.screen.blit(self.image, self.player_rect)
