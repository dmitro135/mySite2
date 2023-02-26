import pygame
from pygame.sprite import Sprite
from random import choice

class AlienBullets(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.aliens = ai_game.aliens
        random_alien = choice(self.aliens.sprites())
        self.color = (230, 0, 0)

        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.midbottom = random_alien.rect.center

        self.y = float(self.rect.y)

    def update(self):
        self.y += 1
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)